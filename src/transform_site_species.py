import json
from pathlib import Path
import pandas as pd

sites = ["MY1", "BG1"]
species = ["NO2"]


def get_site_species():

    with open("data/raw/site_species.json", "r") as file:
        data = json.load(file)

    data_species = data["Sites"]["Site"]

    rows = []

    for site in data_species:
        if site["@SiteCode"] not in sites:
            continue
        
        for specie in site["Species"]:
            if specie["@SpeciesCode"] not in species:
                continue

            rows.append({"site_code" : site["@SiteCode"],
                         "species_code" : specie["@SpeciesCode"],
                         "date_measurement_start" : specie["@DateMeasurementStarted"],
                         "date_measurement_end" : specie["@DateMeasurementFinished"]})

    return pd.DataFrame(rows)

if __name__ == "__main__":
    print(get_site_species())