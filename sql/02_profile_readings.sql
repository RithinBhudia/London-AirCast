-- Profileing


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

