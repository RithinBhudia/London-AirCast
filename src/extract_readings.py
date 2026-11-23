from pathlib import Path
import json
import requests

sites = ["MY1", "BG1", "HR1"]
species = "NO2"

start_date = "2026-01-01"
end_date = "2026-01-31"

ROOT_URL = "https://api.erg.ic.ac.uk/AirQuality"

# create readings folder in data
readings_dir = Path("data/raw/readings")
readings_dir.mkdir(parents = True, exist_ok = True)

for site in sites:
    url = ROOT_URL + f"/Data/SiteSpecies/SiteCode={site}/SpeciesCode={species}/StartDate={start_date}/EndDate={end_date}/Json"

    # get request to url
    response = requests.get(url, timeout = 30)

    # error:
    response.raise_for_status()

    file_path = readings_dir/f"{site}_{species}_2026-01.json"
    
    with open(file_path, "w") as file:
        file.write(response.text)

    print(f"downloaded readings for {site}")