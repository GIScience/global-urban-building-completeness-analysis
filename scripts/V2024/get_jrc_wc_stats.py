import logging
import os
import pathlib
import shutil
import time

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio
from pyproj import Transformer
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info
from rasterio.mask import mask
from rasterio.merge import merge
from rasterstats import zonal_stats
from shapely.geometry import box
from terracatalogueclient import Catalogue

USERNAME = "username"
PASSWORD = "password"
NO_OF_RETRIES = 4


def get_urban_center_ids(input_file: str, input_layer) -> list:
    logging.info("reading urban centers")
    df_uc = gpd.read_file(input_file, layer=input_layer)
    urban_center_ids = df_uc["ID_UC_G0"].values
    logging.info(f"got {len(urban_center_ids)} urban centers")

    return urban_center_ids


def download_wc_tile(
    catalogue: Catalogue,
    box_geom: box,
    path_wc_scratch: pathlib.Path,
    uc_feature: gpd.GeoSeries,
) -> None:
    for tryno in range(NO_OF_RETRIES):
        try:
            logging.info("Downloading WC tile for 2021")
            products_2021 = catalogue.get_products(
                "urn:eop:VITO:ESA_WorldCover_10m_2021_V2", geometry=box_geom
            )
            catalogue.download_products(products_2021, path_wc_scratch, force=True)
        except Exception as e:
            if tryno < NO_OF_RETRIES - 1:
                logging.warning(
                    f"An error occured: UC {uc_feature.ID_UC_G0}. Retrying to Download. Errormessage: {e}"
                )
                # wait 10 seconds before retrying
                time.sleep(30)
                continue
            else:
                logging.error(
                    f"Unable to Download WC Data for UC {uc_feature.ID_UC_G0}. Message: {e}"
                )
                exit()
        break

    logging.info(f"Finished download of WorldCover data for UC {uc_feature.ID_UC_G0}.")


def clip_raster(
    path_wc_scratch: pathlib.Path, box_geom: box, path_wc_clipped: pathlib.Path
) -> None:
    for tile in list(path_wc_scratch.rglob("*InputQuality.tif")):
        os.remove(tile)
    for tile in list(path_wc_scratch.rglob("*Map.tif")):
        with rio.open(tile) as src:
            try:
                out_image, out_transform = mask(
                    src, [box_geom], crop=True, all_touched=True
                )
                out_meta = src.meta.copy()  # copy the metadata of the source Raster
            except ValueError as e:
                logging.error(
                    f"Unable to clip raster for UC {tile}. Message: {e}. Skipping and "
                    f"removing tile."
                )
                os.remove(tile)
                continue

        # update raster metadata
        out_meta.update(
            {
                "driver": "Gtiff",
                "height": out_image.shape[1],  # height starts with shape[1]
                "width": out_image.shape[2],  # width starts with shape[2]
                "transform": out_transform,
            }
        )

        # store clipped raster
        out_name = str(tile.name)
        out_path = pathlib.Path(path_wc_clipped / out_name)
        with rio.open(out_path, "w", **out_meta) as dst:
            dst.write(out_image)
        os.remove(tile)


def merge_tiles(tiles: list, outpath: pathlib.Path, uc_id: int) -> None:
    raster_to_mosiac = []
    for tile in tiles:
        raster = rio.open(tile)
        raster_to_mosiac.append(raster)

    mosaic, output = merge(raster_to_mosiac)

    output_meta = raster.meta.copy()
    output_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": output,
        }
    )
    output_path = pathlib.Path(outpath / f"WorldCover_UC_{uc_id}.tif")
    with rio.open(output_path, "w", **output_meta) as m:
        m.write(mosaic)

    for file in tiles:
        os.remove(file)


def calc_cell_size(tile: pathlib.Path) -> float:
    with rio.open(tile) as src:
        tile_corner_coords = src.bounds
        # query UTM code for that coordinate
        utm_crs_list = query_utm_crs_info(
            datum_name="WGS 84",
            area_of_interest=AreaOfInterest(
                west_lon_degree=tile_corner_coords[0],
                south_lat_degree=tile_corner_coords[1],
                east_lon_degree=tile_corner_coords[0],
                north_lat_degree=tile_corner_coords[1],
            ),
        )
        utm_code = utm_crs_list[0].code

        transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{utm_code}")

        # cell size in degree
        x_cell_size = src.res[0]
        y_cell_size = src.res[1]

        # south-western point
        lon1 = tile_corner_coords[0]
        lat1 = tile_corner_coords[1]

        # one pixel to east
        lon2 = tile_corner_coords[0] + x_cell_size
        lat2 = tile_corner_coords[1]

        # one pixel to north
        lon3 = tile_corner_coords[0]
        lat3 = tile_corner_coords[1] + y_cell_size

        x1, y1 = transformer.transform(lat1, lon1)
        x2, y2 = transformer.transform(lat2, lon2)
        x3, y3 = transformer.transform(lat3, lon3)

        distance_m_lon = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distance_m_lat = np.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

        cell_size = distance_m_lon * distance_m_lat

    return cell_size


