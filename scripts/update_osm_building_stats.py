import logging
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
        params={"urban_center_id": urban_center_id},
        geom_col="geom"
    )
    df.reset_index(inplace=True)
    return df


def query_ohsome_api(input_gdf, filter_str="building=* and geometry:polygon"):
    response = client.elements.area.groupByBoundary.post(
        bpolys=input_gdf,
        filter=filter_str,
        time="2008-01-01/2022-01-01/P1Y",  # TODO: adjust timestamp for 2023
    )
    results_df = response.as_dataframe()
    results_df.reset_index(inplace=True)
    return results_df


def insert_into_postgres(input_gdf):
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    export_columns = [
        "urban_center_id",
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
    input_gdf[export_columns].to_sql(
        "osm_building_area_urban_centers_updated",
        con=con,
        if_exists="append",
    )
    logging.info("updated OSM stats in postgres table.")


if __name__ == "__main__":
    """python scripts/update_osm_building_stats.py"""

    urban_center_ids = [
        3369,
        4417,
        9657,
        10716,
        12270,
        12451,
        12456
    ]

    for urban_center_id in urban_center_ids:
        logging.info(f"start update for urban_center_id: {urban_center_id}")
        urban_centers_df = get_input_geometries(urban_center_id)

        results_df = query_ohsome_api(urban_centers_df)

        urban_centers_df["osm_building_area_sqkm_2022"] = float(
            results_df.loc[results_df["timestamp"] == '2022-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2021"] = float(
            results_df.loc[results_df["timestamp"] == '2021-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2020"] = float(
            results_df.loc[results_df["timestamp"] == '2020-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2019"] = float(
            results_df.loc[results_df["timestamp"] == '2019-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2018"] = float(
            results_df.loc[results_df["timestamp"] == '2018-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2017"] = float(
            results_df.loc[results_df["timestamp"] == '2017-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2016"] = float(
            results_df.loc[results_df["timestamp"] == '2016-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2015"] = float(
            results_df.loc[results_df["timestamp"] == '2015-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2014"] = float(
            results_df.loc[results_df["timestamp"] == '2014-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2013"] = float(
            results_df.loc[results_df["timestamp"] == '2013-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2012"] = float(
            results_df.loc[results_df["timestamp"] == '2012-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2011"] = float(
            results_df.loc[results_df["timestamp"] == '2011-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2010"] = float(
            results_df.loc[results_df["timestamp"] == '2010-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2009"] = float(
            results_df.loc[results_df["timestamp"] == '2009-01-01']["value"]) / (1000 * 1000)
        urban_centers_df["osm_building_area_sqkm_2008"] = float(
            results_df.loc[results_df["timestamp"] == '2008-01-01']["value"]) / (1000 * 1000)

        insert_into_postgres(urban_centers_df)
