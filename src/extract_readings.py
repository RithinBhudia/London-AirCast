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
species = ["NO2"]

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


# move function to the outside
def fetch_readings(site_code, species_code, start_date, end_date):
    url = ROOT_URL + f"/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"

    # get request to url
    response = requests.get(url, timeout = 30)

    # error:
    response.raise_for_status()
    # check file is json
    return response.json()




def main():
    for site in sites:
        for period, (start_date, end_date) in periods.items():

            for specie in species:
                response = fetch_readings(site, specie, start_date, end_date)

                file_path = readings_dir/f"{site}_{specie}_{period}.json"

                if file_path.exists():
                    print(file_path.name ,"file already exists, skipping...")
                    continue

                with open(file_path, "w") as file:
                    json.dump(response, file)

                print(f"downloaded readings for {site}")

if __name__ == "__main__":
    main()