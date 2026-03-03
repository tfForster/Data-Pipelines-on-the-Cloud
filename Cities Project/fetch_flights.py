import pandas as pd
import requests
from datetime import datetime, timedelta
from db_config import engine
import os

API_KEY = os.getenv("AERODATABOX_KEY")

BASE_URL = "https://aerodatabox.p.rapidapi.com/flights/airports/iata"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
}

# Städte definieren
cities = [
    {"city_id": 1, "iata": "BER"}, 
    {"city_id": 2, "iata": "HAM"},
    {"city_id": 3, "iata": "MUC"}
]

# Morgen berechnen (00:00 - 12:00)
tomorrow = datetime.now() + timedelta(days=1)
date_str = tomorrow.strftime("%Y-%m-%d")

time_ranges = [
    (f"{date_str}T00:00", f"{date_str}T12:00"),
    (f"{date_str}T12:00", f"{date_str}T23:59")
]

all_flights = []

for city in cities:

    for start_time, end_time in time_ranges:

        print(f"📡 Lade Flüge für {city['iata']} von {start_time} bis {end_time}")

        url = f"{BASE_URL}/{city['iata']}/{start_time}/{end_time}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Fehler bei {city['iata']}:", response.status_code)
            continue

        data = response.json()
        departures = data.get("departures", [])

        for flight in departures:

            if flight.get("codeshareStatus") != "IsOperator":
                continue

            utc_time_str = flight.get("movement", {}).get("scheduledTime", {}).get("utc")

            if utc_time_str:
                utc_time_str = utc_time_str.replace("Z", "")
                arrival_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M")
            else:
                arrival_time = None

            all_flights.append({
                "city_id": city["city_id"],
                "flight_number": flight.get("number"),
                "airline": flight.get("airline", {}).get("name"),
                "arrival_airport": flight.get("movement", {}).get("airport", {}).get("iata"),
                "arrival_time": arrival_time,
                "status": flight.get("status")
            })

# DataFrame erstellen
flights_df = pd.DataFrame(all_flights)

if not flights_df.empty:
    flights_df.to_sql("flights", engine, if_exists="append", index=False)
    print("✅ Flights erfolgreich eingefügt!")
else:
    print("⚠️ Keine Flugdaten gefunden.")
