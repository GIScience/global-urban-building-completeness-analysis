CREATE INDEX projects_gist
  ON "data_preparation".projects
  USING GIST (geometry);



with urban_centers_with_hot_projects as
(
	select
		a.urban_center_id
		,b.project_id
	from full_urban_centers a, data_preparation.projects b
	where st_intersects(st_makeValid(a.geom), st_makeValid(b.geometry))
	limit 1000
),
urban_centers_with_hot_projects_agg as (
	select
		urban_center_id
		,array_agg(project_id) hot_tm_project_ids
	from urban_centers_with_hot_projects
	group by urban_center_id
),
potential_matches as
(
select
	a.*
	,b.*
from osm_user_contributions_per_urban_center_per_day a
left join data_preparation.osm_user_contributions_per_project_per_day b on
	a.user_id = b.userid
	and
	a."timestamp"::timestamp = b."day"
limit 10
)
select
	a.*
from potential_matches a, urban_centers_with_hot_projects_agg b
where
	a.urban_center_id = b.urban_center_id
	and
	a.project_id = any (b.hot_tm_project_ids)