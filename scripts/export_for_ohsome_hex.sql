-- Grid geometries for very high zoom levels
-- zoom level >=12
drop table if exists urban_building_completeness_12;
create table urban_building_completeness_12 as
select
	id
	,'2023-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm
union
select
	id
	,'2022-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm


-- Polygon boundary for higher zoom levels
-- zoom level 9-11
drop table if exists urban_building_completeness_9;
create table urban_building_completeness_9 as
select
	urban_center_id as id
	,'2023-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2023::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2022-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2022::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2021-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2021::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2020-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2020::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2019-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2019::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2018-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2018::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2017-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2017::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2016-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2016::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2015-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2015::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2014-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2014::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2013-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2013::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2012-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2012::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2011-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2011::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2010-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2010::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2009-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2009::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2008-01-01'::timestamptz as timestamp
	,round(prediction_osm_completeness_2008::numeric, 3) as value
	,st_transform(geom, 3857) as geom
from rf_adjusted_prediction_reference_and_osm_urban_centers;

-- Centroid for lower zoom levels
-- zoom level <=8
drop table if exists urban_building_completeness_6;
create table urban_building_completeness_6 as
select
	id
	,timestamp
	,value
	,st_centroid(geom) as geom
from ohsome_hex_polygons



