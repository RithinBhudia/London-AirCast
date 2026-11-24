# ============================================================
# Explore API
# ============================================================

# ============================================================
# This file creates:
# - sites.json, site_species.json, species_json   stored in data/readings/
#
# This file uses:
# - Live LAQN API
#
# This script collects data from the LAQN API endpoints.
# ============================================================

import requests
import json
from pathlib import Path

ROOT_URL = "https://api.erg.ic.ac.uk/AirQuality"

endpoints = {"sites": "/Information/MonitoringSites/GroupName=London/Json",
             "site_species": "/Information/MonitoringSiteSpecies/GroupName=London/Json",
             "species": "/Information/Species/Json",
             "example_reading": "/Data/SiteSpecies/SiteCode=BG1/SpeciesCode=NO2/StartDate=2024-01-01/EndDate=2024-01-30/Json"}

raw_dir = Path("data/raw")

# Create folder if not exist
raw_dir.mkdir(parents = True, exist_ok = True)


for name, endpoint in endpoints.items():
    # combined url
    url = ROOT_URL + endpoint

    # get request to url
    response = requests.get(url, timeout = 30)

    # errors:
    response.raise_for_status()

    # saves the python data as json file 
    with open(raw_dir / f"{name}.json", "w") as file:
        file.write(response.text)