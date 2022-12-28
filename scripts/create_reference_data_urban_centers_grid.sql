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