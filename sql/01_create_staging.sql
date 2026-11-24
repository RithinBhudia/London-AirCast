CREATE SCHEMA IF NOT EXISTS staging;

CREATE OR REPLACE TABLE staging.readings (
    site_code VARCHAR,
    species_code VARCHAR,
    timestamp VARCHAR,
    value VARCHAR
);

CREATE OR REPLACE TABLE staging.sites(
    site_code VARCHAR,
    site_name VARCHAR,
    site_type VARCHAR,
    latitude VARCHAR,
    longitude VARCHAR,
    local_authority VARCHAR,
    local_authority_code VARCHAR,
    date_opened VARCHAR,
    date_closed VARCHAR
);

SELECT * 
FROM staging.readings
LIMIT 10;

