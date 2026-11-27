# ============================================================
# Transform Readings
# ============================================================

# ============================================================
# This file creates:
# - function get_combined_readings()
# - function data_quality_checks(df)
#
# This file uses:
# - readings
#
# This script loads every monthly JSON reading file, extratcs the
# site/species and hourly values. It rena,es the columns and combines
# the data from each site. Then runs a quality check.
# ============================================================



import json
import pandas as pd
from pathlib import Path

def get_combined_readings(path):
    raw_dir = Path(path)
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

        dataframes.append(df)

    if not dataframes:
        return pd.DataFrame(
        columns=["timestamp", "value", "site_code", "species_code"]
    )

    return pd.concat(dataframes, ignore_index = True)

def data_quality_checks(df):
    # Data quality checks
    numeric_values = pd.to_numeric(df["value"], errors = "coerce")
    timestamps = pd.to_datetime(df["timestamp"], utc = True, errors = "coerce")


    print("start date: ", timestamps.min())
    print("end date: ", timestamps.max())
    print("Total rows:", len(df))
    print("Missing values:", numeric_values.isna().sum())
    print("Valid values:", numeric_values.notna().sum())
    print("invalid timestamps: ", timestamps.isna().sum())

    # Check for duplicates
    duplicates = df.duplicated(subset = ["site_code", "species_code", "timestamp"]).sum()
    print("duplicates: ", duplicates)
    print()

# Output:
#
# start date:  2024-01-01 00:00:00+00:00
# end date:  2026-07-31 23:00:00+00:00
# Total rows: 13152
# Missing values: 5868
# Valid values: 7284
# invalid timestamps:  0
# duplicates:  0



if __name__ == "__main__":
    # historical dataframe
    historical_df = get_combined_readings(Path("data/raw/readings"))

    print("HISTORICAL READINGS")
    print(historical_df.head())
    print(historical_df.shape)
    print(data_quality_checks(historical_df))
    print()






    # incramental dataframe
    updates_df = get_combined_readings(Path("data/raw/updates"))

    print("INCRAMENTAL READINGS")
    print(updates_df.head())
    print(updates_df.shape)
    print(data_quality_checks(updates_df))

