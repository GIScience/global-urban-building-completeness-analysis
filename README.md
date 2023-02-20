# Investigating completeness and inequalities in OpenStreetMap: spatio-temporal analysis of global urban building data

> OpenStreetMap (OSM) has evolved as a popular geospatial dataset for global studies, such as monitoring progress towards the Sustainable Development Goals.
However, many global applications turn a blind eye on its uneven spatial coverage.
We utilized a regression model to infer OSM building completeness within 13,189 urban agglomerations.
For 1,848 cities (16% of the global urban population) OSM building footprint data exceeds 80% completeness, but completeness remains lower than 20% for 9,163 cities (48% of the global urban population).
From 2008-2023 inequalities in OSM have receded, but a strong spatial bias associated with subnational human development index (SHDI), city size and World Bank region remains.
Humanitarian mapping efforts have significantly improved completeness, especially In low SHDI regions, 
Knowing the biases in OSM's coverage enables researchers and practitioners to provide clear recommendations for decision makers, as they now can properly account for the previously “invisible” missing data.

Here we provide the python code and data for reproducing the analysis and figures presented in the global urban OSM building completeness analysis manuscript. Several jupyter notebooks and additional scripts are provided to pre-process the data.


## Data
Make sure to download geopackage data from HeiBox: https://heibox.uni-heidelberg.de/f/b2f22e7f341f48a89100/

You can also interactively explore the results in [ohsomeHex](https://hex.ohsome.org/#/urban_building_completeness/2022-01-01T00:00:00Z/2/29.21752531472042/16.251362043911197).
[![name](figures/ohsome_hex_screenshot.png)](https://hex.ohsome.org/#/urban_building_completeness/2022-01-01T00:00:00Z/2/29.21752531472042/16.251362043911197)


## Create Figures, Maps and Tables
### Figures and Analyses
The processing steps for the analyses can be found in the `notebooks` section. The figures are stored in the `figures` directory.

### Maps
The maps are created in [QGIS](https://www.qgis.org/en/site/). All relevant data files, qgis project files and styles are stored in the geopackage `data/global_urban_building_completeness.gpkg`.
