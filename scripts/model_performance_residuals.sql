drop table if exists residuals_reference_and_osm_urban_centers_grid;
create table residuals_reference_and_osm_urban_centers_grid as
with avg_residual as
(
select
  grid_fid
  ,urban_center_id
  ,iso_a3
  ,region_wb
  ,avg(prediction) as prediction
  ,max(reference_building_area_sqkm) as reference_building_area_sqkm
  ,avg(prediction) - max(reference_building_area_sqkm) as residual
from performance_20_clusters_reference_and_osm a
group by grid_fid, urban_center_id, iso_a3, region_wb
)
select
  a.*
  ,b.geom
from avg_residual a
left join full_urban_centers_grid b
    on a.grid_fid = b.grid_fid