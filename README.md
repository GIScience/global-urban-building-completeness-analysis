# Investigating the digital divide in OpenStreetMap: spatio-temporal analysis of inequalities in global urban building completeness

Here is the python code for reproducing the analysis and figures presented in the global urban building completeness analysis manuscript. Several jupyter notebooks and python scripts are provided.

## Data
Make sure to download geopackage data from HeiBox: https://heibox.uni-heidelberg.de/f/b2f22e7f341f48a89100/

## Workflow
### Data Preparation
Insert the base data into the postgres tables for urban centers and grids. Insert data for corporate and humanitarian map edits.

```
psql -p 5429 -U osm-paper -h localhost -d osm-paper -f data/all_parameters_urban_centers_grid.sql
psql -p 5429 -U osm-paper -h localhost -d osm-paper -f data/all_parameters_urban_centers.sql
psql -p 5429 -U osm-paper -h localhost -d osm-paper -f data/reference_data_urban_centers_grid_raw.sql
psql -p 5429 -U osm-paper -h localhost -d osm-paper -f scripts/update_table_structure.sql
```

Optional: Update OSM building stats per urban center and grid cell. (This might take some time depending on how many urban centers will be analysed.)

```
python scripts/update_osm_buildings_stats.py
psql -p 5429 -U osm-paper -h localhost -d osm-paper -f scripts/update_osm_building_stats.sql
```

```
python scripts/update_osm_buildings_stats_2023.py
psql -p 5429 -U osm-paper -h localhost -d osm-paper -f scripts/update_osm_building_stats_2023.sql
```

Optional: Update Microsoft building stats per grid cell.

### Prediction
Run ML model to predict building area per 1km x 1km grid cell. Then calculate completeness per grid cell and aggregate prediction results for each urban center and derive completeness for each year.

```
python scripts/run_prediction.py reference
psql -p 5429 -U osm-paper -h localhost -d osm-paper -f scripts/aggregate_completeness_reference.sql
```

```
python scripts/run_prediction.py reference_and_osm
psql -p 5429 -U osm-paper -h localhost -d osm-paper -f scripts/aggregate_completeness_reference_and_osm.sql
```

### Performance
* run ML model several times using spatial cross validation approach

### Export data
Export data into GeoPackage file for easier handling in QGIS.

```
ogr2ogr -f "GPKG" data/global_urban_building_completeness.gpkg PG:"host=localhost port=5429 dbname=osm-paper user=osm-paper password=osm-paper" -update -overwrite -nlt POLYGON -nln all_parameters_urban_centers -sql "SELECT * FROM all_parameters_urban_centers"
ogr2ogr -f "GPKG" data/global_urban_building_completeness.gpkg PG:"host=localhost port=5429 dbname=osm-paper user=osm-paper password=osm-paper" -update -overwrite -nlt POLYGON -nln all_parameters_urban_centers_grid -sql "SELECT * FROM all_parameters_urban_centers_grid"
ogr2ogr -f "GPKG" data/global_urban_building_completeness.gpkg PG:"host=localhost port=5429 dbname=osm-paper user=osm-paper password=osm-paper" -update -overwrite -nlt POLYGON -nln rf_adjusted_prediction_reference_and_osm -sql "SELECT * FROM rf_adjusted_prediction_reference_and_osm"
ogr2ogr -f "GPKG" data/global_urban_building_completeness.gpkg PG:"host=localhost port=5429 dbname=osm-paper user=osm-paper password=osm-paper" -update -overwrite -nlt POLYGON -nln rf_adjusted_prediction_reference_and_osm_urban_centers -sql "SELECT * FROM rf_adjusted_prediction_reference_and_osm_urban_centers"
```

### Create Figures, Maps and Tables
#### Figures and Analyses
The processing steps for the analyses can be found in the `notebooks` section. The figures are stored in the `figures` directory.

#### Maps
The maps are created in [QGIS](https://www.qgis.org/en/site/). All relevant data files, qgis project files and styles are stored in the geopackage `data/global_urban_building_completeness.gpkg`.



