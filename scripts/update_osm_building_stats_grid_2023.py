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
        from metadata_urban_centers
        order by urban_center_id
    """
    df = pd.read_sql(sql, con=con)
    urban_center_ids = df["urban_center_id"].values
    logging.info(f"got {len(urban_center_ids)} urban centers")

    return urban_center_ids


def get_grid_geometries(urban_center_id):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    query = f"""
        select
            grid_fid
            ,urban_center_id
            ,ST_MakeValid(geom) as geom
        from metadata_urban_centers_grid a
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
    # TODO: make sure to set correct end timestamp here
    response = client.elements.area.groupByBoundary.post(
        bpolys=input_gdf,
        filter=filter_str,
        time="2008-01-01/2023-01-01/P1Y",
    )
    results_df = response.as_dataframe()
    results_df.reset_index(inplace=True)
    return results_df


def insert_into_postgres_grid(input_gdf):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    export_columns = [
        "grid_fid",
        "urban_center_id",
        "osm_building_area_sqkm_2023",
        "osm_building_area_sqkm_2022",
        "osm_building_area_sqkm_2021",
        "osm_building_area_sqkm_2020",
        "osm_building_area_sqkm_2019",
        "osm_building_area_sqkm_2018",
        "osm_building_area_sqkm_2017",
        "osm_building_area_sqkm_2016",
        "osm_building_area_sqkm_2015",
        "osm_building_area_sqkm_2014",
        "osm_building_area_sqkm_2013",
        "osm_building_area_sqkm_2012",
        "osm_building_area_sqkm_2011",
        "osm_building_area_sqkm_2010",
        "osm_building_area_sqkm_2009",
        "osm_building_area_sqkm_2008",
    ]
    input_gdf.reset_index(inplace=True)
    # TODO: make sure to use correct table name here
    input_gdf[export_columns].to_sql(
        "osm_building_area_2023_urban_centers_grid",
        con=con,
        if_exists="append",
    )
    logging.info("updated OSM stats for grid in postgres table.")


if __name__ == "__main__":
    """python scripts/update_osm_building_stats_grid_2023.py"""

    urban_center_ids = get_urban_center_ids()

    for i, urban_center_id in enumerate(urban_center_ids):
        # if urban_center_id <= 6699:
        #    # skip the urban centers that we've already processed
        #    continue

        logging.info(f"start update for urban_center_id: {urban_center_id}")

        # run query for urban centers grid
        grid_df = get_grid_geometries(urban_center_id)
        grid_df["region"] = "region_" + grid_df["grid_fid"].astype(str)
        grid_df.set_index("region", inplace=True)
        results_df = query_ohsome_api(grid_df)
        logging.info(f"queried ohsome api urban centers grid for {urban_center_id}")
        results_df.reset_index(inplace=True)
        results_df.set_index("boundary", inplace=True)
        results_df.drop(columns=["index"], inplace=True)

        join_df = grid_df.join(results_df)
        join_df["value"] = join_df["value"] / (1000 * 1000)
        join_df["year"] = "osm_building_area_sqkm_" + join_df["timestamp"].dt.year.astype(str)

        new_df = pd.pivot_table(join_df, values='value', columns=["year"], index=['grid_fid', 'urban_center_id'])
        insert_into_postgres_grid(new_df)
        logging.info(f"finished update for urban_center_id: {urban_center_id}")
