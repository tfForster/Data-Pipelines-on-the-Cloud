import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from db_config import engine

cities_list = ["Berlin", "Hamburg", "Munich"]
headers = {"User-Agent": "Mozilla/5.0"}

def dms_to_decimal(dms):
    pattern = r"(\d+)°(\d+)?′?(\d+)?″?([NSEW])"
    match = re.match(pattern, dms)
    if not match:
        return None
    deg, min, sec, dir = match.groups()
    deg = int(deg)
    min = int(min) if min else 0
    sec = int(sec) if sec else 0
    dec = deg + min/60 + sec/3600
    if dir in ['S','W']:
        dec = -dec
    return dec

country_mapping = {"Germany": "DE"}

data = []

for city in cities_list:
    url = f"https://en.wikipedia.org/wiki/{city}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    infobox = soup.find("table", class_=lambda x: x and "infobox" in x)
    rows = infobox.find_all("tr")

    # Country
    country_name = None
    for row in rows:
        if "Country" in row.text:
            td = row.find("td")
            if td:
                country_name = td.text.strip()
                break
    country_code = country_mapping.get(country_name, "DE")

    # Coordinates
    latitude_dms = soup.find("span", class_="latitude").text
    longitude_dms = soup.find("span", class_="longitude").text
    latitude = dms_to_decimal(latitude_dms)
    longitude = dms_to_decimal(longitude_dms)

    data.append({
        "city_name": city,
        "country_code": country_code,
        "latitude": latitude,
        "longitude": longitude,
        "latitude_dms": latitude_dms,
        "longitude_dms": longitude_dms
    })

cities_df = pd.DataFrame(data)
cities_df.to_sql("cities", con=engine, if_exists="append", index=False)

print("✅ Cities eingefügt")
