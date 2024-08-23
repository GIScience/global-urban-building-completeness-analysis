import logging
import pathlib

import geopandas as gpd
import pandas as pd


def create_full_info_uc(inputfile_uc, layer_uc, inputfile_grid, layer_grid):
    grid_df = gpd.read_file(inputfile_grid, layer=layer_grid)
    grid_sum = (
        grid_df[
            [
                "urban_center_id",
                "ghs_pop_2023",
                "worldcover_2021_built_up_sqkm",
                "worldcover_2021_tree_cover_sqkm",
                "worldcover_2021_sparse_vegetation_sqkm",
                "selected_road_length_km",
                "reference_building_area_sqkm",
                "prediction",
                "osm_building_area_sqkm_2008_01",
                "osm_building_area_sqkm_2009_01",
                "osm_building_area_sqkm_2010_01",
                "osm_building_area_sqkm_2011_01",
                "osm_building_area_sqkm_2012_01",
                "osm_building_area_sqkm_2013_01",
                "osm_building_area_sqkm_2014_01",
                "osm_building_area_sqkm_2015_01",
                "osm_building_area_sqkm_2016_01",
                "osm_building_area_sqkm_2017_01",
                "osm_building_area_sqkm_2018_01",
                "osm_building_area_sqkm_2019_01",
                "osm_building_area_sqkm_2020_01",
                "osm_building_area_sqkm_2021_01",
                "osm_building_area_sqkm_2022_01",
                "osm_building_area_sqkm_2023_01",
                "osm_building_area_sqkm_2024_01",
                "osm_building_area_sqkm_2024_05",
            ]
        ]
        .groupby("urban_center_id")
        .sum()
    )

    grid_avg = (
        grid_df[
            [
                "urban_center_id",
                "shdi_2021",
                "vnl_2023",
                "prediction_osm_completeness_2008_01",
                "prediction_osm_completeness_2009_01",
                "prediction_osm_completeness_2010_01",
                "prediction_osm_completeness_2011_01",
                "prediction_osm_completeness_2012_01",
                "prediction_osm_completeness_2013_01",
                "prediction_osm_completeness_2014_01",
                "prediction_osm_completeness_2015_01",
                "prediction_osm_completeness_2016_01",
                "prediction_osm_completeness_2017_01",
                "prediction_osm_completeness_2018_01",
                "prediction_osm_completeness_2019_01",
                "prediction_osm_completeness_2020_01",
                "prediction_osm_completeness_2021_01",
                "prediction_osm_completeness_2022_01",
                "prediction_osm_completeness_2023_01",
                "prediction_osm_completeness_2024_01",
                "prediction_osm_completeness_2024_05",
            ]
        ]
        .groupby("urban_center_id")
        .mean()
    )
    del grid_df

    grid_sum = pd.merge(
        grid_sum,
        grid_avg,
        on="urban_center_id",
        how="left",
    )
    del grid_avg

    uc_df = gpd.read_file(inputfile_uc, layer=layer_uc)
    uc_df = pd.merge(
        uc_df,
        grid_sum,
        on="urban_center_id",
        how="left",
    )
    del grid_sum

    uc_df.to_file("../abgabe.gpkg", layer="uc_full_info_V2024", driver="GPKG")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
    )

    inputfile_uc = pathlib.Path("../abgabe.gpkg")
    layer_uc = "uc_2025"

    inputfile_grid = pathlib.Path("../abgabe.gpkg")
    layer_grid = "grid_full_info_V2024"

    create_full_info_uc(inputfile_uc, layer_uc, inputfile_grid, layer_grid)
