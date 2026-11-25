-- ============================================================
-- Profile Readings
-- ============================================================

-- ============================================================
-- This file Profiles:
-- - row count, missing values, duplicate timestamps, zero/negative readings,
--   and monthly completeness.
--
-- ============================================================


-- Row counts for each site
SELECT site_code AS "site code", COUNT(*) AS "record count",
COUNT(DISTINCT (site_code, species_code, timestamp, value)) AS "distinct record count",
COUNT(*) FILTER(WHERE value IS NULL OR TRIM(value)= '') AS "missing value count",
COUNT(*) FILTER(WHERE timestamp IS NULL OR TRIM(timestamp) = '') AS "missing timestamp count"
FROM staging.readings
GROUP BY site_code;
/*
Data quality findings:
- Both sites contain 25404 records.
- No duplicate records were identified.
- No missing timestamps were identified.
- BG1 has    % missing measurement values.
- MY1 has    % missing measurement values.

What I will do next:
- Investigate missing values by pollutant and month.
- Assess whether BG1 provides sufficient data for meaningful historical analysis.
- Consider replacing BG1 with a site offering more complete monitoring data.
*/

SELECT DATE_TRUNC('month', CAST(timestamp AS TIMESTAMP)) AS month,
COUNT(*) FILTER(WHERE (value IS NULL OR TRIM(value) = '') AND (site_code = 'MY1')) AS "missing MY1 value count",
COUNT(*) FILTER(WHERE(site_code = 'MY1')) AS "total MY1 value spaces",
ROUND(100*("missing MY1 value count")/("total MY1 value spaces"),2) AS "MY1 missing %",

COUNT(*) FILTER(WHERE (value IS NULL OR TRIM(value) = '') AND (site_code = 'BG1')) AS "missing BG1 value count",
COUNT(*) FILTER(WHERE(site_code = 'BG1')) AS "total BG1 value spaces",
ROUND(100*("missing BG1 value count")/("total BG1 value spaces"),2) AS "BG1 missing %"

FROM staging.readings

GROUP BY month
ORDER BY MONTH;
/*
Data quality findings:
- BG1 has inconsistent historical NO2 coverage, with 100% missing values from September 2025 onwards.
- MY1 has much better coverage, although some months contain significant missing data.
- BG1 is unsuitable for recent NO2 analysis.
- Investigate alternative monitoring sites with more consistent measurement coverage.

Decision:
- Retain BG1 in staging for historical completeness, but exclude periods with insufficient coverage 
from downstream analysis.
- Distinguish missing measurements from zero measurements.
- Potential for adding a (monthly) completeness threshold for later visualisations
*/



-- Check for invalid values
SELECT site_code,
COUNT(*) FILTER( TRY_CAST(value AS DOUBLE) = 0 ) AS zero_values,
COUNT(*) FILTER( TRY_CAST(value AS DOUBLE) < 0 ) AS negative_values,

COUNT(*) FILTER(
    WHERE value IS NOT NULL
    AND TRIM(value) != ''
    AND TRY_CAST(value AS DOUBLE) IS NULL
) AS invalid_values

FROM staging.readings
GROUP BY site_code;
/*
Findings:
- MY1 contains 5 zero values and 46 negative values.
- BG1 contains no zero or negative values.
- Neither site has invalid non empty values.

Decision:
- Retain zero values unless confirmed to represent missing data.
- Investigate negative values before deciding whether to exclude them from analysis. (could be caused by tool calibration)
- Keep the original measurements unchanged in staging.
*/


-- Check how negative the values are; tools may be offset slightly towards the negative
SELECT COUNT(*) AS total,
MAX(TRY_CAST(value AS DOUBLE)) AS maximum_value,
MIN(TRY_CAST(value AS DOUBLE)) AS minimum_value,
ROUND(AVG(TRY_CAST(value AS DOUBLE)),2) AS average

FROM staging.readings
WHERE TRY_CAST(value AS DOUBLE) < 0
GROUP BY site_code;
/*
Findings:
- MY1 has 46 negative NO2 readings, ranging from -5.2 to -0.1, with an average of -1.92
- Negative concentrations are not meaningful. It may result from measurement noise or instrument calibration.

Decision:
- Retain original values in staging.
- Flag negative readings for further investigation.
- Consider excluding them from analytical calculations...
*/



-- Check duplicate timestamps
SELECT site_code, species_code,
timestamp,
COUNT(*) AS occurences

FROM staging.readings
GROUP BY site_code, species_code, timestamp
HAVING COUNT(*) >1;
/*
findings:
- No duplicates found
*/

-- Check timestamps are in the correct format
SELECT COUNT(timestamp) AS invalid_timestamp_count
FROM staging.readings
WHERE TRY_CAST(timestamp AS TIMESTAMP) IS NULL
AND timestamp IS NOT NULL;
/*
findings:
- No invalid timestamp formats 
*/




-- Test for load.py files
.maxwidth 200
SELECT * FROM staging.sites
LIMIT 10;

SELECT * FROM staging.site_species
LIMIT 10;


-- ====================================
-- POST CLEANING VALIDATION
-- ====================================

-- Check row count
SELECT COUNT(*) AS count
FROM analytics.readings;
/*
- Should be the same as in staging
*/


-- Check types
DESCRIBE analytics.readings;


-- Preview of cleaned data
SELECT * 
FROM analytics.readings
LIMIT 10;