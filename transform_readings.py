import json
import pandas as pd

with open("data/raw/readings/HR1_NO2_2026-01.json", "r") as file:
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

# Testing if there are any values not Nan
print(df[["timestamp", "value"]].head(50))
print(df["value"].isna().sum())
print(raw_data["Data"][:5])


# convert timestamps to python time
df["timestamp"] = pd.to_datetime(df["timestamp"], utc = True)

# convert value to numeric
df["value"] = pd.to_numeric(df["value"], errors = "coerce")

print(df.head())
print(df.dtypes)

# Testing if there are any values not Nan
print("Total rows:", len(df))
print("Missing values:", df["value"].isna().sum())
print("Valid values:", df["value"].notna().sum())


