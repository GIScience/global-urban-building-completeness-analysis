UPDATE all_parameters_urban_centers b
set
  osm_building_area_sqkm_2022 = a.osm_building_area_sqkm_2022,
  osm_building_area_sqkm_2021 = a.osm_building_area_sqkm_2021,
  osm_building_area_sqkm_2020 = a.osm_building_area_sqkm_2020,
  osm_building_area_sqkm_2019 = a.osm_building_area_sqkm_2019,
  osm_building_area_sqkm_2018 = a.osm_building_area_sqkm_2018,
  osm_building_area_sqkm_2017 = a.osm_building_area_sqkm_2017,
  osm_building_area_sqkm_2016 = a.osm_building_area_sqkm_2016,
  osm_building_area_sqkm_2015 = a.osm_building_area_sqkm_2015,
  osm_building_area_sqkm_2014 = a.osm_building_area_sqkm_2014,
  osm_building_area_sqkm_2013 = a.osm_building_area_sqkm_2013,
  osm_building_area_sqkm_2012 = a.osm_building_area_sqkm_2012,
  osm_building_area_sqkm_2011 = a.osm_building_area_sqkm_2011,
  osm_building_area_sqkm_2010 = a.osm_building_area_sqkm_2010,
  osm_building_area_sqkm_2009 = a.osm_building_area_sqkm_2009,
  osm_building_area_sqkm_2008 = a.osm_building_area_sqkm_2008
FROM osm_building_area_urban_centers_updated a
WHERE a.urban_center_id = b.urban_center_id;