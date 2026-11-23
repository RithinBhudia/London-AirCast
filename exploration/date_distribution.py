# The data quality check in transform_readings.py outputs:

    # site:  BG1
    # species:  NO2
    # Total rows: 720
    # Missing values: 720
    # Valid values: 0
    # invalid timestamps:  0
    # duplicates:  0

# Further investigation into the distribution of valid values:

import json
from pathlib import Path
import pandas as pd

raw_dir = Path("data/raw/readings")

for reading in raw_dir.glob("*.json"):
    with open(reading, "r") as file:
        data = json.load(file)

    raw_data = data["RawAQData"]
    print("site code: ", raw_data["@SiteCode"])
    