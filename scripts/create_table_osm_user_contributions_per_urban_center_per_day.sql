CREATE TABLE osm_user_contributions_per_urban_center_per_day (
	"index" int8 NULL,
	"timestamp" text NULL,
	user_id int8 NULL,
	"CREATION_AREA" float8 NULL,
	"CHANGE_AREA" float8 NULL,
	"DELETION_AREA" float8 NULL,
	"CREATION_COUNT" int8 NULL,
	"CHANGE_COUNT" int8 NULL,
	"DELETION_COUNT" int8 NULL,
	urban_center_id int8 NULL
);

CREATE TABLE osm_user_contributions_per_urban_center_per_day_since_2021 (
	id int8 NULL,
	"timestamp" timestamptz NULL,
	"contributionType" text NULL,
	"userID" int4 NULL,
	area float8 NULL
);