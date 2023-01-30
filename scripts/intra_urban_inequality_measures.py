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

from segregation.singlegroup import Gini
from libpysal.weights.contiguity import Queen
from esda.moran import Moran

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def load_urban_centers_grid(urban_center_id):
    con = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    query = f"""
        SELECT
            grid_fid as fid
            ,grid_fid
            ,urban_center_id
            ,prediction
            ,case
                when osm_building_area_sqkm_2023 > prediction then prediction
                else osm_building_area_sqkm_2023
            end as osm_building_area_sqkm_2023
            ,prediction_osm_completeness_2023
            ,geom
        FROM prediction_reference_and_osm_urban_centers_grid
        WHERE urban_center_id = %(urban_center_id)s
    """
    df = gpd.GeoDataFrame.from_postgis(
        query,
        con,
        geom_col="geom",
        params={"urban_center_id": urban_center_id}
    ).set_index("fid")
    df.loc[
        df["prediction_osm_completeness_2023"] > 1, "prediction_osm_completeness_2023"
    ] = 1
    df.fillna(0, inplace=True)

    logging.info(f"got {len(df)} grids for urban center {urban_center_id}.")
    return df


def get_all_urban_center_ids(size_threshold=None):
    """Load urban center grids for given urban center id."""
    con = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    query = f"""
       select
         urban_center_id
         ,count(*) as samples
       from prediction_reference_and_osm_urban_centers_grid
       where prediction is not null
       group by urban_center_id
       order by urban_center_id
    """
    df = pd.read_sql(query, con)
    if size_threshold is not None:
        df = df.loc[df["samples"] > size_threshold]

    logging.info(f"got {len(df)} urban center ids.")
    return df["urban_center_id"].to_list()


def run_analysis(df):
    osm_completeness = round(df["osm_building_area_sqkm_2023"].sum() / df["prediction"].sum(), 3)

    # calculate gini
    # need to use adjusted osm_building_area here as gini is not defined otherwise
    index = Gini(
        df[['osm_building_area_sqkm_2023', 'prediction']],
        'osm_building_area_sqkm_2023', 'prediction'
    )
    gini = round(index.statistic, 3)

    # calculate moran's I
    w = Queen.from_dataframe(df)
    w.transform = 'r'
    df = df.loc[~df.index.isin(w.islands)]
    w = Queen.from_dataframe(df)
    w.transform = 'r'

    y = df["prediction_osm_completeness_2023"]
    moran_global = Moran(y, w)
    moran = round(moran_global.I, 3)

    return [urban_center_id, osm_completeness, gini, moran]


if __name__ == "__main__":
    urban_center_ids = get_all_urban_center_ids(size_threshold=25)

    stats_list = []
    for i, urban_center_id in enumerate(urban_center_ids):
        gdf = load_urban_centers_grid(urban_center_id)
        stats = run_analysis(gdf)
        stats_list.append(stats)
        logging.info(f"finished analysis for urban center {urban_center_id}")

    columns = ["urban_center_id", "osm_completeness", "gini", "moran"]
    stats_df = pd.DataFrame(stats_list, columns=columns)

    engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    stats_df.to_sql(
        'inequality_measures_urban_centers',
        engine,
        if_exists='replace',
        index=False
    )
