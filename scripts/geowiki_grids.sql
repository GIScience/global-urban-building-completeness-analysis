drop table if exists "geowiki_selection";
create table "geowiki_selection" as
select
	c.*
	,a."SubpixelID"
	,a."LegendItemName"
	,a."ControlPoint"
	,b.urban_center_id
	,b.iso_a3
	,b.region_wb
from
	"Geo-WikiBuilt-upCellsQualityControlled" a,
	full_urban_centers b,
	"Geo-Wiki_grid" c
where
	st_intersects(b.geom, a.geom)
	and
	b.reference_building_area_sqkm is not null
	and
	st_intersects(st_transform(a.geom, 3857), c.geom)