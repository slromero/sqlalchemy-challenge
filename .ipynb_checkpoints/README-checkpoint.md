# sqlalchemy-challenge
Assignment 10

Resources:
https://stackoverflow.com/questions/76282688/how-to-reduce-the-number-of-tick-labels-on-a-bar-plot
https://www.geeksforgeeks.org/adding-items-to-a-dictionary-in-a-loop-in-python/

Part 1: Analyze and Explore the Climate Data
Use Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. Use SQLAlchemy ORM queries, Pandas, and Matplotlib.

Used the provided files (climate_starter.ipynb and hawaii.sqlite) to complete the climate analysis and data exploration.

Used the SQLAlchemy create_engine() function to connect to the SQLite database.

Used the SQLAlchemy automap_base() function to reflect the tables into classes, and then saved references to the classes named station and measurement.

Linked Python to the database by creating a SQLAlchemy session.

IMPORTANT
Remembered to close the session at the end of the notebook.

Performed a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

Precipitation Analysis
Found the most recent date in the dataset.

Using that date, got the previous 12 months of precipitation data by querying the previous 12 months of data.

HINT
Selected only the "date" and "prcp" values.

Loaded the query results into a Pandas DataFrame. Explicitly set the column names.

Sorted the DataFrame values by "date".

Plotted the results by using the DataFrame plot method, as the following image shows:

A screenshot depicts the plot.

Used Pandas to print the summary statistics for the precipitation data.

Station Analysis
Designed a query to calculate the total number of stations in the dataset.

Designed a query to find the most-active stations (that is, the stations that have the most rows). To do so, completed the following steps:

Listed the stations and observation counts in descending order.

HINT
Answered the following question: which station id has the greatest number of observations?
Designed a query that calculated the lowest, highest, and average temperatures filtered on the most-active station id found in the previous query.

HINT
Designed a query to get the previous 12 months of temperature observation (TOBS) data. To do so, completed the following steps:

Filtered by the station that has the greatest number of observations.

Queried the previous 12 months of TOBS data for that station.

Plotted the results as a histogram with bins=12, as the following image shows:

A screenshot depicts the histogram.

Closed the session.

Part 2: Design Your Climate App
Designed a Flask API based on the queries just developed. To do so, used Flask to create routes as follows:

/

Started at the homepage.

Listed all the available routes.

/api/v1.0/precipitation

Converted the query results from the precipitation analysis (i.e. retrieved only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

Returned the JSON representation of your dictionary.

/api/v1.0/stations

Returned a JSON list of stations from the dataset.
/api/v1.0/tobs

Queried the dates and temperature observations of the most-active station for the previous year of data.

Returned a JSON list of temperature observations for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>

Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

For a specified start, calculated TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

For a specified start date and end date, calculated TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.