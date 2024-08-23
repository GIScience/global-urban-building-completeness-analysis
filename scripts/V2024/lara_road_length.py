import logging

import geopandas as gpd
import pandas as pd

#load geopackage
uc_layers = ("../data/jrc_uc_wgs84.gpkg")

#get urban center ids
def get_urban_center_ids():
    df_uc = gpd.read_file(uc_layers, layer='uc_2025')
    urban_center_ids = df_uc["ID_UC_G0"].values
    logging.info(f"got {len(urban_center_ids)} urban centers")

    return urban_center_ids

#import grid for every single id, note: takes a long time, other function is better but does not work!!!
''' only needed if python/geopaandas/fiona versions are not high enough
def get_each_grid(uc_layers, urban_center_id):
    df_grid = gpd.read_file(uc_layers, layer='uc_grid')
    filtered_gdf = df_grid[df_grid['ID_UC_G0'] == urban_center_id]
    return filtered_gdf
    filtered_gdf.reset_index(inplace=True)
    return filtered_gdf
    '''

#import grid of a single urban center id wuth gpd
def import_grid_layer(urban_center_id):
    gdf = gpd.read_file(uc_layers, layer="uc_grid", where=f"ID_UC_G0='{urban_center_id}'")
    return gdf

#query ohsome api for road_length per grid
from ohsome import OhsomeClient

client = OhsomeClient()

def query_ohsome_api(grid_df, filter_str):
    # make sure to set correct end timestamp here
    response = client.elements.length.groupByBoundary.post(
        bpolys=grid_df,
        filter=filter_str,
        #timestamps 1 year interval since 2008 AND most recent value (2024-05-26)
        time="2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2024-05-26"
        )
    results_df = response.as_dataframe()
    results_df.reset_index(inplace=True)
    return results_df


#define parameters
pivot_table = []
urban_center_ids = get_urban_center_ids()

#run all functions
for urban_center_id in urban_center_ids:

    logging.info(f"start update for urban_center_id: {urban_center_id}")

    # run query for urban centers grid
    grid_df = import_grid_layer(urban_center_id)
    grid_df["region"] = "region_" + grid_df["identifier"].astype(str)
    grid_df.set_index("region", inplace=True)

    #query ohsome api
    filter_str = "highway in (motorway, trunk, motorway_link, trunk_link, primary, primary_link, secondary, secondary_link, tertiary, tertiary_link, unclassified, residential) and type:way"
    results_df = query_ohsome_api(grid_df, filter_str)
    logging.info(f"queried ohsome api urban centers grid for {urban_center_id}")

    #turn into df
    results_df.reset_index(inplace=True)
    results_df.set_index("boundary", inplace=True)

    join_df = grid_df.join(results_df)
    #change unit from m to km
    join_df["value"] = join_df["value"] / 1000
    #create column for every year (with month so that latest entry is included as well)
    join_df["year"] = "osm_road_length_km_" + join_df["timestamp"].dt.strftime('%Y-%m')

    #add all results from the for loop to a pivot table
    new_df = pd.pivot_table(join_df, values='value', columns=["year"], index=['identifier', 'ID_UC_G0'])
    pivot_table.append(new_df)
    logging.info(f"finished update for urban_center_id: {urban_center_id}")


#add each result of the for-loop to this table
uc_road_length = pd.concat(pivot_table)
#save as csv
uc_road_length.to_csv("uc_road_length_per_grid.csv")

##later on:join identifier and fid!
