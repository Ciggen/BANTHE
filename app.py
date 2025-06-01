# ----- 
# Loading packages
import os
from flask import Flask, request, render_template, jsonify, flash, redirect
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL   
import pandas as pd
import sqlite3
import warnings
import folium

import pickle
import polyline
import osmnx as ox



# Machine learning packages
from flask import render_template_string
from surprise import SVDpp, Dataset, Reader
from surprise.model_selection import train_test_split, cross_validate, KFold


# Basic Flask configuration
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ignore unimportant warnings 
warnings.filterwarnings("ignore")

# Retrive the database created from db.py script. 
# You need to run str459.ibynb, and db.py first! 
db = SQL("sqlite:///books.db")
db_2 = SQL("sqlite:///BANTHE.db")

graph = ox.load_graphml("vestlandet_bounded_road_network.graphml")


@app.route("/map")
def map_view():
    try:
        clusters = db_2.execute("SELECT cluster_id, cluster_name, latitude, longitude FROM clusters")
        if not clusters:
            return "<p>No cluster data found.</p>"

        avg_lat = sum(c["latitude"] for c in clusters) / len(clusters)
        avg_lon = sum(c["longitude"] for c in clusters) / len(clusters)
        fmap = folium.Map(location=[avg_lat, avg_lon], zoom_start=11)

        for c in clusters:
            folium.Marker(
                location=[c["latitude"], c["longitude"]],
                popup=f"{c['cluster_name']} (ID: {c['cluster_id']})",
                tooltip=c["cluster_name"],
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(fmap)

        map_html = fmap._repr_html_()

        return render_template_string("""
            <!DOCTYPE html>
            <html><head><meta charset="UTF-8"><title>Cluster Map</title></head>
            <body style="margin:0;">
                {{ map_html | safe }}
            </body>
            </html>
        """, map_html=map_html)

    except Exception as e:
        return f"<p>Could not load map: {e}</p>"
    
@app.route("/optimized_routes_from_cluster")
def optimized_routes_from_cluster():
    try:
        import osmnx as ox
        graph = ox.load_graphml("vestlandet_bounded_road_network.graphml")

        s_cl = int(request.args.get("start_cluster", 1))  # Default cluster

        def hent_coords(tabell, id_felt, verdi):
            result = db_2.execute(f"SELECT latitude, longitude FROM {tabell} WHERE {id_felt} = ?", verdi)
            return (result[0]["latitude"], result[0]["longitude"]) if result else None

        def safe_decode(blob, datatype):
            if not blob:
                return []
            try:
                data = pickle.loads(blob)
                if datatype == "entur":
                    return polyline.decode(data)
                elif datatype == "ferry":
                    return data
                elif datatype == "osm":
                    return [(graph.nodes[n]["y"], graph.nodes[n]["x"]) for n in data if n in graph.nodes]
            except Exception as e:
                print(f"❌ Feil ved {datatype}-dekoding: {e}")
            return []

        def draw(coords, color, popup):
            if coords and len(coords) > 1:
                folium.PolyLine(coords, color=color, popup=popup, weight=4).add_to(m)

        start_coords = hent_coords("clusters", "cluster_id", s_cl)
        if not start_coords:
            return f"<p>❌ Fant ikke koordinater for cluster {s_cl}</p>"

        m = folium.Map(location=start_coords, zoom_start=9)
        folium.Marker(start_coords, popup=f"Start Cluster {s_cl}", icon=folium.Icon(color="green")).add_to(m)

        rows = db_2.execute("SELECT * FROM optimized_routes_limited_quays WHERE start_cluster_id = ?", s_cl)

        for row in rows:
            e_cl = int(row["end_cluster_id"])
            e_coords = hent_coords("clusters", "cluster_id", e_cl)
            if e_coords:
                folium.Marker(e_coords, popup=f"End Cluster {e_cl}", icon=folium.Icon(color="red")).add_to(m)

            # Til kai
            if row["start_route_id"]:
                r = db_2.execute("SELECT route_entur, route FROM cluster_to_quay_routes WHERE bus_quay_route_id = ?", row["start_route_id"])
                if r:
                    coords = safe_decode(r[0]["route_entur"] or r[0]["route"], "entur" if r[0]["route_entur"] else "osm")
                    draw(coords, "blue", f"Til kai ➜ {row['start_quay_id']}")

            # Ferje
            if row["start_quay_id"] and row["end_quay_id"]:
                ferry = db_2.execute("SELECT ferry_route FROM quay_distances WHERE start_quay_id = ? AND end_quay_id = ?", row["start_quay_id"], row["end_quay_id"])
                if ferry:
                    coords = safe_decode(ferry[0]["ferry_route"], "ferry")
                    draw(coords, "purple", f"Ferje {row['start_quay_id']} → {row['end_quay_id']}")

            # Fra kai
            if row["end_route_id"]:
                r = db_2.execute("SELECT route_entur, route FROM cluster_to_quay_routes WHERE bus_quay_route_id = ?", row["end_route_id"])
                if r:
                    coords = safe_decode(r[0]["route_entur"] or r[0]["route"], "entur" if r[0]["route_entur"] else "osm")
                    draw(coords, "blue", f"Fra kai ➜ {e_cl}")

            # Direkte buss – hent fra bus_routes_with_emission hvis ingen quay-ruter
            if not row.get("start_route_id") and not row.get("end_route_id") and not row.get("start_quay_id") and not row.get("end_quay_id"):
                r = db_2.execute("""
                    SELECT route_entur, route FROM bus_routes_with_emission
                    WHERE start_cluster_id = ? AND end_cluster_id = ?
                """, row["start_cluster_id"], row["end_cluster_id"])
                if r:
                    coords = safe_decode(r[0]["route_entur"] or r[0]["route"], "entur" if r[0]["route_entur"] else "osm")
                    draw(coords, "green", f"Direkte buss {row['start_cluster_id']} → {row['end_cluster_id']}")

        html = m._repr_html_()
        return render_template_string("""
        <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Optimaliserte ruter</title></head>
        <body style="margin:0;">{{ html | safe }}</body></html>
        """, html=html)

    except Exception as e:
        return f"<p>🚨 Feil: {e}</p>"





# Endpoint to retrieve data from db, and display different datasets
@app.route("/", methods=["GET", "POST"])
def index():
    all_userIDs = db.execute("SELECT DISTINCT userID FROM user_ratings_books_info")
    all_books = db.execute("SELECT DISTINCT title, author FROM user_ratings_books_info ORDER BY title, author")

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            books = db.execute("SELECT title, author, ISBN, imageUrlM FROM user_ratings_books_info WHERE title LIKE ? LIMIT 1", ('%' + query + '%',))
            return render_template("index.html", books=books, all_books=all_books, all_userIDs=all_userIDs)
        else:
            flash("string aquried", "error")
    
    return render_template("index.html", all_books=all_books, all_userIDs=all_userIDs)


# Retrive data for search bar.
@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return jsonify([]) 

    books = db.execute("SELECT title, author, ISBN, imageUrlM FROM user_ratings_books_info WHERE title LIKE ? LIMIT 1", ('%' + query + '%',))
    return jsonify(books)
    

# Add ratings to each book for user 1. 
@app.route("/add_book_rating", methods=["POST"])
def add_book_rating():
    data = request.get_json()
    books = data.get("books")  

    if not books:
        return jsonify({"error": "No books provided"}), 400

    try:
        for book in books:
            userID = book.get("userID")
            isbn = book.get("isbn")
            rating = book.get("rating")

            if not all([userID, isbn, rating]):
                return jsonify({"error": "All fields are required"}), 400

            db.execute("INSERT INTO user_ratings_books_info (userID, ISBN, bookRating) VALUES (?, ?, ?)",
                       userID, isbn, rating)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "All book ratings added successfully"}), 201


