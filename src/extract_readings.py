# ============================================================
# Extract Readings
# ============================================================

# ============================================================
# This file creates:
# - monthly BG1/MY1 NO2 JSON files stored in data/reading/
#
# This file uses:
# - Live LAQN API
#
# This script downloads monthly hourly NO2 readings for BG1 and MY1
# from Janurary 2024 through to the current month.
# ============================================================
from pathlib import Path
import json
import requests
from datetime import date

# removed HR1 due to monitoring station inactivity
sites = ["MY1", "BG1"]
species = "NO2"

start_year = 2024
end_year = 2026

periods = {}

for year in range(start_year, end_year + 1):
    for month in range(1,13):
        start = date(year, month, 1)

        if start > date.today():
            continue
        if month == 12:
            end = date(year+1, 1, 1)

        else:
            end = date(year, month+1, 1)

        periods[start.strftime("%Y-%m")] = (str(start),str(end))




ROOT_URL = "https://api.erg.ic.ac.uk/AirQuality"

# create readings folder in data
readings_dir = Path("data/raw/readings")
readings_dir.mkdir(parents = True, exist_ok = True)

for site in sites:
    for period, (start_date, end_date) in periods.items():
        url = ROOT_URL + f"/Data/SiteSpecies/SiteCode={site}/SpeciesCode={species}/StartDate={start_date}/EndDate={end_date}/Json"

        # get request to url
        response = requests.get(url, timeout = 30)

        # error:
        response.raise_for_status()
        # check file is json
        response.json()

        file_path = readings_dir/f"{site}_{species}_{period}.json"

        if file_path.exists():
            print(file_path.name ,"file already exists, skipping...")
            continue
        
        with open(file_path, "w") as file:
            file.write(response.text)

        print(f"downloaded readings for {site}")