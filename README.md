# BANTHE – Assessing the Impact of Replacing Bus Routes with Hydrogen Boats in Bergen:
An Optimization Study using Linear Programming

🚀 Purpose
BANTHE is a Python-based linear optimization model developed to explore the emission-reduction potential of integrating hydrogen-powered boat transport into Bergen’s public transport system. Using real public transport data, routing algorithms, and a gravity model of travel demand, the system identifies low-emission multimodal routes between spatial clusters in the region.

📦 Project Structure
The code is structured around three main phases:

1. Data Preprocessing
Load and filter public transport boarding data (Skyss)

Cluster population and employment data (SSB) using KMeans

Clean and load quay location data

Compute travel distances between clusters using:

Road routing (OSM + A*)

Multimodal routing for island clusters (Entur API + boat routes)

Construct a gravity-based travel demand matrix using a Weibull distribution


2. Optimization (Linear Programming)
Identify optimal route (bus or boat) per cluster pair

Objective: Minimize total CO₂ emissions

Constraint: Maximum 20% increase in travel time over direct bus route


3. Evaluation
Quantify emissions, travel times, and boat usage

Compare optimized network against bus-only baseline

Visualize quay usage and passenger flow across scenarios

Key Files
File	Description
BANTHE_main.ipynb	Jupyter Notebook with all pipeline steps
Input/	Raw input data (boarding, population, quays, routes)
Output/	Generated matrices, emissions, optimization results
Database/BANTHE.db	SQLite database storing intermediate data
.gitignore	Ignores temporary or large files (e.g., routes)


Methodology Highlights
Routing: Uses A* on OpenStreetMap for road routes; Entur API for inaccessible clusters

Travel Time Calibration: Boat times calibrated using real crossings (e.g., Hufthamar–Krokeide)

Emissions: CO₂e estimated from fuel consumption data (Skyss, 2023)

Gravity Model: Weibull-distributed probability decay based on distance

Multimodal Chains: Precomputed combinations of cluster → quay → boat → quay → cluster

Results Summary
Scenario	Emissions (tons CO₂)	Reduction vs. Baseline
Bus-Only (Baseline)	46,982	–
Optimized (120% time limit)	40,052	↓ ~14.75%
Optimized (No limit)	25,288	↓ ~46%

~29% of optimized trips use boat segments

Contact
Developed as part of a Master's thesis (2024). For questions or collaboration inquiries, contact: sondresiger@hotmail.no 

