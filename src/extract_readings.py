from pathlib import Path
import json
import requests

# removes HR1 due to monitoring station inactivity
sites = ["MY1", "BG1"]
species = "NO2"

start_date = "2026-01-01"
end_date = "2026-01-31"

periods = {"2024-01": ("2024-01-01", "2024-02-01"),
           "2025-01": ("2025-01-01", "2025-02-01"),
           "2026-01": ("2026-01-01", "2026-02-01"),
           "2026-02": ("2026-02-01", "2026-03-01"),
           "2026-03": ("2026-03-01", "2026-04-01"),
           "2026-04": ("2026-04-01", "2026-05-01"),
           "2026-05": ("2026-05-01", "2026-06-01"),
           "2026-06": ("2026-06-01", "2026-07-01"),
           "2026-07": ("2026-07-01", "2026-08-01")}

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