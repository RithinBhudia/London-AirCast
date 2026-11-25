from pathlib import Path
from transform_site_species import get_site_species
import pandas as pd
import duckdb

site_species = get_site_species()

conn = duckdb.connect("data/london_aircast.duckdb")

conn.register("duckdb_site_species", site_species)

conn.begin()

try:
    conn.execute("DELETE FROM staging.site_species")

    conn.execute("""
INSERT INTO staging.site_species( 
site_code,
species_code,
date_measurement_start,
date_measurement_end
)

SELECT
site_code,
species_code,
date_measurement_start,
date_measurement_end

FROM duckdb_site_species
""")

    conn.commit()

except Exception:
    conn.rollback()
    raise

row_nums = conn.execute("""
SELECT COUNT(*)
FROM staging.site_species
""").fetchone()

print("Row number:", row_nums[0])

conn.close()