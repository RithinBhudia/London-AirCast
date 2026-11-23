import json
from pathlib import Path

raw_dir = Path("data/raw")

for name in ["sites", "site_species", "species", "readings"]:
    with open(raw_dir / f"{name}.json", "r") as file:
        data = json.load(file)

    print("top level keys:", list(data.keys()))
    print(json.dumps(data, indent = 3)[:3000])

# sites: Information about london monitoring stations - including their locations.
# site_species: Information about which pollutants are measured at each station.
# species: Information about each pollutant - things like name and code
# readings: Hourly pollutant concentration measurents at a given monitoring station over a given period of time