-- Create table
CREATE TABLE IF NOT EXISTS energy_consumption (
    state TEXT,
    region TEXT,
    latitude REAL,
    longitude REAL,
    date DATE,
    usage REAL
);

-- Remove rows with NULL values
DELETE FROM energy_consumption
WHERE state IS NULL
   OR region IS NULL
   OR usage IS NULL;

-- Standardize state names
UPDATE energy_consumption
SET state = TRIM(state);

-- Remove negative usage values
DELETE FROM energy_consumption
WHERE usage < 0;

-- Example transformation for Tableau
-- Aggregate usage by state and date
CREATE VIEW state_daily_usage AS
SELECT
    state,
    region,
    date,
    SUM(usage) AS total_usage
FROM energy_consumption
GROUP BY state, region, date;