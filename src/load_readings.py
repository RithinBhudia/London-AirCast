# ============================================================
# Load Staging
# ============================================================

# ============================================================
# This file creates:
# - sites.json, site_species.json, species,json
#
# This file uses:
# - transform_readings.py
# - 01_create_staging.sql
#
# This script begins the load stage. It transforms all the readings,
# executes the staging SQL and replaces the existing staging.readings.
# ============================================================

import duckdb
from transform_readings import get_combined_readings
from pathlib import Path

combined_readings = get_combined_readings(Path("data/raw/readings"))

conn = duckdb.connect("data/london_aircast.duckdb")

sql = Path("sql/01_create_staging.sql").read_text()
conn.execute(sql)




print(conn.execute("SHOW ALL TABLES").fetchdf())


conn.register("duckdb_combined_readings", combined_readings)

conn.begin()
try:
    # For rerun of script
    conn.execute("DELETE FROM staging.readings")

    conn.execute("""
    INSERT INTO staging.readings(
    site_code,
    species_code,
    timestamp,
    value
    )

    SELECT site_code,
    species_code,
    timestamp,
    value
    FROM duckdb_combined_readings
    """)
    conn.commit()

except Exception:
    conn.rollback()
    raise

num_rows = conn.execute("""
SELECT COUNT(*)
FROM staging.readings
""").fetchone()

print("Rows loaded:", num_rows[0])

conn.close()