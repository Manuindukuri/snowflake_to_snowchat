
USE ROLE HOL_ROLE;
USE WAREHOUSE HOL_WH1;

Select * From COVID19_DATA.PUBLIC.NYC_HEALTH_TESTS Limit 100;

-- Step 2: Filter out null values and create a new table
-- Step 1: Create a new table
CREATE TABLE HOL_DB1.COVID_NYC.CLEANED_NYC_HEALTH_TESTS AS
SELECT *
FROM COVID19_DATA.PUBLIC.NYC_HEALTH_TESTS
WHERE TOTAL_COVID_TESTS IS NOT NULL
  AND PERCENT_POSITIVE IS NOT NULL;
-- Add similar conditions for other columns as needed

-- Step 2: Insert cleaned data into the new table
INSERT INTO HOL_DB1.COVID_NYC.CLEANED_NYC_HEALTH_TESTS
SELECT *
FROM COVID19_DATA.PUBLIC.NYC_HEALTH_TESTS
WHERE TOTAL_COVID_TESTS IS NOT NULL
  AND PERCENT_POSITIVE IS NOT NULL;


-- Add similar conditions for other columns as needed

  -- Add similar conditions for other columns as needed;

-- Select * from HOL_DB1.COVID_NYC.CLEANED_NYC_HEALTH_TESTS limit 100;

Select * from HOL_DB1.COVID_NYC.CLEANED_NYC_HEALTH_TESTS limit 10000;