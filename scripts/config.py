import os


HOST = os.getenv("POSTGRES_HOST", default="localhost")
PORT = os.getenv("POSTGRES_PORT", default=5429)
DATABASE = os.getenv("POSTGRES_DB", default="osm-paper")
USER = os.getenv("POSTGRES_USER", default="osm-paper")
PASSWORD = os.getenv("POSTGRES_PASSWORD", default="osm-paper")

COVARIATE_COLUMNS = [
    "built_up_sqkm",
    "built_up_sqkm_moran_loc",
    "tree_cover_sqkm",
    "sparse_vegetation_sqkm",
    "ghspop",
    "ghspop_moran_loc",
    "vnl",
    "shdi",
    "osm_other_major_roads_length_km",
    "region_code",
]

UNIT = "area_sqkm"
REFERENCE_COLUMN = f"reference_building_{UNIT}"
MODEL_NAME = "rf_adjusted"
