import logging
import pathlib
from random import sample

import geopandas as gpd
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import RobustScaler


def load_urban_centers_grid(input_file, layer_grid):
    df = gpd.read_file(input_file, layer=layer_grid)

    df["region_wb_cat"] = pd.Categorical(df["region_wb"])
    df["region_code"] = df.region_wb_cat.cat.codes

    df["shdi"].fillna((df["shdi"].mean()), inplace=True)
    df["selected_road_length_km"].fillna(
        (df["selected_road_length_km"].mean()), inplace=True
    )

    for column in df.columns:
        if column in [
            "external_reference_building_area_sqkm",
            "microsoft_building_area_sqkm",
            "reference_building_area_sqkm",
            "reference_osm_completeness",
            "region_wb",
            "region_wb_cat",
            "region_code",
        ]:
            continue

        df[column] = df[column].fillna(0)

    logging.info(len(df))
    return df


def get_urban_center_centroids(inputfile, layer_uc, grid_df):
    """Get the centroids of the urban centers."""
    # returns message, that centroids are likely incorrect because the data is in a geographic CRS. is reprojecting neccessary??
    copy_df = grid_df[
        ["ID_UC_G0", "osm_building_area_sqkm_2024-05", "reference_building_area_sqkm"]
    ]
    copy_df = copy_df.groupby("ID_UC_G0").sum()
    copy_df["reference_osm_completeness"] = round(
        copy_df["osm_building_area_sqkm_2024-05"]
        / copy_df["reference_building_area_sqkm"],
        3,
    )

    uc_grid = gpd.read_file(inputfile, layer=layer_uc)
    uc_grid = pd.merge(
        uc_grid,
        copy_df[["reference_building_area_sqkm", "reference_osm_completeness"]],
        on="ID_UC_G0",
        how="left",
    )

    # filter the columns out, where the (training) data might not be complete
    df = uc_grid[
        (uc_grid["reference_osm_completeness"] < 1.5)
        & (uc_grid["reference_building_area_sqkm"].notnull())
    ]

    # create centroids
    df_reprojected = df.to_crs("+proj=cea")
    df["x"] = df_reprojected.centroid.to_crs(df.crs).x
    df["y"] = df_reprojected.centroid.to_crs(df.crs).y

    logging.info(f"got {len(df)} urban centers with centroid coordinates")

    return df[["ID_UC_G0", "x", "y"]]


def spatial_train_test_split_cluster(df, cluster_label, n=0):
    """Split based on sample location."""

    train_indices = df.index[
        (df["cluster"] != cluster_label)
        & (df["reference_building_area_sqkm"] > 0)  # this includes OSM data
    ].tolist()

    test_indices = df.index[
        (df["cluster"] == cluster_label)
        & (
            df["reference_building_area_sqkm"] > 0
        )  # this includes only reference data and osm data
    ].tolist()

    if n > 0:
        if n > len(train_indices):
            n = len(train_indices)
        train_indices = sample(train_indices, n)

    return train_indices, test_indices


def kmeans_cluster_urban_centers(df, x, y, n_clusters):
    """create location based clusters"""
    columns = [x, y]
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[columns])
    df["cluster"] = kmeans.labels_
    return df, n_clusters


def estimate_model_performance(inputfile, layer_uc, layer_prediction, n_clusters=10):
    df = load_urban_centers_grid(inputfile, layer_prediction)

    urban_centers_df = get_urban_center_centroids(inputfile, layer_uc, df)
    cluster_df, n_clusters = kmeans_cluster_urban_centers(
        urban_centers_df, "x", "y", n_clusters
    )
    df = df.join(cluster_df.set_index("ID_UC_G0"), on="ID_UC_G0", how="inner")
    region_groups = list(range(0, n_clusters))

    # df for model
    df_model = df.reset_index()

    # feature scaling
    sc = RobustScaler()
    X = sc.fit_transform(df_model[COVARIATE_COLUMNS].values)
    y = df_model[REFERENCE_COLUMN].values

    for r in range(0, 5):
        logging.info(f"start round: {r+1}")
        for i, regions in enumerate(region_groups):
            logging.info(f"processing round {r+1}: {i + 1}/{len(region_groups)}")

            # max 50k samples per split
            train_indices, test_indices = spatial_train_test_split_cluster(
                df_model, regions, n=50000
            )

            X_train = X[train_indices]
            y_train = y[train_indices]

            X_test = X[test_indices]
            y_test = y[test_indices]

            # check if there are reference samples
            if len(y_test) < 1:
                logging.info(f"no test samples: {regions}")
                continue
            elif len(y_train) < 1:
                logging.info(f"no training samples: {regions}")
                continue

            regressor = RandomForestRegressor(n_estimators=50)
            regressor.fit(X_train, y_train)
            logging.info("fitted model")

            y_pred = regressor.predict(X_test)
            logging.info("predicted model")

            df_test = df_model.iloc[test_indices]

            df_test["repeat"] = r
            df_test["prediction"] = y_pred
            df_test["reference_building_area_sqkm"] = y_test
            df_test["split"] = i

            # save predictions to Geopackage
            df_export = df_test[
                [
                    "ID_UC_G0",
                    "identifier",
                    "region_wb",
                    "repeat",
                    "split",
                    "prediction",
                    "reference_building_area_sqkm",
                    "geometry",
                ]
            ]
            if r == 0 and i == 0:
                df_export.to_file(
                    inputfile,
                    layer=f"performance_{n_clusters}_clusters_reference_and_osm",
                    driver="GPKG",
                )
            else:
                df_export.to_file(
                    inputfile,
                    layer=f"performance_{n_clusters}_clusters_reference_and_osm",
                    driver="GPKG",
                    mode="a",
                )

            del df_export

            logging.info("saved predictions to Geopackage.")


if __name__ == "__main__":
    """python scripts/model_performance.py"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
    )

    inputfile = pathlib.Path("../jrc_uc_wgs84.gpkg")
    layer_uc = "uc_2025"
    layer_grid = "uc_grid"
    layer_grid_prediction = "prediction_improved"

    COVARIATE_COLUMNS = [
        "wc_built_up_sqkm",
        "wc_tree_cover_sqkm",
        "wc_sparse_vegetation_sqkm",
        "GHS_POP",
        "vnl_mean",
        "shdi",
        "selected_road_length_km",
        "region_code",
    ]

    REFERENCE_COLUMN = "reference_building_area_sqkm"

    estimate_model_performance(
        inputfile, layer_uc, layer_grid_prediction, n_clusters=20
    )
