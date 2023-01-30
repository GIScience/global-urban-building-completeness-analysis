import sys
import logging
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import RobustScaler
from utils import (
    load_urban_centers_grid,
    get_urban_center_ids
)

from config import (
    HOST,
    PORT,
    DATABASE,
    USER,
    PASSWORD,
    COVARIATE_COLUMNS,
    REFERENCE_COLUMN,
)


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def run_prediction(training_data):
    logging.info("start workflow")

    df = load_urban_centers_grid()
    logging.info("got dataframe")

    if training_data == "reference_and_osm":
        urban_center_ids = get_urban_center_ids(threshold=0.005)
        df.loc[
            (df["urban_center_id"].isin(urban_center_ids)),
            f"reference_building_area_sqkm"
        ] = df[f"osm_building_area_sqkm_2023"]

        df[f"reference_completeness_area_sqkm"] = round(df[f"osm_building_area_sqkm_2023"] / df[f"reference_building_area_sqkm"], 3)

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
    logging.info(f"fitted model")

    y_pred = regressor.predict(X_input)
    logging.info(f"predicted model")

    # get importance
    importance = regressor.feature_importances_
    # summarize feature importance
    feature_importance = {}
    for i, v in enumerate(importance):
        feature_importance[COVARIATE_COLUMNS[i]] = v
    logging.info(feature_importance)

    df[f"prediction"] = y_pred
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    export_columns = [
        "grid_fid",
        "urban_center_id",
        "prediction",
        "geom"
    ]
    df[export_columns].to_postgis(
        f"prediction_{training_data}_grid_raw",
        con=con,
        if_exists="replace",
    )
    logging.info("saved predictions to postgres table.")


if __name__ == "__main__":
    """python scripts/run_prediction.py reference_and_osm"""

    training_data = sys.argv[1]

    if training_data in ["reference", "reference_and_osm"]:
        run_prediction(training_data)
    else:
        print("please pass a valid argument: 'reference' or 'reference_and_osm'")
