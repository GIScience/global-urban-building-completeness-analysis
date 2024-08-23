show search_path;

SET search_path TO benni, public;

-- Grid geometries for very high zoom levels
-- zoom level >=12
drop table if exists benni.urban_building_completeness_grid;
create table benni.urban_building_completeness_grid as
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2024-05-01Z'::timestamptz as timestamp
	,osm_completeness_2024_05::integer as osm_building_completeness
	,osm_building_area_sqkm_2024_05::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2024-01-01Z'::timestamptz as timestamp
	,osm_completeness_2024_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2024_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2023-01-01Z'::timestamptz as timestamp
	,osm_completeness_2023_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2023_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2022-01-01Z'::timestamptz as timestamp
	,osm_completeness_2022_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2022_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2021-01-01Z'::timestamptz as timestamp
	,osm_completeness_2021_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2021_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2020-01-01Z'::timestamptz as timestamp
	,osm_completeness_2020_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2020_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2019-01-01Z'::timestamptz as timestamp
	,osm_completeness_2019_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2019_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2018-01-01Z'::timestamptz as timestamp
	,osm_completeness_2018_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2018_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2017-01-01Z'::timestamptz as timestamp
	,osm_completeness_2017_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2017_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2016-01-01Z'::timestamptz as timestamp
	,osm_completeness_2016_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2016_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2015-01-01Z'::timestamptz as timestamp
	,osm_completeness_2015_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2015_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2014-01-01Z'::timestamptz as timestamp
	,osm_completeness_2014_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2014_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2013-01-01Z'::timestamptz as timestamp
	,osm_completeness_2013_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2013_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2012-01-01Z'::timestamptz as timestamp
	,osm_completeness_2012_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2012_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2011-01-01Z'::timestamptz as timestamp
	,osm_completeness_2011_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2011_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2010-01-01Z'::timestamptz as timestamp
	,osm_completeness_2010_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2010_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2009-01-01Z'::timestamptz as timestamp
	,osm_completeness_2009_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2009_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
union
select
	identifier as id
	,"ID_UC_G0" as urban_center_id
	,'2008-01-01Z'::timestamptz as timestamp
	,osm_completeness_2008_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2008_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(a.geom, 3857) as geom
from grid_full_info_v2024 a
;

-- Polygon boundary for higher zoom levels
-- zoom level 9-11
drop table if exists benni.urban_building_completeness_polygon;
create table benni.urban_building_completeness_polygon as
select
	"ID_UC_G0" as id
	,'2024-05-01Z'::timestamptz as timestamp
	,osm_completeness_2024_05::integer as osm_building_completeness
	,osm_building_area_sqkm_2024_05::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2024-01-01Z'::timestamptz as timestamp
	,osm_completeness_2024_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2024_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2023-01-01Z'::timestamptz as timestamp
	,osm_completeness_2023_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2023_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2022-01-01Z'::timestamptz as timestamp
	,osm_completeness_2022_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2022_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2021-01-01Z'::timestamptz as timestamp
	,osm_completeness_2021_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2021_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2020-01-01Z'::timestamptz as timestamp
    ,osm_completeness_2020_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2020_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2019-01-01Z'::timestamptz as timestamp
	,osm_completeness_2019_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2019_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2018-01-01Z'::timestamptz as timestamp
	,osm_completeness_2018_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2018_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2017-01-01Z'::timestamptz as timestamp
	,osm_completeness_2017_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2017_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2016-01-01Z'::timestamptz as timestamp
	,osm_completeness_2016_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2016_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2015-01-01Z'::timestamptz as timestamp
	,osm_completeness_2015_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2015_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2014-01-01Z'::timestamptz as timestamp
	,osm_completeness_2014_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2014_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2013-01-01Z'::timestamptz as timestamp
	,osm_completeness_2013_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2013_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2012-01-01Z'::timestamptz as timestamp
	,osm_completeness_2012_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2012_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2011-01-01Z'::timestamptz as timestamp
	,osm_completeness_2011_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2011_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2010-01-01Z'::timestamptz as timestamp
	,osm_completeness_2010_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2010_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2009-01-01Z'::timestamptz as timestamp
	,osm_completeness_2009_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2009_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024
UNION
select
	"ID_UC_G0" as id
	,'2008-01-01Z'::timestamptz as timestamp
	,osm_completeness_2008_01::integer as osm_building_completeness
	,osm_building_area_sqkm_2008_01::float4 as osm_building_area_sqkm
	,prediction_improved_sqkm::float4 as predicted_building_area_sqkm
	,st_transform(geom, 3857) as geom
from uc_full_info_V2024;

