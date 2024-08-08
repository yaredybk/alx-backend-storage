-- Write a SQL script that lists all bands with Glam rock as their main style, ranked by their longevity
-- 
-- Requirements:
-- 
-- Import this table dump: metal_bands.sql.zip
-- Column names must be: band_name and lifespan (in years until 2022 - please use 2022 instead of YEAR(CURDATE()))
-- You should use attributes formed and split for computing the lifespan
-- Your script can be executed on any database
CREATE TEMPORARY TABLE `life` AS
SELECT band_name,
  (IFNULL(split, '2022') - formed) AS lifespan
FROM metal_bands
where style LIKE '%Glam rock%';
SELECT *
FROM `life`
ORDER BY lifespan desc;