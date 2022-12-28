import os
import logging
import pandas as pd
import geopandas as gpd

from sqlalchemy import create_engine


HOST = os.getenv("POSTGRES_HOST", default="localhost")
PORT = os.getenv("POSTGRES_PORT", default=5429)
DATABASE = os.getenv("POSTGRES_DB", default="osm-paper")
USER = os.getenv("POSTGRES_USER", default="osm-paper")
PASSWORD = os.getenv("POSTGRES_PASSWORD", default="osm-paper")


def load_urban_centers_grid(unit):
    con = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    query = f"""
        SELECT
          a.id as fid
          ,a.id as grid_fid
          ,a.urban_center_id
          ,a."name_main" as name
          ,a.iso_a3
          ,a.country_id
          ,a.continent
          ,a.region_wb
          -- reference
          ,a.reference_building_{unit}
          -- OSM
          ,a.osm_building_{unit}
          -- covariates
          ,a.ghspop
          ,a.shdi
          ,a.vnl
          ,a.osm_motorway_roads_length_km
          ,a.osm_other_major_roads_length_km
          ,a.osm_airports_area_sqkm
          ,a.osm_railway_length_km
          -- ,a.osm_amenity_count
          ,a.wsf_built_up_area_sqkm
          -- worldcover
          ,a.tree_cover_sqkm
          ,a.shrubland_sqkm
          ,a.grassland_sqkm
          ,a.cropland_sqkm
          ,a.built_up_sqkm
          ,a.sparse_vegetation_sqkm
          ,a.snow_and_ice_sqkm
          ,a.permanent_water_bodies_sqkm
          ,a.herbaceous_wetland_sqkm
          ,a.mangroves_sqkm
          ,a.moss_and_lichen_sqkm
          ,a.total_sqkm
          -- spatial autocorrelation
          ,a.ghspop_moran_loc 
          ,a.osm_motorway_roads_length_km_moran
          ,a.osm_other_major_roads_length_km_moran
          ,a.built_up_sqkm_moran_loc
          -- CO2
          ,a.fossil_fuel
          -- geometry
          ,a.geom
        FROM all_parameters_urban_centers_grid a
    """
    df = gpd.GeoDataFrame.from_postgis(query, con, geom_col="geom").set_index("fid")
    df[f"reference_completeness_{unit}"] = round(df[f"osm_building_{unit}"] / df[f"reference_building_{unit}"], 3)

    columns = [
        "ghspop",
        "vnl",
        "osm_motorway_roads_length_km",
        "osm_other_major_roads_length_km",
        "osm_airports_area_sqkm",
        # "osm_amenity_count",
        "tree_cover_sqkm",
        "shrubland_sqkm",
        "grassland_sqkm",
        "cropland_sqkm",
        "built_up_sqkm",
        "sparse_vegetation_sqkm",
        "snow_and_ice_sqkm",
        "permanent_water_bodies_sqkm",
        "herbaceous_wetland_sqkm",
        "mangroves_sqkm",
        "moss_and_lichen_sqkm",
        "ghspop_moran_loc",
        "osm_motorway_roads_length_km_moran",
        "osm_other_major_roads_length_km_moran",
        "built_up_sqkm_moran_loc",
        "fossil_fuel",
        "wsf_built_up_area_sqkm",
    ]
    for column in columns:
        df[column] = df[column].fillna(0)

    logging.info(len(df))

    df.dropna(subset=[
        "total_sqkm",
        "shdi"
    ], inplace=True)

    logging.info(len(df))

    df["region_wb"] = pd.Categorical(df["region_wb"])
    df['region_code'] = df.region_wb.cat.codes

    return df


def get_urban_center_ids(model_name, threshold=0.01):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    table_name = f"{model_name}_prediction_reference_urban_centers"
    sql = f"""
        select 
          urban_center_id 
        from {table_name} a
        -- potential training regions where OSM exceeds our prediction above error range
        -- this means that for these region we underestimate the actual building area
        -- (assuming that OSM is correct)
        where
            (osm_building_area_sqkm_2022 - sum_prediction_sqkm )
            > 
            -- here we need to define when to consider OSM as complete
            (ST_Area(geom::geography)/(1000*1000) * {threshold})
    """
    df = pd.read_sql(sql, con=con)
    urban_center_ids = df["urban_center_id"].values
    logging.info(f"got {len(urban_center_ids)} urban centers for potential training")

    return urban_center_ids
