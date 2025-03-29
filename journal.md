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
- CA Central Valley: The California wildfire season is between May and October for the Southern California region based on the historical trends of past wildfires. The Northern California wildfire season is from July to October (wfca_teila 2022). Wildfires continue throughout the years, focusing on 2013 to 2022, showing that the total acres burned each year exceed 114,000 (When Is California Fire Season?, 2023). The trend also indicates that July has the most fire incidents, while September and October include the most burned acres (California Department of Forestry and Fire Protection | CAL FIRE 2023). This is when factors such as heat, drought, wind, and human activity increase the risk of fires. Measures are being taken to prevent wildfires, such as vegetation management, wildfire prevention grants, increase in fire training, etc. (wfca_teila 2022; California Department of Forestry and Fire Protection | CAL FIRE 2023) and (When Is California Fire Season?, 2023). Variables: fire history, longitude/latitude, air temp, mass fraction of cloud liquid water, east wind, north wind, relative humidity, specific humidity, ozone ration, cumulative mass flux, convective rainwater, 3D flux of ice convective precipitation, 3D flux of ice nonconvective precipitation, 3D flux of liquid convective precipitation, 3D flux of liquid nonconvective precipitation, evap. subl. convective precipitation, evap. subl. Nonconvective precipitation, normalized difference vegetation index
- Logistic Regression and Neural Networks: Variables: topography, burned areas, distance to roads, distance to urban areas, distance to agriculture, distance to shrublands, distance to forest
Forest Fire Prediction: Variables: Humidity, wind speed, temperature, location
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
- Found datasets for said features: XXXXX



Week of March 10th:
- Creating file tree:
  I will base my file tree off of this one (given by chatGPT)
/
 ├── data/                         # Raw and processed data
 │      ├── raw/                   # Raw data (original dataset files)
 │      ├── processed/             # Preprocessed/cleaned data
 │      └── external/              # External datasets or auxiliary files
 │
 ├── notebooks/                    # Jupyter Notebooks for EDA & experiments
 │      ├── eda.ipynb              # Exploratory Data Analysis
 │      ├── feature_eng.ipynb      # Feature engineering/testing
 │      └── model_testing.ipynb    # Model testing and evaluation
 │
 ├── scripts/                      # Python scripts for various stages
 │      ├── data_grid.py           # For loading & saving datasets into the grid
 │      ├── preprocess.py          # Preprocessing steps (cleaning, encoding, scaling)
 │      ├── feature_engineering.py # Feature extraction & selection
 │      ├── model_train.py         # Model training script
 │      ├── model_eval.py          # Model evaluation script
 │      └── utils.py               # Helper functions (e.g., custom metrics)
 │
 ├── models/                       # Saved models & serialized files
 │      ├── model.pkl              # Trained model file
 │      ├── scaler.pkl             # Scaler object
 │      └── vectorizer.pkl         # Vectorizer (TF-IDF, CountVectorizer, etc.)
 │
 ├── config/                       # Configuration files
 │      └── config.yaml            # Hyperparameters, file paths, etc.
 │
 ├── tests/                        # Unit and integration tests
 │      ├── test_preprocess.py
 │      ├── test_model.py
 │      └── test_utils.py
 │
 ├── requirements.txt              # Python dependencies
 ├── main.py                       # Main entry point for running the pipeline
 ├── README.md                     # Project description and instructions
 └── .gitignore                    # Git ignore file

- Combine all datasets into one dataset
- First I need to choose my grid resolution: Based on other projects,
  - 1 km × 1 km (~0.01° lat/lon): High-resolution but large dataset.
  - 10 km × 10 km (~0.1° lat/lon): Moderate balance between precision and performance.
  - 50 km × 50 km (~0.5° lat/lon): Coarse but computationally efficient.
  - I will start with 0.1° (~10 km grid) for a good balance, and adjust based on performance.
- Next I create the grid using python (data_grid.py)
- I then assign data do the grid and merge all datasets.

Week of March 24th:
- Normalizing and scaling features.
  
Week of March 31:
- TODO: Run models


