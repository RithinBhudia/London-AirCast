-- ============================================================
-- Create Staging
-- ============================================================

-- ============================================================
-- This file creates:
-- - table:              taging.readings
--   contains columns:   site_code, species_code, timestamp, value
--
-- - table:              staging.sites
--   contains columns:   site_code, site_name, site_type,
--                       latitude, longitude,
--                       local_authority, local authority_code,
--                       date_opened, date_closed
--
-- ============================================================

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
    date_closed VARCHAR,
);

CREATE TABLE IF NOT EXISTS staging.site_species (
    site_code VARCHAR,
    species_code VARCHAR,
    date_measurement_start VARCHAR,
    date_measurement_end VARCHAR
);

