import logging
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine

from config import (
    HOST,
    PORT,
    DATABASE,
    USER,
    PASSWORD,
)

from ohsome import OhsomeClient
client = OhsomeClient()


def get_urban_center_ids():
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    sql = f"""
        select 
          urban_center_id 
        from all_parameters_urban_centers
    """
    df = pd.read_sql(sql, con=con)
    urban_center_ids = df["urban_center_id"].values
    logging.info(f"got {len(urban_center_ids)} urban centers")

    return urban_center_ids


def get_input_geometries(urban_center_id):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    query = f"""
        select
            urban_center_id
            ,ST_MakeValid(geom) as geom
        from all_parameters_urban_centers a
        where urban_center_id = %(urban_center_id)s
    """
    df = gpd.GeoDataFrame.from_postgis(
        query,
        con=con,
        params={"urban_center_id": int(urban_center_id)},
        geom_col="geom"
    )
    df.reset_index(inplace=True)
    return df


def get_grid_geometries(urban_center_id):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    query = f"""
        select
            id as grid_fid
            ,urban_center_id
            ,ST_MakeValid(geom) as geom
        from all_parameters_urban_centers_grid a
        where urban_center_id = %(urban_center_id)s
    """
    df = gpd.GeoDataFrame.from_postgis(
        query,
        con=con,
        params={"urban_center_id": int(urban_center_id)},
        geom_col="geom"
    )
    df.reset_index(inplace=True)
    return df


def query_ohsome_api(input_gdf, filter_str="building=* and geometry:polygon"):
    response = client.elements.area.groupByBoundary.post(
        bpolys=input_gdf,
        filter=filter_str,
        time="2022-12-15",  # TODO: adjust timestamp for 2023-01-01 once available
    )
    results_df = response.as_dataframe()
    results_df.reset_index(inplace=True)
    return results_df


def insert_into_postgres(input_gdf):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    export_columns = [
        "urban_center_id",
        "osm_building_area_sqkm_2023",
    ]
    input_gdf[export_columns].to_sql(
        "osm_building_area_urban_centers_2023",
        con=con,
        if_exists="append",
    )
    logging.info("updated OSM stats for urban center in postgres table.")


def insert_into_postgres_grid(input_gdf):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    export_columns = [
        "grid_fid",
        "urban_center_id",
        "osm_building_area_sqkm_2023",
    ]
    input_gdf.reset_index(inplace=True)
    input_gdf[export_columns].to_sql(
        "osm_building_area_urban_centers_grid_2023",
        con=con,
        if_exists="append",
    )
    logging.info("updated OSM stats for grid in postgres table.")


if __name__ == "__main__":
    """python scripts/update_osm_building_stats_2023.py"""

    urban_center_ids = get_urban_center_ids()

    for urban_center_id in urban_center_ids:
        logging.info(f"start update for urban_center_id: {urban_center_id}")

        # run query for urban centers
        urban_centers_df = get_input_geometries(urban_center_id)
        results_df = query_ohsome_api(urban_centers_df)
        # TODO: adjust timestamp for 2023-01-01 once available
        urban_centers_df["osm_building_area_sqkm_2023"] = float(
            results_df.loc[results_df["timestamp"] == '2022-12-15']["value"]) / (1000 * 1000)
        insert_into_postgres(urban_centers_df)

        # run query for urban centers grid
        grid_df = get_grid_geometries(urban_center_id)
        grid_df["region"] = "region_" + grid_df["grid_fid"].astype(str)
        grid_df.set_index("region", inplace=True)
        results_df = query_ohsome_api(grid_df)
        results_df.reset_index(inplace=True)
        results_df.set_index("boundary", inplace=True)
        results_df.drop(columns=["index"], inplace=True)

        join_df = grid_df.join(results_df)
        join_df["osm_building_area_sqkm_2023"] = join_df["value"] / (1000 * 1000)
        insert_into_postgres_grid(join_df)
