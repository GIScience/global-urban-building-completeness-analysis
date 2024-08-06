import logging
import pathlib

import geopandas as gpd
import pandas as pd
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


def get_outliers(df, uc_file, layer_UC, threshold=0.005):
    copy_df = df[["ID_UC_G0", "osm_building_area_sqkm_2024-05", "prediction_sqkm"]]
    copy_df = copy_df.groupby("ID_UC_G0").sum()

    uc_df = gpd.read_file(uc_file, layer=layer_UC)
    uc_df = pd.merge(
        uc_df,
        copy_df[["osm_building_area_sqkm_2024-05", "prediction_sqkm"]],
        on="ID_UC_G0",
        how="left",
    )

    uc_df = uc_df.to_crs("ESRI:54009")
    uc_df["area"] = uc_df.geometry.area / (1000 * 1000)

    # select all rows where area is greater than threshold
    uc_df_subset = uc_df[
        (uc_df["osm_building_area_sqkm_2024-05"] - uc_df["prediction_sqkm"])
        > uc_df["area"] * threshold
    ]

    outliers = uc_df_subset["ID_UC_G0"].values
    logging.info(
        f"got {len(outliers)} urban center ids with prediction below threshold (th = {threshold})"
    )
    return outliers


def run_prediction(training_data, uc_file, layer_grid, layer_UC):
    logging.info("start workflow")

    df = load_urban_centers_grid(uc_file, layer_grid)
    logging.info("got dataframe")

    if training_data == "reference_and_osm":
        urban_center_ids = get_outliers(df, uc_file, layer_UC, threshold=0.005)
        df[f"reference_building_area_sqkm_initial"] = df[f"reference_building_area_sqkm"]
        df.loc[
            (df["ID_UC_G0"].isin(urban_center_ids)), "reference_building_area_sqkm"
        ] = df["osm_building_area_sqkm_2024-05"]

        df["reference_completeness_area_sqkm"] = round(
            df["osm_building_area_sqkm_2024-05"] / df["reference_building_area_sqkm"], 3
        )

    df_train = df[
        (df["reference_building_area_sqkm"] > 0)
        &
        # avoid urban centers for which training data might not be complete
        (df["reference_osm_completeness"] < 1.5)
    ]
    logging.info(f"training samples: {len(df_train)}")

    # Feature Scaling
    X_train = df_train[COVARIATE_COLUMNS].values
    y_train = df_train[REFERENCE_COLUMN].values
    sc = RobustScaler()
    X = df[COVARIATE_COLUMNS].values
    X_input = sc.fit_transform(X)
    X_train = sc.transform(X_train)
    logging.info("scaled features.")

    # fit model and predict
    regressor = RandomForestRegressor(n_estimators=50)
    regressor.fit(X_train, y_train)
    logging.info("fitted model")

    y_pred = regressor.predict(X_input)
    logging.info("predicted model")

    # get importance
    importance = regressor.feature_importances_
    # summarize feature importance
    feature_importance = {}
    for i, v in enumerate(importance):
        feature_importance[COVARIATE_COLUMNS[i]] = v
    logging.info(feature_importance)

    gdf_temp = df.drop(
        columns=[
            "region_wb_cat",
            "region_code",
        ],
        errors="ignore",
    )
    if layer_grid != "prediction":
        gdf_temp["prediction_sqkm"] = y_pred
        gdf_temp.to_file(uc_file, layer="prediction", driver="GPKG")
    else:
        gdf_temp["prediction_improved_sqkm"] = y_pred
        gdf_temp["osm_completeness"] = (
            (
                gdf_temp["osm_building_area_sqkm_2024-05"]
                / gdf_temp["prediction_improved_sqkm"]
            )
            * 100
        ).round(3)
        gdf_temp.to_file(uc_file, layer="prediction_improved", driver="GPKG")
    logging.info("saved predictions to GPKG.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
    )

    uc_file = pathlib.Path("../jrc_uc_wgs84.gpkg")
    layer_UC = "uc_2025"
    layer_grid = "uc_grid"
    layer_grid_prediction = "prediction"

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

    """python scripts/run_prediction.py reference_and_osm"""

    # training_data = "reference"
    training_data = "reference_and_osm"

    if training_data == "reference":
        run_prediction(training_data, uc_file, layer_grid, layer_UC)
    elif training_data == "reference_and_osm":
        run_prediction(training_data, uc_file, layer_grid_prediction, layer_UC)
    else:
        print("please pass a valid argument: 'reference' or 'reference_and_osm'")