# Create dataset for recommendation model 
def load_data():
    conn = sqlite3.connect('books.db')
    query = """
    SELECT userID, ISBN, bookRating, title, author, imageUrlM
    FROM user_ratings_books_info
    """
    books_data = pd.read_sql_query(query, conn)
    conn.close()

    reader = Reader(rating_scale=(0, 10))
    data = Dataset.load_from_df(books_data[['userID', 'ISBN', 'bookRating']], reader)
    trainset = data.build_full_trainset()

    svd_model = SVDpp()
    svd_model.fit(trainset)
    return svd_model, trainset, books_data

# Get recommendations - same function form the ibynb file, using the SVDpp method: 
@app.route("/get_recommendations", methods=["POST"])

def get_recommendations():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    model, trainset, books_data = load_data()

    try:
        recommendations = recommend_books(user_id, model, trainset, n=5)
        results = []
        for pred in recommendations:
            book = books_data[books_data['ISBN'] == pred.iid].iloc[0]
            results.append({
                'ISBN': pred.iid,
                'Estimated Rating': pred.est,
                'Title': book['title'],
                'Author': book['author'],
                'ImageUrl': book['imageUrlM']
            })
        return jsonify(results)
    except ValueError:
        return jsonify({'error': 'user not found in the dataset'}), 404


# Threshold = 6 in rating, results = top 5 books, as in the original script. 
def recommend_books(user_id, model, trainset, n=5, threshold=6):
    try:
        inner_uid = trainset.to_inner_uid(user_id)
    except ValueError:
        raise ValueError("User not found")
    
    user_items = set(jid for (jid, _) in trainset.ur[inner_uid])
    unrated_books = [trainset.to_raw_iid(iid) for iid in trainset.all_items() if iid not in user_items]
    predictions = [model.predict(user_id, iid) for iid in unrated_books]
    predictions.sort(key=lambda x: x.est, reverse=True)
    return [pred for pred in predictions if pred.est >= threshold][:n]

# Retrive title. 
def get_book_title(isbn, books_data):
    match = books_data[books_data['ISBN'] == isbn]
    return match.iloc[0]['title'] if not match.empty else "Unknown book"

# Delete user 1 from DB, after "reset"
@app.route("/reset_user", methods=["POST"])
def reset_user():
    try:
        db.execute("DELETE FROM user_ratings_books_info WHERE userID = 1")
        return jsonify({"message": "User 1 reset successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5006)