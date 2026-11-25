




-- Count number of rows
SELECT COUNT(*)
FROM staging.site_species;
/*
- Should the number of sites you include.
*/


-- Check duplicate site and species combination
SELECT site_code, species_code, 
COUNT(*) AS occurances
FROM staging.site_species
GROUP BY site_code, species_code
HAVING occurances > 1;
/*
- I have no rows for my site choices as of now.
- A monitoring station can theoretically start, stop then restart.
- I cannot disprove that this is possible so choose primary key accordingly
*/


-- Check invalid date measurements
SELECT
COUNT(*) AS occurances

FROM staging.site_species
WHERE(
TRY_CAST(date_measurement_start AS DATETIME) IS NULL AND
NULLIF(TRIM(date_measurement_start), '') IS NOT NULL)

OR (TRY_CAST(date_measurement_end AS DATETIME) IS NULL
AND NULLIF(TRIM(date_measurement_end), '') IS NOT NULL
);
/*
- Should be zero
*/
