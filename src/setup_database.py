# ============================================================
# Setup Database
# ============================================================

# ============================================================
# This file creates:
# - london_aircast.duckdb
# - staging and analytics schemas
#
# This file uses:
# - 
#
# This script creates the DuckDB database and creates the analytics
# and staging schemas.
# ============================================================

import duckdb
from pathlib import Path

db_path = Path("data/london_aircast.duckdb")
db_path.parent.mkdir(parents = True, exist_ok = True)

conn = duckdb.connect(str(db_path))


# create schemas:
conn.execute("CREATE SCHEMA IF NOT EXISTS staging")
conn.execute("CREATE SCHEMA IF NOT EXISTS analytics")

conn.close()