# Originally I had included 'Harrow - Stanmore', code 'BG1'. I did this because this is where I live.

# In extract_readings, I transformed the data into a pandas dataframe and 
# noticed all the values were NaN for Janurary 2026.

# This lead me to investigating the operating periods of the monitoring sites I had selected.

# Findings:
# - BG1 (Rush Green): Appears to be operational to date.
# - MY1 (Marylebone Road): Appears to be operational to date.
# - HR1 (Harrow - Stanmore): Monitoring ended in August 2023 and is currently inactive.

# Decision: 
# Exclude HR1 from the ongoing incremental extraction because it
# no longer provides current readings.

from pathlib import Path
import json


with open("data/raw/sites.json", "r") as file:
    data = json.load(file)

sites = data["Sites"]["Site"]

for site in sites:
    if site["@SiteCode"] in ["BG1", "HR1", "MY1"]:
        print("site code: ", site["@SiteCode"])
        print("site name:", site["@SiteName"])
        print("date opened: ", repr(site.get("@DateOpened")))
        print("date closed: ", repr(site.get("@DateClosed")))
        print()