def main(
    input_file: pathlib.Path, layer_uc: str, layer_grid: str, csv_output: pathlib.Path
) -> None:
    # read in UC areas
    df_uc = gpd.read_file(input_file, layer=layer_uc)

    ## Downloading WorldCover data  for each urban center

    # Authenticate to the Terrascope platform and create catalogue object
    catalogue = Catalogue().authenticate_non_interactive(
        username=USERNAME, password=PASSWORD
    )

    collected_table_grid = []

    for index in df_uc.index:
        path_wc_scratch = pathlib.Path("./wc_scratch/")
        if not os.path.exists(path_wc_scratch):
            os.makedirs(path_wc_scratch)

        uc_feature = df_uc.loc[index]
        logging.info(f"Working on urban center {uc_feature.ID_UC_G0} of {len(df_uc)}.")
        bounds = uc_feature.geometry.bounds
        box_geom = box(*bounds)

        # Download each WorldCover tile
        download_wc_tile(catalogue, box_geom, path_wc_scratch, uc_feature)

        # Clip raster to UC Bounding Box
        logging.info("Clip raster to UC Bounding Box.")
        path_wc_clipped = pathlib.Path("./wc_clipped/")
        if not os.path.exists(path_wc_clipped):
            os.makedirs(path_wc_clipped)
        clip_raster(path_wc_scratch, box_geom, path_wc_clipped)

        # Merge clipped rasters if necessary
        path_wc_map = pathlib.Path("./wc_map/")
        if not os.path.exists(path_wc_map):
            os.makedirs(path_wc_map)
        if len(list(path_wc_clipped.rglob("*Map.tif"))) > 1:
            logging.info("Merging clipped rasters.")
            merge_tiles(
                list(path_wc_clipped.rglob("*Map.tif")),
                path_wc_map,
                uc_feature.ID_UC_G0,
            )
        else:
            for file in path_wc_clipped.rglob("*_Map.tif"):
                new_name = pathlib.Path(f"WorldCover_UC_{uc_feature.ID_UC_G0}.tif")
                os.rename(file, path_wc_map / new_name)

        # clean up scratch dirs
        shutil.rmtree(path_wc_scratch)
        shutil.rmtree(path_wc_clipped)

        logging.info(f"Finished creation of WC Map for UC {uc_feature.ID_UC_G0}.")

        # import grid for this UC
        grid_df = gpd.read_file(
            input_file, layer=layer_grid, where=f"ID_UC_G0='{uc_feature.ID_UC_G0}'"
        )
        if len(list(path_wc_map.rglob("*.tif"))) > 1:
            logging.warning(
                "Multiple maps in dir for zonal stats! This should not be the case!"
            )

        ## Calculate zonal statistics per UC for each grid cell

        for tile in list(path_wc_map.rglob("*.tif")):
            # get cell area for WC pixel
            area_per_wc_cell = calc_cell_size(tile)
            # calc pixel count per classes
            stats_df = pd.DataFrame(
                zonal_stats(vectors=grid_df["geometry"], raster=tile, categorical=True)
            )
            # join gdf with zonal stats
            gdf_temp = grid_df.join(stats_df, how="left")
            # convert pixel counts to sqkm
            if 50 not in gdf_temp.columns:
                gdf_temp[50] = 0
            if 10 not in gdf_temp.columns:
                gdf_temp[10] = 0
            if 60 not in gdf_temp.columns:
                gdf_temp[60] = 0
            gdf_temp["built_up_sqkm"] = gdf_temp[50] * area_per_wc_cell / (1000 * 1000)
            gdf_temp["tree_cover_sqkm"] = (
                gdf_temp[10] * area_per_wc_cell / (1000 * 1000)
            )
            gdf_temp["sparse_vegetation_sqkm"] = (
                gdf_temp[60] * area_per_wc_cell / (1000 * 1000)
            )
            # Fill nan values with 0
            gdf_temp["built_up_sqkm"] = gdf_temp["built_up_sqkm"].fillna(0)
            gdf_temp["tree_cover_sqkm"] = gdf_temp["tree_cover_sqkm"].fillna(0)
            gdf_temp["sparse_vegetation_sqkm"] = gdf_temp["sparse_vegetation_sqkm"].fillna(0)

            # drop pixel count columns
            gdf_temp = gdf_temp.drop(
                columns=[
                    10,
                    20,
                    30,
                    40,
                    50,
                    60,
                    70,
                    80,
                    90,
                    95,
                    100,
                ],
                errors="ignore",
            )
            os.remove(tile)
        collected_table_grid.append(gdf_temp)
        logging.info(f"finished update for urban_center_id: {uc_feature.ID_UC_G0}")

    logging.info("Finished zonal stats calculation for all urban centers")
    shutil.rmtree(path_wc_map)
    uc_wc_stats = pd.concat(collected_table_grid)
    uc_wc_stats.to_csv(csv_output)


if __name__ == "__main__":
    uc_file = pathlib.Path("../jrc_uc_wgs84.gpkg")
    csv_output = pathlib.Path("./uc_wc_stats.csv")
    layer_UC = "uc_2025"
    layer_grid = "uc_grid"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
    )

    main(uc_file, layer_UC, layer_grid, csv_output)
