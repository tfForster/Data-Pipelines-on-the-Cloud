# Automated Data Pipeline (Local Version)

Small end-to-end data pipeline built with Python and MySQL.

---

## 📌 Project Overview

This project collects city-related data (cities, population, weather and flights) from public APIs and stores it in a relational MySQL database.

The pipeline is structured into separate Python scripts for:

- Inserting cities  
- Fetching population data  
- Fetching weather data  
- Fetching flight data  

The database schema and EER diagram are included in this repository.

---

## 🛠 Tech Stack

- Python  
- Pandas  
- Requests  
- MySQL  
- SQLAlchemy  

---

## ⚙️ Setup

1. Create a MySQL database.
2. Run the SQL creation script to generate the tables.
3. Add your API keys in a `.env` file.
4. Run the Python scripts to populate the database.

---

## ☁️ Cloud Version

A cloud-based version of this pipeline was deployed using:

- Google Cloud SQL  
- Google Cloud Functions  
- Google Cloud Scheduler  

This allowed the pipeline to run automatically once per day.
