-- Read CSV
CREATE OR REPLACE TABLE sales AS
SELECT *
FROM read_csv_auto('data_csv/sales.csv');
-- 1) Normalize types
CREATE OR REPLACE TABLE daily_sales AS
SELECT CAST(date AS DATE) AS date,
    region,
    product,
    CAST(amount AS DOUBLE) AS amount
FROM sales;
-- 2) Aggregate: total by region
CREATE OR REPLACE TABLE agg_region AS
SELECT region,
    SUM(amount) AS total_amount
FROM daily_sales
GROUP BY region
ORDER BY region;
-- 3) Aggregate: total by product
CREATE OR REPLACE TABLE agg_product AS
SELECT product,
    SUM(amount) AS total_amount
FROM daily_sales
GROUP BY product
ORDER BY product;
-- Export results
COPY agg_region TO 'out/agg_region.parquet' (FORMAT PARQUET);
COPY agg_region TO 'out/agg_region.csv' (HEADER, DELIMITER ',');
COPY agg_product TO 'out/agg_product.parquet' (FORMAT PARQUET);
COPY agg_product TO 'out/agg_product.csv' (HEADER, DELIMITER ',');