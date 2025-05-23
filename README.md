This project is composed of two parts: dataset creation and ML pipeline.
For the creation of the data set, I created intermitten csv files after adding each individual variable with a python script. 
I have not included the intermittent csv files, so some of the dataset scripts won't run without them. 
As such, to use this code to create a dataset, you will need to run them all from start to finish to create each intermittent csv file. 
Fortunately this is not necessary as I have provided the final dataset to test the ML pipeline on.

Here is a breakdown of each file in /src/:

<u>Dataset Creation</u>

/data/: the data file holds all of the raw data from various sources. mapalldata.csv holds the fire data, and population, temp, wind direction, and windspeed are self explanatory. The folders /data/pdsi/, /data/zindex/, and /data/precipitation/ have files for each county for that variable. 

/boundries/: holds all of the files for the CA County boundries shapefile which is used to assign grid cells to a county

windSpeedData.py, windDirectionData.py, and tempData.py: in these scrpits, I upload data from the meteostat api and create the csv files found in /data/

createDataSet.py: this creates the first csv with each grid cell, county, week, and weather station outputting fireData.csv

uploadStationData.py: adds the temperature, wind direction, and wind speed to fireData.csv

uploadCountyData.py: adds the pdsi, zindex, and precipitation to the fireData.csv and saves that into a new file called fireData_with_climate.csv

uploadPop.py: adds the population data to fireData_with_climate.csv and saves that into a new file called fireData_with_climate_and_population.csv

uploadFireData.py: adds the fire history and target variable to fireData_with_climate_and_population.csv and saves that into fireDataPreProcessing.csv

missingData.py: this takes fireDataPreProcessing.csv, drops wind direction because there were too many missing values, and fills in any missing data, saving the data into cleaned_fire_data.csv

addMonth.py: I forgot to add this variable, so this file takes cleaned_fire_data.csv and adds the month variable, saving this into dataPreScaling.csv

<u>Pre Processing</u>

preProcessing.py: splits (random 80/20) and scales the data and then does feature importance

preProcessing2.py: splits (random 80/20) and scales and does the correlation matrix

scaleAndSplit.py: scales and (random 80/20) splits the data creating train_data.csv and test_data.csv

scaleAndSplitKfold.py: scales and splits using StratifiedKfold to split the data saving it into train_data_KFold.csv and test_data_KFold.csv

scaleAndSplitNoFire.py: scales and splits (random 80/20) and drops the fire history column saving it into train_data_noFire.csv and test_data_noFire.csv

<u>ML Models</u>

models.py: runs the initial models (used for each of the training/testing splits)

models2.py: runs the ensemble methods

models3.py: looks deeper into the confidence aware model inlcuding looking at false positive and negatives for more insight

models4.py: time series cross validation

