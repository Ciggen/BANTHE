# BANTHE – Norwegian School of Economics (NHH) - Independent Thesies in Business Analytics

## "Assessing the Impact of Replacing Bus Routes with Hydrogen Boats in Bergen"  
### - *A Linear Programming Optimization Study*

#### ---- Authors: Sondre Sejersted Siger and Eirik Korshamn ----

## 📘 Introduction

This program was developed as part of our master’s thesis at NHH, focusing on optimizing public transport routes in the Bergen region by integrating hydrogen-powered boats. The full pipeline is structured into **13 sequential steps**, as illustrated in the flowchart (see Appendix B).

> NB! The thesis will be published and linked here after formal evaluation, in order to avoid issues related to plagiarism detection.


### 🚀 Purpose
BANTHE is a Python-based linear optimization model developed to explore the emission-reduction potential of integrating hydrogen-powered boat transport into Bergen’s public transport system. Using real public transport data, routing algorithms, and a gravity model of travel demand, the system identifies low-emission multimodal routes between spatial clusters in the region.

### 📦 Project Structure
The code is structured around three main phases:

The entire pipeline follows a structured sequence of 13 documented steps, from data ingestion to optimization and results analysis. Each step corresponds to a specific task, as illustrated in the flow diagram below.

Each code block in the main notebook (BANTHE_main.ipynb) begins with a descriptive header that explains what that block accomplishes (e.g., “Step 5 – Compute All Cluster-to-Cluster Travel Routes”). This makes the code easy to follow, modify, and reuse.

The steps are grouped into three main phases:

### 🧹 Preprocessing (Steps 1–10)
Install required packages and initialize database

Import Skyss passenger boarding data

Generate spatial population/employment clusters

Import ferry quays and compute distances

Calculate cluster-to-cluster travel routes

Simulate inter-cluster demand via gravity model

Define emissions per transport mode

Calculate emissions for bus-only routes

Estimate boat-compatible routes from clusters to quays

Prepare final dataset for optimization

### ⚙️ Optimization (Step 11)
Solve the emission-minimizing assignment problem under travel time constraints

### 📊 Analysis (Steps 12–13)
Generate baseline (bus-only) emissions

Summarize and compare results: emissions, time, mode share

Each step is self-contained and can be run independently, allowing flexibility in debugging or applying the method to new datasets.

Key Files
File	Description
BANTHE_main.ipynb	Jupyter Notebook with all pipeline steps
Input/	Raw input data (boarding (Skyss-data), population (SSB), quays, boat routes (91)).
Output/	Generated matrices, emissions, optimization results
Database/BANTHE.db	SQLite database storing intermediate data
.gitignore	Ignores temporary or large files (e.g., routes)

Results Summary
Scenario	Emissions (tons CO₂)	Reduction vs. Baseline
Bus-Only (Baseline)	46,982	–
Optimized (120% time limit)	40,052	↓ ~14.75%
Optimized (No limit)	25,288	↓ ~46%

~29% of optimized trips use boat segments

Contact
Developed as part of a Master's thesis (2024) at NHH - authors Sondre Sejersted Siger & Eirik Korshamn. For questions or collaboration inquiries, contact: sondresiger@hotmail.no.

## 📱 App
Although slightly outside the core scope of this thesis, we are also developing an app (see the app/ folder) to visualize the optimized transport solutions.

The current MVP (minimum viable product) supports:

Loading results from a selected optimization scenario

Selecting a start cluster and viewing routes to all possible destination clusters

The app can be downloaded and run locally on any computer with Python installed. This makes it accessible for those who want to explore the model's outputs interactively, either for further analysis or demonstration purposes.

A more advanced version is currently under development—for our personal portfolios and for anyone interested in engaging with the model in a user-friendly format.