-- Centroid for lower zoom levels
-- zoom level <=8
drop table if exists benni.urban_building_completeness_point;
create table benni.urban_building_completeness_point as
select
	id
	,timestamp
	,osm_building_completeness
	,osm_building_area_sqkm
	,predicted_building_area_sqkm
	,st_centroid(geom) as geom
from benni.urban_building_completeness_polygon;



------------------------
ALTER TABLE public.urban_building_completeness_point SET SCHEMA michel_temp;
ALTER TABLE public.urban_building_completeness_polygon SET SCHEMA michel_temp;
ALTER TABLE public.urban_building_completeness_grid SET SCHEMA michel_temp;



CREATE TABLE public.urban_building_completeness_point AS
SELECT
  id ,
  "timestamp" ,
  osm_building_completeness AS osm_building_completeness_pc,
  predicted_building_area_sqkm / 100 AS predicted_building_area_ha,
  geom::geometry(POINT,3857) as geom
FROM benni.urban_building_completeness_point;

CREATE TABLE public.urban_building_completeness_polygon AS
SELECT
  id ,
  "timestamp" ,
  osm_building_completeness AS osm_building_completeness_pc,
  predicted_building_area_sqkm / 100 AS predicted_building_area_ha,
  geom::geometry(MULTIPOLYGON ,3857) as geom
FROM benni.urban_building_completeness_polygon;

DROP TABLE public.urban_building_completeness_grid CASCADE;

CREATE TABLE public.urban_building_completeness_grid AS
SELECT
  id ,
  "timestamp" ,
  osm_building_completeness AS osm_building_completeness_pc,
  predicted_building_area_sqkm / 100 AS predicted_building_area_ha,
  (ST_DUMP(geom)).geom::geometry(POLYGON ,3857) as geom
FROM benni.urban_building_completeness_grid;

-------------

CREATE INDEX urban_building_completeness_point_timestamp_osm_b_compl_pc_idx ON public.urban_building_completeness_point (timestamp, osm_building_completeness_pc);
ANALYZE public.urban_building_completeness_point;
CLUSTER public.urban_building_completeness_point USING urban_building_completeness_point_timestamp_osm_b_compl_pc_idx;
CREATE INDEX urban_building_completeness_point_timestamp_idx ON public.urban_building_completeness_point (timestamp);
CREATE INDEX urban_building_completeness_point_id_idx ON public.urban_building_completeness_point (id);
CREATE INDEX urban_building_completeness_point_osm_build_compl_pc_idx ON public.urban_building_completeness_point (osm_building_completeness_pc);
CREATE INDEX urban_building_completeness_point_geom_idx ON public.urban_building_completeness_point USING gist(geom);
ANALYZE public.urban_building_completeness_point;

-- order (CLUSTER) poylgons only by timestamp, they do not overlap on the map
CREATE INDEX urban_building_completeness_polygon_timestamp_idx ON public.urban_building_completeness_polygon (timestamp);
ANALYZE public.urban_building_completeness_polygon;
CLUSTER public.urban_building_completeness_polygon USING urban_building_completeness_polygon_timestamp_idx;
CREATE INDEX urban_building_completeness_polygon_id_idx ON public.urban_building_completeness_polygon (id);
CREATE INDEX urban_building_completeness_polygon_osm_build_compl_pc_idx ON public.urban_building_completeness_polygon (osm_building_completeness_pc);
CREATE INDEX urban_building_completeness_polygon_geom_idx ON public.urban_building_completeness_polygon USING gist(geom);
ANALYZE public.urban_building_completeness_polygon;

-- order (CLUSTER) grid cells by timestamp and value, they do not overlap but the strokeline sometimes glitches
CREATE INDEX urban_building_completeness_grid_timestamp_osm_b_compl_pc_idx ON public.urban_building_completeness_grid (timestamp,osm_building_completeness_pc);
ANALYZE public.urban_building_completeness_grid;
CLUSTER public.urban_building_completeness_grid USING urban_building_completeness_grid_timestamp_osm_b_compl_pc_idx;
CREATE INDEX urban_building_completeness_grid_timestamp_idx ON public.urban_building_completeness_grid (timestamp);
CREATE INDEX urban_building_completeness_grid_id_idx ON public.urban_building_completeness_grid (id);
CREATE INDEX urban_building_completeness_grid_osm_build_compl_pc_idx ON public.urban_building_completeness_grid (osm_building_completeness_pc);
CREATE INDEX urban_building_completeness_grid_geom_idx ON public.urban_building_completeness_grid USING gist(geom);
ANALYZE public.urban_building_completeness_grid;




