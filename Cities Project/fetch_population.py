import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from db_config import engine

headers = {"User-Agent": "Mozilla/5.0"}
today_date = datetime.now().date()

cities_from_db = pd.read_sql(
    "SELECT city_id, city_name FROM cities",
    engine
)

population_data = []

for _, row in cities_from_db.iterrows():
    city_id = row["city_id"]
    city_name = row["city_name"]

    url = f"https://en.wikipedia.org/wiki/{city_name}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    infobox = soup.find("table", class_=lambda x: x and "infobox" in x)
    rows = infobox.find_all("tr")

    population_value = None

    for r in rows:
        header = r.find("th")
        if header and "Population" in header.text:
            next_row = r.find_next_sibling("tr")
            if next_row:
                td = next_row.find("td", class_="infobox-data")
                if td:
                    pop_text = re.sub(r"\[.*?\]", "", td.text.strip())
                    pop_number = re.search(r"\d[\d,]*", pop_text)
                    if pop_number:
                        population_value = int(pop_number.group().replace(",", ""))
            break

    population_data.append({
        "city_id": city_id,
        "population": population_value,
        "timestamp_population": today_date
    })

pop_df = pd.DataFrame(population_data)
pop_df.to_sql("populations", con=engine, if_exists="append", index=False)

print("✅ Population eingefügt")