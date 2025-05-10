This project is composed of two parts: dataset creation and ML pipeline.
For the creation of the data set, I created intermitten csv files after adding each individual variable with a python script. 
I have not included the intermittent csv files, so some of the dataset scripts won't run without them. 
As such, to use this code to create a dataset, you will need to run them all from start to finish to create each intermittent csv file. 
Fortunately this is not necessary as I have provided the final dataset to test the ML pipeline on.

Here is a breakdown of each file in /src/:

Dataset Creation

/data/: the data file holds all of the raw data from various sources. mapalldata.csv holds the fire data, and population, temp, wind direction, and windspeed are self explanatory. The folders /data/pdsi/, /data/zindex/, and /data/precipitation/ have files for each county for that variable. 

/boundries/: holds all of the files for the CA County boundries shapefile which is used to assign grid cells to a county

windSpeedData.py, windDirectionData.py, and tempData.py: in these scrpits, I upload data from the meteostat api and create the csv files found in /data/

createDataSet.py: this creates the first csv with each grid cell, county, week, and weather station
