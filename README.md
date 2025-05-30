# 🚍 Windsor Transit Bus Occupancy Analysis – Capstone Project

![Windsor Transit Bus](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Windsor_Terminal_and_Tunnel_Bus.jpg/1100px-Windsor_Terminal_and_Tunnel_Bus.jpg)

This repository contains selected open-source components from a capstone project focused on analyzing and predicting bus occupancy trends for Windsor Transit. The project integrates data engineering, machine learning, and dashboard visualization to support transit planning and optimization.

> ⚠️ **Disclaimer:** Some project files are excluded from this repository due to data confidentiality agreements with Windsor Transit. Only code and notebooks that use publicly available data or simulated examples are shared here.

---

## 📁 Repository Overview

### 🔹 `main` branch – Data Processing and Analysis
- `webscrape.py`: Automates GTFS data extraction from the [City of Windsor Open Data Portal](https://opendata.citywindsor.ca/), converts `.txt` GTFS feeds to Excel, and uploads files to GitHub with Microsoft Teams notifications.
- `optimized_code.ipynb`: Streamlines and optimizes raw GTFS data for analysis.
- `updated_correlation_heatmap.ipynb`: Explores correlations between route data, time, and occupancy-related features.

### 🔹 `machine-learning-model` branch – Bus Occupancy Prediction
- `modeling.ipynb`: Builds and evaluates a machine learning model to predict bus crowding levels. Uses engineered features from GTFS feeds (e.g., time of day, route ID, stop patterns).

> 🚫 **Private Files Not Included:**
> - Proprietary Windsor Transit datasets not available on public data portals
> - Real-time passenger counts and internal route annotations
> - Final interactive dashboard (due to licensing and privacy restrictions)

---

## 🎯 Project Objectives

- Analyze historical GTFS data to uncover occupancy trends
- Predict bus crowding using machine learning
- Support Windsor Transit in improving route efficiency and rider experience
- Build a reproducible and scalable data pipeline

---

## 🛠️ Tools & Technologies

- **Languages**: Python
- **Data Libraries**: `pandas`, `scikit-learn`, `seaborn`, `matplotlib`
- **Web Scraping**: `requests`, `BeautifulSoup`
- **Excel Processing**: `openpyxl`
- **Version Control**: GitHub API, branching
- **Collaboration**: Microsoft Teams webhook notifications
- **Data Source**: [City of Windsor Open Data Portal](https://opendata.citywindsor.ca/), 13 months' APC Datasets


