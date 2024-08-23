import logging
import time

import geojson
import geopandas as gpd
import pandas as pd
import psycopg2

uc_layers = "jrc_uc_wgs84.gpkg"
def get_urban_center_ids(dns):
    df_uc = gpd.read_file(uc_layers, layer='uc_2025')
    urban_center_ids = []
    query = """
    WITH bpoly AS (
    SELECT
        ST_Setsrid (ST_GeomFromGeoJSON (%s), 4326) AS geom
    )
    SELECT
        -- ratio of area within coverage (empty if outside, between 0-1 if intersection)
        ST_Area (ST_Intersection (bpoly.geom, coverage.geom)) / ST_Area (bpoly.geom) as area_ratio,
        ST_AsGeoJSON (ST_Intersection (bpoly.geom, coverage.geom)) AS geom
    FROM
        bpoly,
        {table_name} coverage
    WHERE
        ST_Intersects (bpoly.geom, coverage.geom)
    """

    for id in df_uc.index:
        logging.info(f"checking coverage for UC_ID: {id}")
        feature = df_uc.loc[id]
        geom = geojson.dumps(feature.geometry)
        for try_no in range(4):
            try:
                with psycopg2.connect(dns) as con:
                    with con.cursor() as cur:
                        cur.execute(query.format(table_name = "microsoft_roads_coverage_simple"), (geom,))
                        res = cur.fetchone()
                        if res:
                            urban_center_ids.append(feature.ID_UC_G0)
            except Exception as e:
                if try_no < 4 - 1:
                    logging.warning(
                        f"An error occured: UC ID {id}, Retrying. Errormessage: {e}"
                    )
                    # wait 30 seconds before retrying
                    time.sleep(30)
                    continue
                else:
                    logging.error(
                        f"Unable to query Data for: UC {id}, Message: {e}"
                    )
                    exit()
            break

    logging.info(f"found {len(urban_center_ids)} urban centers withing coverage region")
    return urban_center_ids

def import_grid_layer(urban_center_id):
    gdf = gpd.read_file(uc_layers, layer="uc_grid", where=f"ID_UC_G0='{urban_center_id}'")
    return gdf

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")

    dns = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        host="",
        port="",
        database="db",
        user="user",
        password="password",
    )
    urban_center_ids = get_urban_center_ids(dns)
    query = """
    WITH bpoly AS (
    SELECT
        -- split mutlipolygon into list of polygons for more efficient processing
        (ST_DUMP (ST_Setsrid (ST_GeomFromGeoJSON (%s), 4326))).geom AS geom
    )
    SELECT
        SUM(cr.covered),
        SUM(cr.length)
    FROM
        bpoly
        LEFT JOIN {table_name} cr ON ST_Intersects (cr.midpoint, bpoly.geom);
    """
    collected_table = []
    for urban_center_id in urban_center_ids:
        logging.info(f"start update for urban_center_id: {urban_center_id}")

        # import grid for id
        grid_df = import_grid_layer(urban_center_id)
        for i in grid_df.index:
            feature = grid_df.iloc[i]

            geom = geojson.dumps(feature.geometry)
            for try_no in range(4):
                try:
                    with psycopg2.connect(dns) as con:
                        with con.cursor() as cur:
                            cur.execute(query.format(table_name = "microsoft_roads_midpoint"), (geom,))
                            res = cur.fetchone()
                            if res[1] is None or res is None:
                                res = 0
                            else:
                                res = res[1]/1000
                            grid_df.at[i, "microsoft_roads_length"] = res
                except Exception as e:
                    if try_no < 4 - 1:
                        logging.warning(
                            f"An error occured: UC ID {urban_center_id}, Index {i}, Retrying. Errormessage: {e}"
                        )
                        # wait 30 seconds before retrying
                        time.sleep(30)
                        continue
                    else:
                        logging.error(
                            f"Unable to query Data for: UC {urban_center_id}, Index {i}. Message: {e}"
                        )
                        exit()
                break
        collected_table.append(grid_df)
        logging.info(f"finished update for urban_center_id: {urban_center_id}")
    uc_ms_road_length = pd.concat(collected_table)
    uc_ms_road_length.to_csv("uc_ms_road_length.csv")
