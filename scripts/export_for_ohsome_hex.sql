-- Grid geometries for very high zoom levels
-- zoom level >=12
drop table if exists urban_building_completeness_grid;
create table urban_building_completeness_grid as
select
	grid_fid as id
	,urban_center_id
	,'2023-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2023 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2023::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2022-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2022 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2022::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2021-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2021 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2021::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2020-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2020 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2020::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2019-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2019 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2019::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2018-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2018 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2018::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2017-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2017 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2017::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2016-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2016 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2016::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2015-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2015 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2015::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2014-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2014 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2014::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2013-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2013 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2013::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2012-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2012 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2012::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2011-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2011 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2011::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2010-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2010 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2010::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2009-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2009 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2009::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
union
select
	grid_fid as id
	,urban_center_id
	,'2008-01-01Z'::timestamptz as timestamp
	,(100* osm_building_area_sqkm_2008 / prediction)::integer as osm_building_completeness
	,osm_building_area_sqkm_2008::float4 as osm_building_area_sqkm
	,prediction::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from prediction_reference_and_osm_urban_centers_grid a
;

-- Polygon boundary for higher zoom levels
-- zoom level 9-11
drop table if exists urban_building_completeness_polygon;
create table urban_building_completeness_polygon as
select
	urban_center_id as id
	,'2023-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2023)::integer as osm_building_completeness
	,osm_building_area_sqkm_2023::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2022-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2022)::integer as osm_building_completeness
	,osm_building_area_sqkm_2022::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2021-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2021)::integer as osm_building_completeness
	,osm_building_area_sqkm_2021::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2020-01-01Z'::timestamptz as timestamp
    ,(100*prediction_osm_completeness_2020)::integer as osm_building_completeness
	,osm_building_area_sqkm_2020::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2019-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2019)::integer as osm_building_completeness
	,osm_building_area_sqkm_2019::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2018-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2018)::integer as osm_building_completeness
	,osm_building_area_sqkm_2018::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2017-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2017)::integer as osm_building_completeness
	,osm_building_area_sqkm_2017::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2016-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2016)::integer as osm_building_completeness
	,osm_building_area_sqkm_2016::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2015-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2015)::integer as osm_building_completeness
	,osm_building_area_sqkm_2015::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2014-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2014)::integer as osm_building_completeness
	,osm_building_area_sqkm_2014::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2013-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2013)::integer as osm_building_completeness
	,osm_building_area_sqkm_2013::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2012-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2012)::integer as osm_building_completeness
	,osm_building_area_sqkm_2012::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2011-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2011)::integer as osm_building_completeness
	,osm_building_area_sqkm_2011::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2010-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2010)::integer as osm_building_completeness
	,osm_building_area_sqkm_2010::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2009-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2009)::integer as osm_building_completeness
	,osm_building_area_sqkm_2009::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers
UNION
select
	urban_center_id as id
	,'2008-01-01Z'::timestamptz as timestamp
	,(100*prediction_osm_completeness_2008)::integer as osm_building_completeness
	,osm_building_area_sqkm_2008::float4 as osm_building_area_sqkm
	,sum_prediction_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from prediction_reference_and_osm_urban_centers;

-- Centroid for lower zoom levels
-- zoom level <=8
drop table if exists urban_building_completeness_point;
create table urban_building_completeness_point as
select
	id
	,timestamp
	,osm_building_completeness
	,osm_building_area_sqkm
	,predicted_building_area_sqkm
	,st_centroid(geom) as geom
from urban_building_completeness_polygon;

