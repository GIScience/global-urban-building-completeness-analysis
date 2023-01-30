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


def load_urban_centers_grid():
    con = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    query = f"""
        SELECT
           a.grid_fid as fid
          ,a.*
        FROM full_urban_centers_grid a
    """
    df = gpd.GeoDataFrame.from_postgis(query, con, geom_col="geom").set_index("fid")

    df["region_wb"] = pd.Categorical(df["region_wb"])
    df['region_code'] = df.region_wb.cat.codes

    df['shdi_2019'].fillna((df['shdi_2019'].mean()), inplace=True)
    df['osm_road_length_km_2023'].fillna((df['osm_road_length_km_2023'].mean()), inplace=True)

    for column in df.columns:
        if column in [
            "external_reference_building_area_sqkm",
            "microsoft_building_area_sqkm",
            "reference_building_area_sqkm",
            "reference_osm_completeness",
        ]:
            continue

        df[column] = df[column].fillna(0)

    logging.info(len(df))
    return df


def get_urban_center_ids(threshold=0.01):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    table_name = f"prediction_reference_urban_centers"
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
