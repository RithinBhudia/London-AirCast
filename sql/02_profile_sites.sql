




-- Total number of sites
SELECT COUNT(*) AS total_sites
FROM staging.sites;
/*
- Should the number of sites you include.
*/


-- Check each site_code appears only once
SELECT site_code, COUNT(*) AS occurances

FROM staging.sites
GROUP BY site_code
HAVING occurances > 1;
/*
- Should ideally be Zero.
*/


-- Check missing/invalid coordinates
.maxwidth 200
SELECT COUNT(*) AS "latitude or longitude is null count"
FROM staging.sites
WHERE TRY_CAST(latitude AS DOUBLE) IS NULL
OR TRY_CAST(longitude AS DOUBLE) IS NULL;/*
- Should ideally be Zero.
*/

-- Check missing site codes
SELECT COUNT(*)  AS "empty or null site_code count"
FROm staging.sites
WHERE TRIM(site_code) = ''
OR site_code IS NUlL;




-- ====================================
-- POST CLEANING VALIDATION
-- ====================================

-- Check row count
SELECT COUNT(*) AS count
FROM analytics.sites;
/*
- Should be the same as in staging
*/


-- Check types
DESCRIBE analytics.sites;


-- Check for invalid or missing coordinates
SELECT *
FROM analytics.sites
WHERE latitude IS NULL
OR longitude IS NULL
OR latitude NOT BETWEEN -90 AND 90
OR longitude NOT BETWEEN -180 AND 180;
/*
- Should show no rows
*/


-- Check for invalid operating periods
SELECT *
FROM analytics.sites
WHERE date_closed < date_opened;
/*
- Should show no rows
*/


-- Preview of cleaned data
SELECT * 
FROM analytics.sites
LIMIT 10;