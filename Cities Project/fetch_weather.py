import pandas as pd
import requests
from datetime import datetime
from db_config import engine
import os

API_KEY = os.getenv("OPENWEATHER_KEY")

cities_from_db = pd.read_sql(
    "SELECT city_id, latitude, longitude FROM cities",
    engine
)

weather_data = []

for _, row in cities_from_db.iterrows():
    city_id = row["city_id"]
    lat = row["latitude"]
    lon = row["longitude"]

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    weather_json = response.json()

    if "list" in weather_json:
        for entry in weather_json["list"]:
            weather_data.append({
                "city_id": city_id,
                "forecast_time": datetime.fromtimestamp(entry["dt"]),
                "temperature": entry["main"]["temp"],
                "humidity": entry["main"]["humidity"],
                "wind_speed": entry["wind"]["speed"],
                "description": entry["weather"][0]["description"]
            })

weather_df = pd.DataFrame(weather_data)
weather_df.to_sql("weather", con=engine, if_exists="append", index=False)

print("✅ Weather eingefügt")