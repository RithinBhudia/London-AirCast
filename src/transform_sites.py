from pathlib import Path
import pandas as pd
import json
import requests

sites = ["MY1", "BG1"]
species = "NO2"


def get_sites():
    with open("data/raw/sites.json", "r") as file:
        data = json.load(file)

    data_sites_site = data["Sites"]["Site"]

    rows = []

    for site in data_sites_site:
        if site["@SiteCode"] not in sites:
            continue

        rows.append({"site_code" : site["@SiteCode"],
                    "site_name" : site["@SiteName"],
                    "site_type" : site["@SiteType"],
                    "latitude" : site["@Latitude"],
                    "longitude" : site["@Longitude"],
                    "local_authority" : site["@LocalAuthorityName"],
                    "local_authority_code" : site["@LocalAuthorityCode"],
                    "date_opened" : site["@DateOpened"],
                    "date_closed" : site["@DateClosed"]})
        
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(get_sites())




