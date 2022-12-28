UPDATE all_parameters_urban_centers b
set
  osm_building_area_sqkm_2023 = a.osm_building_area_sqkm_2023
FROM osm_building_area_urban_centers_2023 a
WHERE a.urban_center_id = b.urban_center_id;

UPDATE all_parameters_urban_centers_grid b
set
  osm_building_area_sqkm = a.osm_building_area_sqkm_2023
FROM osm_building_area_urban_centers_grid_2023 a
WHERE a.grid_fid = b.id;