drop table if exists prediction_reference_and_osm_urban_centers_grid;
create table prediction_reference_and_osm_urban_centers_grid AS (
    select
        a.*
        ,b.prediction
        ,a.osm_building_area_sqkm_2023 / b.prediction as prediction_osm_completeness_2023
    from full_urban_centers_grid a
    left join prediction_reference_and_osm_grid_raw b on
        a.grid_fid = b.grid_fid
);

drop table if exists prediction_reference_and_osm_urban_centers;
create table prediction_reference_and_osm_urban_centers AS
with urban_centers_data as (
    select
      urban_center_id
      ,sum(prediction) as sum_prediction_sqkm
    from prediction_reference_and_osm_grid_raw a
    group by urban_center_id
)
select
    a.*
    ,b.sum_prediction_sqkm
    ,a.osm_building_area_sqkm_2023  / b.sum_prediction_sqkm as prediction_osm_completeness_2023
    ,a.osm_building_area_sqkm_2022  / b.sum_prediction_sqkm as prediction_osm_completeness_2022
    ,a.osm_building_area_sqkm_2021  / b.sum_prediction_sqkm as prediction_osm_completeness_2021
    ,a.osm_building_area_sqkm_2020  / b.sum_prediction_sqkm as prediction_osm_completeness_2020
    ,a.osm_building_area_sqkm_2019  / b.sum_prediction_sqkm as prediction_osm_completeness_2019
    ,a.osm_building_area_sqkm_2018  / b.sum_prediction_sqkm as prediction_osm_completeness_2018
    ,a.osm_building_area_sqkm_2017  / b.sum_prediction_sqkm as prediction_osm_completeness_2017
    ,a.osm_building_area_sqkm_2016  / b.sum_prediction_sqkm as prediction_osm_completeness_2016
    ,a.osm_building_area_sqkm_2015  / b.sum_prediction_sqkm as prediction_osm_completeness_2015
    ,a.osm_building_area_sqkm_2014  / b.sum_prediction_sqkm as prediction_osm_completeness_2014
    ,a.osm_building_area_sqkm_2013  / b.sum_prediction_sqkm as prediction_osm_completeness_2013
    ,a.osm_building_area_sqkm_2012  / b.sum_prediction_sqkm as prediction_osm_completeness_2012
    ,a.osm_building_area_sqkm_2011  / b.sum_prediction_sqkm as prediction_osm_completeness_2011
    ,a.osm_building_area_sqkm_2010  / b.sum_prediction_sqkm as prediction_osm_completeness_2010
    ,a.osm_building_area_sqkm_2009  / b.sum_prediction_sqkm as prediction_osm_completeness_2009
    ,a.osm_building_area_sqkm_2008  / b.sum_prediction_sqkm as prediction_osm_completeness_2008
from full_urban_centers a
left join urban_centers_data b on
    a.urban_center_id = b.urban_center_id;