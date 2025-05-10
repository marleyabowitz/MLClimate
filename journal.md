Diary of Progress

Week of February 17th: 
- Decide on the project theme
- Wrote Proposal (abstract file)
- Created and organized Git Hub Repo
- Planned work for rest of semester

Week of February 24th:
- Outline project goals
- Research similar projects to choose variables
  Goals of research are noting all variables different fire predictors use. Do they combine datasets or use them individually? How do they process data? What worked and what didn't?
  Findings: (each bullet point represents an article that is linked in the google doc and will be in the final report)
- CA Central Valley: Variables: fire history, longitude/latitude, air temp, mass fraction of cloud liquid water, east wind, north wind, relative humidity, specific humidity, ozone ration, cumulative mass flux, convective rainwater, 3D flux of ice convective precipitation, 3D flux of ice nonconvective precipitation, 3D flux of liquid convective precipitation, 3D flux of liquid nonconvective precipitation, evap. subl. convective precipitation, evap. subl. Nonconvective precipitation, normalized difference vegetation index
- Logistic Regression and Neural Networks: Variables: topography, burned areas, distance to roads, distance to urban areas, distance to agriculture, distance to shrublands, distance to forest
- Forest Fire Prediction: Variables: Humidity, wind speed, temperature, location
- CA wildfire predicting: Variables: Past fire data, meteorological data, vegetation and environmental features
- China forest fire: Variables: longitude/latitude, topography, surface temp, wind speed, hours of sunshine, infrastructure, socioeconomic
- Mediterranean Spatial Patterns: Variables: average temperature, minimum temperature, average elevation, …
- San Diego: Variables: weather data, remote sensing data, fire history data, vegetation data
- Game theory: Variables: local meteorological variables, land surface variables, coordinates, socioeconomic variables, large-scale meteorological patterns 
- Nor. Cal.: Variables: fire history, weather, vegetation, power line, terrain

The variables I have chosen given this research are the following:
Chosen Variables:
- Temperature
- Humidity
- Percipitation
- Wind (speed and strength)
- Fire history
- Vegitation
- County/longitutde/latitude
- Season
- Large scale weather patterns
- Socioeconomic variables
- Population density
- Emergency response time
- Drought index
- Land cover type
- Air quality index
- Lightning strike frequency
- Vegetation health index
- Climate anomaly indicators

Week of March 3rd:
- Finalized what features we will use.
- Approaching the issue of spatial and temporal discrepancies in the data: because a lot of the data is defined geographically, I am choosing to approach the dataset by doing a latitude longitude grid.
  I will divide California into a grid of equally spaced latitude/longitude cells (e.g., 0.1° x 0.1° or 0.01° x 0.01° resolution). Geospatial data (weather patterns, vegetation) are usually in lat/lon format, making it easy to integrate. Some socioeconomic or county-level data may require aggregation or disaggregation, so I will need to figure this out. First I will assign each data point (e.g., weather station data, fire history) to the nearest lat/lon grid cell. For region-based data (e.g., county data), repeat the value across all cells within the region.
- I narrowed down features to precipitation, z index, PDSI, population density, wind speed, wind direction, temperature, and fire history.
- Unprocessed datasets are in the data file. 

Week of March 10th:
- First I need to choose my grid resolution: Based on other projects,
  - 1 km × 1 km (~0.01° lat/lon): High-resolution but large dataset
  - 10 km × 10 km (~0.1° lat/lon): Moderate balance between precision and performance
  - 50 km × 50 km (~0.5° lat/lon): Coarse but computationally efficient
  - I will start with 0.1° (~10 km grid)
- Next I create the grid in a shapefile format using python (data_grid.py)
- I then assign data do the grid and merge all datasets.
  - Index: Latitude, Longitude, Week (from 2014-01-01 to 2024-12-31)
  - Variables per grid cell-week:
    - precipitation (monthly → assigned to each week in that month)
    - z_index (monthly → weekly via forward fill within the month)
    - pdsi (monthly → weekly)
    - population (yearly → repeated for all weeks in that year)
    - wind_speed (weekly, by station → interpolated to grid)
    - wind_direction (weekly, same as above)
    - temperature (weekly, same as above)
    - fire_past_6mo (binary: was there a fire in this grid in past 26 weeks)
    - fire_this_week (binary: was there a fire in this grid this week)
- Each grid is assigned a county for the county-based datasets using this dataset: https://lab.data.ca.gov/dataset/california-county-boundaries-and-identifiers
- Missing values are imputed with nearby data.

Week of March 24th:
- Normalizing and scaling features.
- Scale numerical features (temperature, humidity, wind speed) using MinMaxScaler() or StandardScaler() from sklearn.preprocessing.
- Handle missing data (e.g., use mean imputation or fill with 0 for sparse datasets).
  
Week of March 31st:
- I am unable to work this week because I have two midterms on Monday. These are my last ones, so I can work on this project a lot in the next two weeks!

Week of April 7th:
- Feature importance
- Feature correlation
- Running initial models (Random Forest, XGBoost, Logistic Regression, LightGBM, and a Multi- Layer Perceptron)

Week of April 14th:
- Exploring ensemble methods
- Started writing final paper

Week of April 21st:
- Made presentation
- Continued final paper

Week of April 28th: Presentation!

Week of May 5th:
- Implementing suggestions from my presentation:
  - Firstly, I removed the fire history from the data and re-ran all of my models. This was pretty straightforward.
  - Next, I created new training and testing data files using a Stratified K-Fold split.
  - I used the Sklearn StratifiedKFold function and my code looks like this:
    - skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    - train_idx, test_idx = next(skf.split(X_scaled_df, y))
  - After this, I did time series cross-validation by first splitting with TimeSeriesSplit from sklearn, and then creating 5 sequential train/test splits that preserve temporal order, and then finally training the models by fold.
  - The last thing I did was permutation feature importance. For this, I just used sklearn's feature_importance function and implemented it in this line of code:
    - result_xgb = permutation_importance( xgb_model, X_test, y_test, n_repeats=10, random_state=42, scoring='accuracy' )
  - Updated journal and code to turn everything in!
