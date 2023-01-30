drop table if exists full_urban_centers;
create table full_urban_centers as
(
with ghspop_2020_urban_centers as (
	select urban_center_id, sum(ghspop_2020) as ghspop_2020
	from ghspop_2020_urban_centers_grid
	group by urban_center_id
),
shdi_2019_urban_centers as (
	select urban_center_id, avg(shdi) as shdi_2019
	from shdi_2019_urban_centers_grid sucg
	group by urban_center_id
),
osm_building_area_2023_urban_centers as (
	select
		urban_center_id
		,sum(osm_building_area_sqkm_2023) as osm_building_area_sqkm_2023
		,sum(osm_building_area_sqkm_2022) as osm_building_area_sqkm_2022
		,sum(osm_building_area_sqkm_2021) as osm_building_area_sqkm_2021
		,sum(osm_building_area_sqkm_2020) as osm_building_area_sqkm_2020
		,sum(osm_building_area_sqkm_2019) as osm_building_area_sqkm_2019
		,sum(osm_building_area_sqkm_2018) as osm_building_area_sqkm_2018
		,sum(osm_building_area_sqkm_2017) as osm_building_area_sqkm_2017
		,sum(osm_building_area_sqkm_2016) as osm_building_area_sqkm_2016
		,sum(osm_building_area_sqkm_2015) as osm_building_area_sqkm_2015
		,sum(osm_building_area_sqkm_2014) as osm_building_area_sqkm_2014
		,sum(osm_building_area_sqkm_2013) as osm_building_area_sqkm_2013
		,sum(osm_building_area_sqkm_2012) as osm_building_area_sqkm_2012
		,sum(osm_building_area_sqkm_2011) as osm_building_area_sqkm_2011
		,sum(osm_building_area_sqkm_2010) as osm_building_area_sqkm_2010
		,sum(osm_building_area_sqkm_2009) as osm_building_area_sqkm_2009
		,sum(osm_building_area_sqkm_2008) as osm_building_area_sqkm_2008
	from osm_building_area_2023_urban_centers_grid
	group by urban_center_id
),
external_reference_data_urban_centers as (
	select
		urban_center_id
		,SUM(external_reference_building_area_sqkm) as external_reference_building_area_sqkm
	from external_reference_data_urban_centers_grid
	group by urban_center_id
),
microsoft_reference_data_urban_centers as (
	select
		urban_center_id
		,SUM(microsoft_building_area_sqkm) as microsoft_building_area_sqkm
	from microsoft_buildings_urban_centers_grid
	group by urban_center_id
),
geowiki_selection_urban_centers as (
    select urban_center_id, 1  as geowiki
    from geowiki_selection
    group by urban_center_id
)
select
	a.*
	,b.ghspop_2020 as ghspop_2020
	,case
        when b.ghspop_2020 < 200000 then 'small urban areas'
        when b.ghspop_2020 < 500000 then 'medium-size urban areas'
        when b.ghspop_2020 < 1500000 then 'metropolitan areas'
        when b.ghspop_2020 >= 1500000 then 'large metropolitan areas'
    end as ghspop_2020_class
    ,round(c.shdi_2019, 3) as shdi_2019
    ,CASE
      when c.shdi_2019 < 0.55 THEN 'low'
      WHEN c.shdi_2019 < 0.7 THEN 'medium'
      WHEN c.shdi_2019 < 0.8 THEN 'high'
      WHEN c.shdi_2019 >= 0.8 THEN 'very high'
    END as shdi_2019_class
    ,d.osm_building_area_sqkm_2023
    ,d.osm_building_area_sqkm_2022
    ,d.osm_building_area_sqkm_2021
    ,d.osm_building_area_sqkm_2020
    ,d.osm_building_area_sqkm_2019
    ,d.osm_building_area_sqkm_2018
    ,d.osm_building_area_sqkm_2017
    ,d.osm_building_area_sqkm_2016
    ,d.osm_building_area_sqkm_2015
    ,d.osm_building_area_sqkm_2014
    ,d.osm_building_area_sqkm_2013
    ,d.osm_building_area_sqkm_2012
    ,d.osm_building_area_sqkm_2011
    ,d.osm_building_area_sqkm_2010
    ,d.osm_building_area_sqkm_2009
    ,d.osm_building_area_sqkm_2008
    ,e.external_reference_building_area_sqkm
    ,f.microsoft_building_area_sqkm
    ,case
    	when e.external_reference_building_area_sqkm is null then f.microsoft_building_area_sqkm
    	else e.external_reference_building_area_sqkm
    end as reference_building_area_sqkm
    ,case
    	when e.external_reference_building_area_sqkm is null and g.geowiki=1 then f.microsoft_building_area_sqkm
    	else e.external_reference_building_area_sqkm
    end as reference_building_area_sqkm_strict
    ,case
		when e.external_reference_building_area_sqkm is null then d.osm_building_area_sqkm_2023 / f.microsoft_building_area_sqkm
		else d.osm_building_area_sqkm_2023 / e.external_reference_building_area_sqkm
	end as reference_osm_completeness
	,case
		when e.external_reference_building_area_sqkm is null then d.osm_building_area_sqkm_2023 / f.microsoft_building_area_sqkm
		else d.osm_building_area_sqkm_2023 / e.external_reference_building_area_sqkm
	end as reference_osm_completeness_strict
	,g.geowiki
from metadata_urban_centers a
left join ghspop_2020_urban_centers b on
	a.urban_center_id = b.urban_center_id
left join shdi_2019_urban_centers c on
	a.urban_center_id = c.urban_center_id
left join osm_building_area_2023_urban_centers d on
	a.urban_center_id = d.urban_center_id
left join external_reference_data_urban_centers e on
	a.urban_center_id = e.urban_center_id
left join microsoft_reference_data_urban_centers f on
	a.urban_center_id = f.urban_center_id
left join geowiki_selection_urban_centers g on
    a.urban_center_id = g.urban_center_id
);

CREATE INDEX full_urban_centers_gist
  ON full_urban_centers
  USING GIST (geom);