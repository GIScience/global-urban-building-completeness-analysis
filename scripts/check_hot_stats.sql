
-- total building stasts
select
	sum("CREATION_AREA" + "CHANGE_AREA" - "DELETION_AREA") / (1000*1000) as hot_tm_area_stats
from osm_user_contributions_per_urban_center_per_day_with_flag
where
	timestamp > '2010-01-01'
	and user_id != 16865185
	and user_id != 65282
	and user_id != 9379362
	and "timestamp" < '2021-07-01';


select
	date_trunc('month', timestamp) as month
	,count(*) as count
	,count(distinct user_id) as distinct_hot_tm_users
	,sum("CREATION_AREA" + "CHANGE_AREA" - "DELETION_AREA") / (1000*1000) as area_stats_sqkm
from osm_user_contributions_per_urban_center_per_day_with_flag
where
	timestamp > '2010-01-01'
group by month


select
  sum(osm_building_area_sqkm_2023)
from full_urban_centers



-- total hot tm building stats
select
	sum("CREATION_AREA" + "CHANGE_AREA" - "DELETION_AREA") / (1000*1000) as hot_tm_area_stats
from osm_user_contributions_per_urban_center_per_day_with_flag
where
	hot_tm_user = 1
	and timestamp > '2010-01-01'
	and user_id != 16865185
	and user_id != 65282
	and user_id != 9379362
	and "timestamp" < '2021-07-01'

select
	date_trunc('month', timestamp) as month
	,count(*) as count
	,count(distinct user_id) as distinct_hot_tm_users
	,sum("CREATION_AREA" + "CHANGE_AREA" - "DELETION_AREA") / (1000*1000) as hot_tm_area_stats
from osm_user_contributions_per_urban_center_per_day_with_flag
where
	hot_tm_user = 1
	and timestamp > '2010-01-01'
	and user_id != 16865185
	and user_id != 65282
	and user_id != 9379362
group by month


select
	user_id
	,count(*)
	,date_trunc('month', timestamp) as month
	,sum("CREATION_AREA" + "CHANGE_AREA" - "DELETION_AREA") / (1000*1000) as hot_tm_area_stats
from osm_user_contributions_per_urban_center_per_day_with_flag
where hot_tm_user = 1 and timestamp >= '2022-08-01' and "timestamp" < '2022-09-01'
group by user_id, month
order by hot_tm_area_stats desc


select *
from osm_user_contributions_per_urban_center_per_day_with_flag
where user_id = 16865185 or user_id = 65282
-- order by "DELETION_AREA" asc
order by "CREATION_AREA" desc



select
	user_id
	,count(*) as count
	,date_trunc('month', timestamp) as month
	,sum("CREATION_AREA" + "CHANGE_AREA" - "DELETION_AREA") / (1000*1000) as hot_tm_area_stats
from osm_user_contributions_per_urban_center_per_day_with_flag
where hot_tm_user = 1 and timestamp >= '2021-12-01' and "timestamp" < '2022-01-01'
group by user_id, month
order by hot_tm_area_stats desc


select *
from osm_user_contributions_per_urban_center_per_day_with_flag
where user_id = 9379362
-- order by "DELETION_AREA" asc
order by "CREATION_AREA" desc



select
	sum("CREATION_AREA" + "CHANGE_AREA" - "DELETION_AREA") / (1000*1000) as hot_tm_area_stats
from osm_user_contributions_per_urban_center_per_day_with_flag
where
	hot_tm_user = 1
	and timestamp > '2015-01-01'



