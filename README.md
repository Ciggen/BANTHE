# BANTHE – Norwegian School of Economics (NHH) - Independent Thesies in Business Analytics

## "Assessing the Impact of Replacing Bus Routes with Hydrogen Boats in Bergen"  
### - *A Linear Programming Optimization Study*

#### Authors: Sondre Sejersted Siger & Eirik Korshamn

## 📘 Introduction

This program was developed as part of our master’s thesis at NHH, focusing on optimizing public transport routes in the Bergen region by integrating hydrogen-powered boats. The full pipeline is structured into **13 sequential steps**, as illustrated in the flowchart (see Appendix B), for full SQL/database structure (see Appendix C).

> NB! The thesis will be published and linked here after formal evaluation, in order to avoid issues related to plagiarism detection.


### 🚀 Purpose
BANTHE is a Python-based linear optimization model developed to explore the emission-reduction potential of integrating hydrogen-powered boat transport into Bergen’s public transport system. Using real public transport data, routing algorithms, and a gravity model of travel demand, the system identifies low-emission multimodal routes between spatial clusters in the region.

### 📦 Project Structure
The code is structured around three main phases:

The entire pipeline follows a structured sequence of 13 documented steps, from data ingestion to optimization and results analysis. Each step corresponds to a specific task, as illustrated in the flow diagram below.

Each code block in the main notebook (BANTHE_main.ipynb) begins with a descriptive header that explains what that block accomplishes (e.g., “Step 5 – Compute All Cluster-to-Cluster Travel Routes”). This makes the code easy to follow, modify, and reuse.

The steps are grouped into three main phases:

### 🧹 Preprocessing (Steps 1–10)
1. Install required packages and initialize database

2. Import Skyss passenger boarding data

3. Generate spatial population/employment clusters

4. Import ferry quays and compute distances

5. Calculate cluster-to-cluster travel routes

6. Simulate inter-cluster demand via gravity model

7. Define emissions per transport mode

8. Calculate emissions for bus-only routes

9. Estimate boat-compatible routes from clusters to quays

10. Prepare final dataset for optimization

### ⚙️ Optimization (Step 11)
11. Solve the emission-minimizing assignment problem under travel time constraints

### 📊 Analysis (Steps 12–13)
12. Generate baseline (bus-only) emissions

13. Summarize and compare results: emissions, time, mode share

Each step is self-contained and can be run independently, allowing flexibility in debugging or applying the method to new datasets.

Key Files
File	Description
BANTHE_main.ipynb	Jupyter Notebook with all pipeline steps
Input/	Raw input data (boarding (Skyss-data), population (SSB), quays, boat routes (91)).
Output/	Generated matrices, emissions, optimization results
Database/BANTHE.db	SQLite database storing intermediate data
.gitignore	Ignores temporary or large files (e.g., routes)

-------------------------------------
Results Summary
Scenario	Emissions (tons CO₂)	Reduction vs. Baseline
Bus-Only (Baseline)	46,982	–
Optimized (120% time limit)	40,052	↓ ~14.75%
Optimized (No limit)	25,288	↓ ~46%

~29% of optimized trips use boat segments

Contact
Developed as part of a Master's thesis (2024) at NHH - authors Sondre Sejersted Siger & Eirik Korshamn. For questions or collaboration inquiries, contact: sondresiger@hotmail.no.

-------------------------------------

## 📱 App
Although slightly outside the core scope of this thesis, we are also developing an app (see the app/ folder) to visualize the optimized transport solutions.

The current MVP (minimum viable product) supports:

Loading results from a selected optimization scenario

Selecting a start cluster and viewing routes to all reachable destination clusters

The app can be downloaded and run locally on any computer with Python installed. This allows users to explore the model's outputs interactively—either for further analysis or demonstration purposes.

⚠️ Note: To use the app locally, you must first run the main notebook (BANTHE_main.ipynb) to generate the local SQLite database (BANTHE.db). This database is required for the app to function properly.

An extended version of the app is currently in development, intended for our personal portfolios and for those interested in a more refined and user-friendly interface.
