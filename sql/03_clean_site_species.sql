


CREATE OR REPLACE TABLE analytics.site_species(
    site_code VARCHAR,
    species_code VARCHAR,
    date_measurement_start TIMESTAMP,
    date_measurement_end TIMESTAMP,

    PRIMARY KEY (site_code, species_code, date_measurement_start)
);

INSERT INTO analytics.site_species(
    site_code,
    species_code,
    date_measurement_start,
    date_measurement_end
)
SELECT
    site_code,
    species_code,
    TRY_CAST(date_measurement_start AS TIMESTAMP),
    TRY_CAST(date_measurement_end AS TIMESTAMP)
FROM staging.site_species;

SELECT * 
FROM analytics.site_species;