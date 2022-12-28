drop table if exists reference_data_urban_centers_grid;
create table reference_data_urban_centers_grid as (
with agg_reference_data as (
	select
		grid_fid
		,max(building_area_sqkm) as building_area_sqkm
		,max(building_count) as building_count
		,max(
		    CASE WHEN source = 'microsoft' THEN building_area_sqkm ELSE NULL END
		) as microsoft_building_area_sqkm
		,max(
		    CASE WHEN source = 'microsoft' THEN building_count ELSE NULL END
		) as microsoft_building_count
	from reference_data_urban_centers_grid_raw
	where source != 'google'
	group by grid_fid
)
select
	a.id as grid_fid
	,a.urban_center_id
	,a.name_main
	,a.iso_a3
	,a.country_id
	,b.building_area_sqkm as reference_building_area_sqkm
	,b.building_count as reference_building_count
	,b.microsoft_building_area_sqkm
	,b.microsoft_building_count
	,a.geom
from all_parameters_urban_centers_grid a
left join agg_reference_data b on
    a.id = b.grid_fid
where b.building_area_sqkm is not null
);
-- update the table which is used by the ML model
UPDATE all_parameters_urban_centers_grid b
set
  reference_building_area_sqkm = a.reference_building_area_sqkm,
  reference_building_count = a.reference_building_count,
  microsoft_building_area_sqkm = a.microsoft_building_area_sqkm,
  microsoft_building_count = a.microsoft_building_count
FROM reference_data_urban_centers_grid a
WHERE a.grid_fid = b.id;
-- update the table which is used by the ML model
UPDATE all_parameters_urban_centers b
set
  reference_building_area_sqkm = a.reference_building_area_sqkm,
  reference_osm_completeness = osm_building_area_sqkm_2022 / a.reference_building_area_sqkm,
  microsoft_building_area_sqkm = a.microsoft_building_area_sqkm
FROM (
    select
        urban_center_id
        ,sum(reference_building_area_sqkm) as reference_building_area_sqkm
        ,sum(microsoft_building_area_sqkm) as microsoft_building_area_sqkm
    from reference_data_urban_centers_grid a
    group by urban_center_id
) a
WHERE a.urban_center_id = b.urban_center_id;