select
*
from data_preparation.osm_user_contributions_per_project_per_day




drop table if exists hot_tm_projects;
create table hot_tm_projects as
select
  project_id
  ,st_makevalid(geometry) as geom
from data_preparation.projects p;

CREATE INDEX hot_tm_projects_gist
  ON hot_tm_projects
  USING GIST (geom);

drop table if exists osm_user_contributions_per_urban_center_per_day_full;
create table osm_user_contributions_per_urban_center_per_day_full as
(
select
	"timestamp"::timestamp as timestamp
	,user_id
	,"CREATION_AREA"
	,"CHANGE_AREA"
	,"DELETION_AREA"
	,"CREATION_COUNT"
	,"CHANGE_COUNT"
	,"DELETION_COUNT"
	,urban_center_id
from osm_user_contributions_per_urban_center_per_day
)
union
(
select
	timestamp::timestamptz at time zone 'UTC' as timestamp
	,"userID" as user_id
	,SUM(
		case when "contributionType" = '_creation' then area
		else 0
		end
	) as "CREATION_AREA"
	,SUM(
		case when "contributionType" = '_change' then area
		else 0
		end
	) as "CHANGE_AREA"
	,SUM(
		case when "contributionType" = '_deletion' then area
		else 0
		end
	) as "DELETION_AREA"
	,SUM(
		case when "contributionType" = '_creation' then 1
		else 0
		end
	) as "CREATION_COUNT"
	,SUM(
		case when "contributionType" = '_change' then 1
		else 0
		end
	) as "CHANGE_COUNT"
	,SUM(
		case when "contributionType" = '_deletion' then 1
		else 0
		end
	) as "DELETION_COUNT"
	,id as urban_center_id
from osm_user_contributions_per_urban_center_per_day_since_2021
where timestamp > '2021-11-30'
group by "userID", timestamp, urban_center_id
order by urban_center_id, timestamp, "userID"
);

create table data_preparation.projects_urban_centers as
select
  a.project_id
  ,b.urban_center_id as urban_center_id
from  hot_tm_projects a, full_urban_centers b
where st_intersects(a.geom, b.geom);


drop table if exists osm_user_contributions_per_urban_center_per_day_with_flag;
create table osm_user_contributions_per_urban_center_per_day_with_flag as
with tm_user_sessions_per_project_per_day as (
	select
	  project_id
	  ,userid
	  ,date_trunc('day', starttime) as day
	      ,count(*) session_count
	from data_preparation.sessions s
    group by project_id, userid, day
),
osm_user_contributions_per_project_per_day_hot_tm as (
select
	a.*
	,case when b.project_id is not null then 1 else 0 end as hot_tm_user
from data_preparation.osm_user_contributions_per_project_per_day a
left join tm_user_sessions_per_project_per_day b on
	-- Here we match session in the HOT Tasking Manager and
    -- contributions made to OSM. We assume that a user that worked
    -- on a session in the HOT Tasking Manager and that mapped in OSM
    -- on the same day in the project region can be counted as a
    -- mapper that edited OSM through the HOT Tasking Manager
    a.project_id = b.project_id
    and
    a.userid = b.userid
    and
    a.day = b.day
),
urban_center_projects as (
select
  urban_center_id
  ,array_agg(project_id) as project_ids
from data_preparation.projects_urban_centers puc
group by urban_center_id
),
first_step as
(
select
  a.*
  ,b.project_ids
from osm_user_contributions_per_urban_center_per_day_full a
left join urban_center_projects b
	on a.urban_center_id = b.urban_center_id
)
select
  a.*
  ,case when c.userid is not null then 1 else 0 end as hot_tm_user
from first_step a
left join osm_user_contributions_per_project_per_day_hot_tm c on
	c.hot_tm_user = 1
	and a.user_id = c.userid
	and a."timestamp"::timestamp = c.day
	and c.project_id = ANY(a.project_ids)
where
    -- these users have edited unrealistic big features tagged as a building in OSM
    -- we remove their contributions
	user_id != 16865185
	and user_id != 65282
	and user_id != 9379362
	and user_id != 14753818
	and user_id != 1778799
	and user_id != 2823574
;


