import logging
import pathlib

import geopandas as gpd
import pandas as pd


def create_full_info_uc(inputfile_uc, layer_uc, inputfile_grid, layer_grid):
    grid_df = gpd.read_file(inputfile_grid, layer=layer_grid)
    grid_sum = (
        grid_df[
            [
                "ID_UC_G0",
                "GHS_POP",
                "wc_built_up_sqkm",
                "wc_tree_cover_sqkm",
                "wc_sparse_vegetation_sqkm",
                "selected_road_length_km",
                "reference_building_area_sqkm",
                "prediction_improved_sqkm",
                "osm_building_area_sqkm_2008-01",
                "osm_building_area_sqkm_2009-01",
                "osm_building_area_sqkm_2010-01",
                "osm_building_area_sqkm_2011-01",
                "osm_building_area_sqkm_2012-01",
                "osm_building_area_sqkm_2013-01",
                "osm_building_area_sqkm_2014-01",
                "osm_building_area_sqkm_2015-01",
                "osm_building_area_sqkm_2016-01",
                "osm_building_area_sqkm_2017-01",
                "osm_building_area_sqkm_2018-01",
                "osm_building_area_sqkm_2019-01",
                "osm_building_area_sqkm_2020-01",
                "osm_building_area_sqkm_2021-01",
                "osm_building_area_sqkm_2022-01",
                "osm_building_area_sqkm_2023-01",
                "osm_building_area_sqkm_2024-01",
                "osm_building_area_sqkm_2024-05",
            ]
        ]
        .groupby("ID_UC_G0")
        .sum()
    )

    grid_avg = (
        grid_df[
            [
                "ID_UC_G0",
                "shdi",
                "vnl_mean",
                "osm_completeness_2008_01",
                "osm_completeness_2009_01",
                "osm_completeness_2010_01",
                "osm_completeness_2011_01",
                "osm_completeness_2012_01",
                "osm_completeness_2013_01",
                "osm_completeness_2014_01",
                "osm_completeness_2015_01",
                "osm_completeness_2016_01",
                "osm_completeness_2017_01",
                "osm_completeness_2018_01",
                "osm_completeness_2019_01",
                "osm_completeness_2020_01",
                "osm_completeness_2021_01",
                "osm_completeness_2022_01",
                "osm_completeness_2023_01",
                "osm_completeness_2024_01",
                "osm_completeness_2024_05",
            ]
        ]
        .groupby("ID_UC_G0")
        .mean()
    )
    del grid_df

    grid_sum = pd.merge(
        grid_sum,
        grid_avg,
        on="ID_UC_G0",
        how="left",
    )
    del grid_avg

    uc_df = gpd.read_file(inputfile_uc, layer=layer_uc)
    uc_df = pd.merge(
        uc_df,
        grid_sum,
        on="ID_UC_G0",
        how="left",
    )
    del grid_sum

    uc_df.to_file("../full_info_uc.gpkg", layer="full_info_uc", driver="GPKG")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
    )

    inputfile_uc = pathlib.Path("../jrc_uc_wgs84.gpkg")
    layer_uc = "uc_2025"

    inputfile_grid = pathlib.Path("../abgabe.gpkg")
    layer_grid = "grid_full_info_V2024"

    create_full_info_uc(inputfile_uc, layer_uc, inputfile_grid, layer_grid)
