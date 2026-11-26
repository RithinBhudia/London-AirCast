# incramental script

import duckdb
from datetime import datetime, timedelta, timezone
from extract_readings import fetch_readings
from pathlib import Path
import json


def get_latest_timestamps(conn):
    ans = conn.execute("""
SELECT site_code,
species_code,
MAX(timestamp) AS latest_timestamp

FROM analytics.readings
GROUP BY site_code, species_code
""").fetchall()
    
    return ans


def get_extraction_dates(conn):
    latest_readings = get_latest_timestamps(conn)

    updating_periods = []

    for site_code, species_code, latest_timestamp in latest_readings:
        start_date = latest_timestamp.date() - timedelta(days = 2)

        end_date = datetime.now(timezone.utc).date() + timedelta(days = 1)

        print()
        print(site_code, species_code)
        print("start:", start_date)
        print("end:", end_date)
        print()

        updating_periods.append([site_code, species_code, start_date, end_date])

    return updating_periods





ROOT_URL = "https://api.erg.ic.ac.uk/AirQuality"

updating_readings_dir = Path("data/raw/updates")
updating_readings_dir.mkdir(parents = True, exist_ok = True)


def update_readings(conn):
    updating_readings = get_extraction_dates(conn)

    for updating_reading in updating_readings:
        response = fetch_readings(updating_reading[0], updating_reading[1],updating_reading[2],updating_reading[3])

        file_path = updating_readings_dir/f"{updating_reading[0]}_{updating_reading[1]}_{updating_reading[2]}_{updating_reading[3]}.json"

        if file_path.exists():
            print(file_path.name ,"file already exists, skipping...")
            continue

        with open(file_path, "w") as file:
            json.dump(response, file)

        print(f"downloaded readings for {updating_reading[0]}_{updating_reading[1]}_{updating_reading[2]}_{updating_reading[3]}.json")




if __name__ == "__main__":
    conn = duckdb.connect("data/london_aircast.duckdb")

    try:
        update_readings(conn)
    finally:
        conn.close()