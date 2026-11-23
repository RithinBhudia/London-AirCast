import json
import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw/readings")

dataframes = []

for file_path in raw_dir.glob("*.json"):
    
    with open(file_path, "r") as file:
        data = json.load(file)

    raw_data = data["RawAQData"]

    site_code = raw_data["@SiteCode"]
    species_code = raw_data["@SpeciesCode"]

    readings = raw_data["Data"]

    # Make a data frame with columns: @MeasurementDateGMT, @Value
    df = pd.DataFrame(readings)

    # Rename columns
    df = df.rename(columns={"@MeasurementDateGMT" : "timestamp",
                        "@Value" : "value"})

    # To df add columns: site_code, species_code
    df["site_code"] = site_code
    df["species_code"] = species_code

    # convert timestamps to python time
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc = True)

    # convert value to numeric
    df["value"] = pd.to_numeric(df["value"], errors = "coerce")

    # print(df.head())
    # print(df.dtypes)


    # =======================================================================================
    # Data quality checks
    print("site: ", site_code)
    print("start date: ", df["timestamp"].min())
    print("end date: ", df["timestamp"].max())
    print("species: ", species_code)
    print("Total rows:", len(df))
    print("Missing values:", df["value"].isna().sum())
    print("Valid values:", df["value"].notna().sum())
    print("invalid timestamps: ", df["timestamp"].isna().sum())

    # Check for duplicates
    duplicates = df.duplicated(subset = ["site_code", "species_code", "timestamp"]).sum()
    print("duplicates: ", duplicates)
    print()


    dataframes.append(df)

combined_readings = pd.concat(dataframes, ignore_index = True)

print(combined_readings.head())
print(combined_readings.shape)