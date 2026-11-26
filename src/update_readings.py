import duckdb
from datetime import datetime, timedelta, timezone

conn = duckdb.connect("data/london_aircast.duckdb")

def get_latest_timestamps(conn):
    ans = conn.execute("""
SELECT site_code,
species_code,
MAX(timestamp) AS latest_timestamp

FROM analytics.readings
GROUP BY site_code, species_code
""").fetchall()
    
    return ans


def get_extraction_dates(conn):
    latest_readings = get_latest_timestamps(conn)

    for site_code, species_code, latest_timestamp in latest_readings:
        start_date = latest_timestamp.date() - timedelta(days = 2)

        end_date = datetime.now(timezone.utc).date()

        print()
        print(site_code, species_code)
        print("start:", start_date)
        print("end:", end_date)
        print()









if __name__ == "__main__":
    conn = duckdb.connect("data/london_aircast.duckdb")

    try:
        print(get_latest_timestamps(conn))
        print(get_extraction_dates(conn))
    finally:
        conn.close()