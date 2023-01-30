drop table if exists microsoft_buildings_urban_centers_grid;
create table microsoft_buildings_urban_centers_grid as
with coverage_urban_centers_2023 as
(
select
	a.urban_center_id
	,count(a.id) as count
	,max(b.total_area_sqkm) total_area_sqkm
	,count(a.id) / max(b.total_area_sqkm) as coverage
from microsoft_buildings_urban_centers_grid_raw a
left join full_urban_centers b on
	a.urban_center_id = b.urban_center_id
where a.ms_building_area_sq_m / (1000*1000) < 1
group by a.urban_center_id
),
microsoft_buildings_urban_centers_grid_2023 as
(
select
	a.grid_id::integer as grid_fid
	,a.urban_center_id::integer
	,a.ms_building_count as microsoft_building_count
	,a.ms_building_area_sq_m / (1000*1000) as microsoft_building_area_sqkm
	,b.coverage
	,a.geom
from microsoft_buildings_urban_centers_grid_raw a
left join coverage_urban_centers_2023 b on
	a.urban_center_id = b.urban_center_id
where b.coverage > 0.95 and a.ms_building_area_sq_m / (1000*1000) < 1
),
coverage_urban_centers_2022 as
(
select
	a.urban_center_id
	,count(a.grid_fid) as count
	,max(b.total_area_sqkm) total_area_sqkm
	,count(a.grid_fid) / max(b.total_area_sqkm) as coverage
from microsoft_reference_data_urban_centers_grid a
left join full_urban_centers b on
	a.urban_center_id = b.urban_center_id
group by a.urban_center_id
),
microsoft_buildings_urban_centers_grid_2022 as
(
select
	a.grid_fid::integer
	,a.urban_center_id::integer
	,a.microsoft_building_count
	,a.microsoft_building_area_sqkm
	,b.coverage
	,a.geom
from microsoft_reference_data_urban_centers_grid a
left join coverage_urban_centers_2022 b on
	a.urban_center_id = b.urban_center_id
where b.coverage > 0.95
),
microsoft_buildings_urban_centers_grid_2023_union as
(
select * from microsoft_buildings_urban_centers_grid_2023
union
select * from microsoft_buildings_urban_centers_grid_2022
)
select
	a.grid_fid
	,a.urban_center_id
	,max(a.microsoft_building_count) as microsoft_building_count
	,max(a.microsoft_building_area_sqkm) as microsoft_building_area_sqkm
	,b.geom
from microsoft_buildings_urban_centers_grid_2023_union a
left join metadata_urban_centers_grid b on
	a.grid_fid = b.grid_fid and a.urban_center_id = b.urban_center_id
group by a.urban_center_id, a.grid_fid, b.geom;



