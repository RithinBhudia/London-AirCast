import duckdb
from pathlib import Path
from transform_sites import get_sites

sites = get_sites()

conn = duckdb.connect("data/london_aircast.duckdb")

conn.register("duckdb_sites", sites)
conn.begin()

try:
    conn.execute("DELETE FROM staging.sites")

    conn.execute("""
INSERT INTO staging.sites(
site_code,
site_name,
site_type,
latitude,
longitude,
local_authority,
local_authority_code,
date_opened,
date_closed
)

SELECT
site_code,
site_name,
site_type,
latitude,
longitude,
local_authority,
local_authority_code,
date_opened,
date_closed

FROM duckdb_sites
""")
    conn.commit()

    
except Exception:
    conn.rollback()
    raise

num_rows = conn.execute("""
SELECT COUNT(*)
FROM staging.sites
""").fetchone()

print("Rows loaded:", num_rows)

conn.close()