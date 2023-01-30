import logging
import pandas as pd
from sqlalchemy import create_engine

from sklearn.cluster import AgglomerativeClustering

from config import (
    HOST,
    PORT,
    DATABASE,
    USER,
    PASSWORD,
)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def load_dataframe():
    con = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    query = f"""
        select 
            urban_center_id
            ,osm_completeness
            ,gini
            ,moran
        from inequality_measures_urban_centers
        order by urban_center_id
    """
    df = pd.read_sql_query(query, con=con)
    df.dropna(inplace=True)
    return df


def get_cluster(x):
    cluster = ["e", "b", "d", "a", "c"]
    return cluster[x]


if __name__ == "__main__":
    n_clusters = 5
    columns = [
        "osm_completeness",
        "gini",
        "moran"
    ]

    df = load_dataframe()
    X = df[columns].values

    cluster = AgglomerativeClustering(n_clusters=n_clusters).fit(X)
    df["label"] = cluster.labels_
    df["cluster"] = df['label'].apply(get_cluster)

    print(df["cluster"].value_counts())
    print(df)

    cluster_labels = [
        3, 1, 4, 2, 0
    ]

    engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    df.to_sql(
        'inequality_measures_with_clusters_urban_centers',
        engine,
        if_exists='replace',
        index=False
    )
