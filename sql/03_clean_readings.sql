CREATE SCHEMA IF NOT EXIST analytics;

CREATE OR REPLACE TABLE analytics.readings(
    site_code VARCHAR,
    species_code VARCHAR,
    timestamp TIMESTAMP,
    value DOUBLE,
    is_negative BOOLIAN,

    PRIMARY KEY (site_code,species_code,timestamp)
);

INSERT INTO analytics.readings
SELECT 
site_code,
species_code,
TRY_CAST(timestamp AS TIMESTAMP) AS timestamp,
TRY_CAST(value AS DOUBLE) AS value,
COALESCE(TRY_CAST(value AS DOUBLE) < 0) AS is_negative_or_null
FROM staging.readings

-- Do not include rows where timestamp is null
WHERE TRY_CAST(timestamp AS TIMESTAMP) IS NOT NULL;



CREATE OR REPLACE analytics.sites(
    site_code VARCHAR,
    site_name VARCHAR,
    site_type VARCHAR,
    latitude DOUBLE,
    longitude DOUBLE,
    local_authority VARCHAR,
    local_authority_code VARCHAR,
    date_opened TIMESTAMP,
    date_closed TIMESTAMP
)



SELECT * FROM staging.sites
LIMIT 10;