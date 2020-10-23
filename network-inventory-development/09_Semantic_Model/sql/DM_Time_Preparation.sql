INVALIDATE METADATA

DROP TABLE dm_tiempo_hv;

set hivevar:start_date=2019-01-01;
set hivevar:days=3650;
set hivevar:table_name=dm_tiempo_hv;
set hive.support.sql11.reserved.keywords=false;

CREATE TABLE IF NOT EXISTS ${table_name} AS
WITH dates AS (
    SELECT date_add("${start_date}", a.pos) AS `date`
    FROM (SELECT posexplode(split(repeat(",", ${days}), ","))) a
),
dates_expanded AS (
  SELECT
    `date`,
    year(`date`) AS year,
    month(`date`) AS month,
    day(`date`) AS day,
    date_format(`date`, 'u') AS day_of_week 
  FROM dates
)
SELECT
    `date`,
    year,
    cast(month(`date`)/4 + 1 AS BIGINT) AS quarter,
    month,
    date_format(`date`, 'W') AS week_of_month, 
    date_format(`date`, 'w') AS week_of_year, 
    day,
    day_of_week,
    date_format(`date`, 'EEE') AS day_of_week_s, 
    date_format(`date`, 'D') AS day_of_year 
FROM dates_expanded
SORT BY `date`
;

SELECT *
FROM dm_tiempo_hv
ORDER BY `date`