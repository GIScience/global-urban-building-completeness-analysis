drop table if exists full_urban_centers_grid;
create table full_urban_centers_grid as
with geowiki_selection_urban_centers as (
    select urban_center_id, 1  as geowiki
    from geowiki_selection
    group by urban_center_id
)
select
	a.*
	,b.built_up_sqkm as worldcover_2020_built_up_sqkm
	,b.tree_cover_sqkm as worldcover_2020_tree_cover_sqkm
	,b.sparse_vegetation_sqkm as worldcover_2020_sparse_vegetation_sqkm
	,c.ghspop_2020
	,d.shdi as shdi_2019
	,e.vnl as vnl_2020
	,f.osm_road_length_km_2023
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
	,h.external_reference_building_area_sqkm
	,i.microsoft_building_area_sqkm
	,case
		when h.external_reference_building_area_sqkm is null then i.microsoft_building_area_sqkm
		else h.external_reference_building_area_sqkm
	end reference_building_area_sqkm
	,case
		when h.external_reference_building_area_sqkm is null and j.geowiki=1 then i.microsoft_building_area_sqkm
		else h.external_reference_building_area_sqkm
	end reference_building_area_sqkm_strict
	,case
		when h.external_reference_building_area_sqkm is null then g.osm_building_area_sqkm_2023 / i.microsoft_building_area_sqkm
		else g.osm_building_area_sqkm_2023 / h.external_reference_building_area_sqkm
	end as reference_osm_completeness
	,case
		when h.external_reference_building_area_sqkm is null and j.geowiki=1 then g.osm_building_area_sqkm_2023 / i.microsoft_building_area_sqkm
		else g.osm_building_area_sqkm_2023 / h.external_reference_building_area_sqkm
	end as reference_osm_completeness_strict
	,j.geowiki
from metadata_urban_centers_grid a
left join worldcover_2020_urban_centers_grid b on
	a.grid_fid = b.grid_fid
left join ghspop_2020_urban_centers_grid c on
	a.grid_fid = c.grid_fid
left join shdi_2019_urban_centers_grid d on
	a.grid_fid = d.grid_fid
left join vnl_2020_urban_centers_grid e on
	a.grid_fid = e.grid_fid
left join osm_road_length_2023_urban_centers_grid f on
	a.grid_fid = f.grid_fid
left join osm_building_area_2023_urban_centers_grid g on
	a.grid_fid = g.grid_fid
left join external_reference_data_urban_centers_grid h on
	a.grid_fid = h.grid_fid
left join microsoft_buildings_urban_centers_grid i on
	a.grid_fid = i.grid_fid
left join geowiki_selection_urban_centers j on
	a.urban_center_id = j.urban_center_id
order by urban_center_id, grid_fid;

CREATE INDEX full_urban_centers_grid_gist
  ON full_urban_centers_grid
  USING GIST (geom);