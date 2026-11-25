CREATE SCHEMA IF NOT EXISTS analytics;

CREATE OR REPLACE TABLE analytics.readings(
    site_code VARCHAR,
    species_code VARCHAR,
    timestamp TIMESTAMP,
    value DOUBLE,
    is_negative BOOLEAN,

    PRIMARY KEY (site_code,species_code,timestamp)
);

INSERT INTO analytics.readings
SELECT 
site_code,
species_code,
TRY_CAST(timestamp AS TIMESTAMP) AS timestamp,
TRY_CAST(value AS DOUBLE) AS value,
COALESCE(TRY_CAST(value AS DOUBLE) < 0, FALSE) AS is_negative
FROM staging.readings

-- Do not include rows where timestamp is null
WHERE TRY_CAST(timestamp AS TIMESTAMP) IS NOT NULL;




-- Remove this later:
SELECT * 
FROM analytics.readings
WHERE is_negative IS TRUE
LIMIT 10;