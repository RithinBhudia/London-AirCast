import requests
import json
from pathlib import Path

ROOT_URL = "https://api.erg.ic.ac.uk/AirQuality"

endpoints = {"sites": "/Information/MonitoringSites/GroupName=London/Json",
             "site_species": "/Information/MonitoringSiteSpecies/GroupName=London/Json",
             "species": "/Information/Species/Json"}

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