drop table if exists full_urban_centers_grid;
create table full_urban_centers_grid as
with external_reference_data_urban_centers_grid_clean as (
	select grid_fid, sum(building_area_sqkm) as building_area_sqkm
	from external_reference_data_urban_centers_grid
	group by grid_fid
)
select
	a.*
	,b.built_up_sqkm as worldcover_2020_built_up_sqkm
	,b.tree_cover_sqkm as worldcover_2020_tree_cover_sqkm
	,b.sparse_vegetation_sqkm as worldcover_2020_sparse_vegetation_sqkm
	,c.ghspop_2020
	,d.shdi as shdi_2019
	,e.vnl as vnl_2020
	,f.osm_motorway_roads_length_km + osm_other_major_roads_length_km as osm_roads_km_2022
	,g.osm_building_area_sqkm_2023
	,g.osm_building_area_sqkm_2022
	,g.osm_building_area_sqkm_2021
	,g.osm_building_area_sqkm_2020
	,g.osm_building_area_sqkm_2019
	,g.osm_building_area_sqkm_2018
	,g.osm_building_area_sqkm_2017
	,g.osm_building_area_sqkm_2016
	,g.osm_building_area_sqkm_2015
	,g.osm_building_area_sqkm_2014
	,g.osm_building_area_sqkm_2013
	,g.osm_building_area_sqkm_2012
	,g.osm_building_area_sqkm_2011
	,g.osm_building_area_sqkm_2010
	,g.osm_building_area_sqkm_2009
	,g.osm_building_area_sqkm_2008
	,h.building_area_sqkm as external_reference_building_area_sqkm
	,i.building_area_sqkm as microsoft_reference_building_area_sqkm
	,g.osm_building_area_sqkm_2023 / h.building_area_sqkm as external_reference_osm_completeness_2023
	,g.osm_building_area_sqkm_2023 / i.building_area_sqkm as microsoft_reference_osm_completeness_2023
from metadata_urban_centers_grid a
left join worldcover_2020_urban_centers_grid b on
	a.grid_fid = b.grid_fid
left join ghspop_2020_urban_centers_grid c on
	a.grid_fid = c.grid_fid
left join shdi_2019_urban_centers_grid d on
	a.grid_fid = d.grid_fid
left join vnl_2020_urban_centers_grid e on
	a.grid_fid = e.grid_fid
left join osm_roads_2022_urban_centers_grid f on
	a.grid_fid = f.grid_fid
left join osm_building_area_2023_urban_centers_grid g on
	a.grid_fid = g.grid_fid
left join external_reference_data_urban_centers_grid_clean h on
	a.grid_fid = h.grid_fid
left join microsoft_reference_data_urban_centers_grid i on
	a.grid_fid = i.grid_fid;

CREATE INDEX full_urban_centers_grid_gist
  ON full_urban_centers_grid
  USING GIST (geom);