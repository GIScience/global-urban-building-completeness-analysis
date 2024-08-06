import logging

import geopandas as gpd
import pandas as pd
from ohsome import OhsomeClient

client = OhsomeClient()

#load geopackage
uc_layers = ("../covariates/jrc_uc_wgs84.gpkg")

def get_urban_center_ids():
    df_uc = gpd.read_file(uc_layers, layer='uc_2025')
    urban_center_ids = df_uc["ID_UC_G0"].values
    logging.info(f"got {len(urban_center_ids)} urban centers")

    return urban_center_ids


'''def get_each_grid(uc_layers, urban_center_id):
    df_grid = gpd.read_file(uc_layers, layer='uc_grid')
    filtered_gdf = df_grid[df_grid['ID_UC_G0'] == urban_center_id]
    filtered_gdf.reset_index(inplace=True)
    return filtered_gdf'''

#try to filter while importing so it does not take as much time
#geopandas
def import_grid_layer(urban_center_id):
    gdf = gpd.read_file(uc_layers, layer="uc_grid", where=f"ID_UC_G0='{urban_center_id}'")
    return gdf


def query_ohsome_api(grid_df, filter_str):
    response = client.elements.area.groupByBoundary.post(
        bpolys=grid_df,
        filter=filter_str,
        time="2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2024-05-26"
    )
    results_df = response.as_dataframe()
    results_df.reset_index(inplace=True)
    return results_df



#run all functions


if __name__ == "__main__":
    urban_center_ids = get_urban_center_ids()
    pivot_table = []

    for urban_center_id in urban_center_ids:

        logging.info(f"start update for urban_center_id: {urban_center_id}")

        #import grid for id
        grid_df = import_grid_layer(urban_center_id)
        grid_df["region"] = "region_" + grid_df["identifier"].astype(str)
        grid_df.set_index("region", inplace=True)

        #calculate building area per grid
        filter_str = "building=* and geometry:polygon"
        result_df = query_ohsome_api(grid_df, filter_str)
        logging.info(f"queried ohsome api urban centers grid for {urban_center_id}")

        #turn into dataframe
        result_df.reset_index(inplace=True)
        result_df.set_index("boundary", inplace=True)

        #add both df
        join_df = grid_df.join(result_df)
        #change unit from m to km
        join_df["value"] = join_df["value"] / (1000*1000)
        #create new column
        join_df["year"] = "osm_building_area_sqkm_" + join_df["timestamp"].dt.strftime('%Y-%m')

        #create new table
        new_df = pd.pivot_table(join_df, values='value', columns=["year"], index=['identifier', 'ID_UC_G0'])

        pivot_table.append(new_df)
        print(f"Finished adding values for uc_id: {urban_center_id}.")

    uc_building_area = pd.concat(pivot_table)
    uc_building_area.to_csv("../covariates/uc_building_area_per_grid.csv")
