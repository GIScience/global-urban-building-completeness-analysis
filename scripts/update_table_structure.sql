UPDATE all_parameters_urban_centers
SET osm_building_area_sqkm_2022 = osm_building_area_sqkm;

ALTER TABLE all_parameters_urban_centers
  DROP COLUMN osm_building_area_sqkm;

ALTER TABLE all_parameters_urban_centers_grid
  ADD COLUMN microsoft_building_area_sqkm numeric,
  ADD COLUMN microsoft_building_count int8;
