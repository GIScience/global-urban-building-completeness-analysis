create table geowiki_grids_final as
select
  a.id
  ,a.cell_uid
  ,a.stratum_le
  ,a.id_left
  ,a."LegendItemName" as reference_label
  ,a.region_wb
  ,a.urban_center_id
  ,a.iso_a3
  ,b.ms_building_count
  ,b.building_area_intersecting_sq_m
  ,case
	  when c.microsoft_building_area_sqkm > 0 then True
	  else False
	end as microsoft_available
  ,case
		when building_area_intersecting_sq_m > 0 and a."LegendItemName" = 'Built-up' then 1
		else 0
  end as tp
  ,case
		when building_area_intersecting_sq_m > 0 and a."LegendItemName" = 'Not built-up' then 1
		else 0
  end as fp
  ,case
		when building_area_intersecting_sq_m is null and a."LegendItemName" = 'Not built-up' then 1
		else 0
  end as tn
  ,case
		when building_area_intersecting_sq_m is null and a."LegendItemName" = 'Built-up' then 1
		else 0
  end as fn
  ,st_centroid(a.geom) as geom
from geowiki_selection a
left join geowiki_grids_with_ms_stats b on
	a.cell_uid = b.cell_uid
left join full_urban_centers c on
	a.urban_center_id = c.urban_center_id;
