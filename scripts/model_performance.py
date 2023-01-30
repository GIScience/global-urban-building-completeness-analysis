import logging
import pandas as pd
from random import sample

from sqlalchemy import create_engine

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans

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


def get_urban_center_centroids():
    con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    sql = f"""
        select 
            urban_center_id 
            ,ST_X(centroid) as x
            ,ST_Y(centroid) as y
        from full_urban_centers
        where
            reference_building_area_sqkm is not null
            AND
            -- avoid urban centers for which training data might not be complete
            reference_osm_completeness < 1.5
    """
    df = pd.read_sql(sql, con=con)
    logging.info(f"got {len(df)} urban centers with centroid coordinates")

    return df


def spatial_train_test_split_cluster(df, cluster_label, n=0):
    """Split based on sample location."""

    train_indices = df.index[
        (df["cluster"] != cluster_label)
        &
        (df["reference_building_area_sqkm"] > 0)  # this includes OSM data
    ].tolist()

    test_indices = df.index[
        (df["cluster"] == cluster_label)
        &
        (df["reference_building_area_sqkm"] > 0)  # this includes only reference data and osm data
    ].tolist()

    if n > 0:
        if n > len(train_indices):
            n = len(train_indices)
        train_indices = sample(train_indices, n)

    return train_indices, test_indices


def kmeans_cluster_urban_centers(df, x, y, n_clusters=10):
    columns = [x, y]
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[columns])
    df["cluster"] = kmeans.labels_
    return df, n_clusters


def estimate_model_performance(n_clusters=10):
    df = load_urban_centers_grid()

    urban_centers_df = get_urban_center_centroids()
    cluster_df, n_clusters = kmeans_cluster_urban_centers(urban_centers_df, "x", "y", n_clusters)
    df = df.join(cluster_df.set_index('urban_center_id'), on="urban_center_id", how="inner")
    region_groups = list(range(0, n_clusters))

    df[f"reference_building_area_sqkm_initial"] = df[f"reference_building_area_sqkm"]

    urban_center_ids = get_urban_center_ids(threshold=0.005)
    df.loc[
        (df["urban_center_id"].isin(urban_center_ids))
        &
        (df["reference_building_area_sqkm"] < df[f"osm_building_area_sqkm_2023"]),
        f"reference_building_area_sqkm"
    ] = df[f"osm_building_area_sqkm_2023"]
    df[f"reference_completeness_area_sqkm"] = round(df[f"osm_building_area_sqkm_2023"] / df[f"reference_building_area_sqkm"], 3)

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
            train_indices, test_indices = spatial_train_test_split_cluster(df_model, regions, n=50000)

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
            logging.info(f"fitted model")

            y_pred = regressor.predict(X_test)
            logging.info(f"predicted model")

            df_test = df_model.iloc[test_indices]

            df_test["repeat"] = r
            df_test[f"prediction"] = y_pred
            df_test[f"reference_building_area_sqkm"] = y_test
            df_test["split"] = i

            con = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
            export_columns = [
                "grid_fid",
                "urban_center_id",
                "iso_a3",
                "region_wb",
                "repeat",
                "split",
                "prediction",
                f"reference_building_area_sqkm",
            ]
            df_test[export_columns].to_sql(
                f"performance_{n_clusters}_clusters_reference_and_osm",
                con=con,
                if_exists="append",
            )
            logging.info("saved predictions to postgres table.")


if __name__ == "__main__":
    """python scripts/model_performance.py"""
    estimate_model_performance(n_clusters=20)
