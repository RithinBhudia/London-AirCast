

CREATE OR REPLACE TABLE analytics.sites (
    site_code VARCHAR,
    site_name VARCHAR,
    site_type VARCHAR,
    latitude DOUBLE,
    longitude DOUBLE,
    local_authority VARCHAR,
    local_authority_code VARCHAR,
    date_opened TIMESTAMP,
    date_closed TIMESTAMP,

    PRIMARY KEY (site_code)
);

INSERT INTO analytics.sites(
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
    TRY_CAST(latitude AS DOUBLE),
    TRY_CAST(longitude AS DOUBLE),
    local_authority,
    local_authority_code,
    TRY_CAST(date_opened AS TIMESTAMP),
    TRY_CAST(date_closed AS TIMESTAMP)
FROM staging.sites;

.maxwidth 200
SELECT * FROM analytics.sites;