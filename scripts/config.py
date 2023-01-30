import os


HOST = os.getenv("POSTGRES_HOST", default="localhost")
PORT = os.getenv("POSTGRES_PORT", default=5429)
DATABASE = os.getenv("POSTGRES_DB", default="osm-paper")
USER = os.getenv("POSTGRES_USER", default="osm-paper")
PASSWORD = os.getenv("POSTGRES_PASSWORD", default="osm-paper")

COVARIATE_COLUMNS = [
    "worldcover_2020_built_up_sqkm",
    "worldcover_2020_tree_cover_sqkm",
    "worldcover_2020_sparse_vegetation_sqkm",
    "ghspop_2020",
    "vnl_2020",
    "shdi_2019",
    "osm_road_length_km_2023",
    "region_code",
]

REFERENCE_COLUMN = f"reference_building_area_sqkm"
