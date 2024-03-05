# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    
    """List all available api routes."""
    return (
        f"<h2>Precipitation and Temperature Readings</h2>"
        f"<h3>Dates 2010-01-01 to 2017-08-23</h3><br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"-------------<br/>"
        f"For a specific start date, as in '/api/v1.0/2014-01-01':<br/>"
        f"/api/v1.0/&lt;yyyy-mm-dd&gt;<br/><br/>"
        f"-------------<br/>"
        f"For a specific date range, as in '/api/v1.0/2014-01-01/2014-01-31':<br/>"
        f"/api/v1.0/&lt;yyyy-mm-dd&gt;/&lt;yyyy-mm-dd&gt;<br/><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip_dict_json():

    """Convert precipitation analysis to dictionary (12 months of data)"""
    
    #Find the most recent date in the data set.
    most_recent_date = session.query(Measurement.date).order_by(desc(Measurement.date)).first()
    
    #Calculate the date one year from the last date in data set.
    last_year_start = dt.datetime.strptime(most_recent_date[0],'%Y-%m-%d').date() - dt.timedelta(days=365)

    #Perform a query to retrieve the data and precipitation scores for 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
       filter(Measurement.date >= last_year_start)

    # Create a dictionary from the row data and append to a list of precipitation results
    # readings = {}
    readings = {}
    for date, prcp in results:
            readings.update({date:prcp})
    return jsonify(readings)


@app.route("/api/v1.0/stations")
def precip_stations_json():

    """station list"""
    
    station_list = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    all_stations = []
    for id, station, name, latitude, longitude, elevation in station_list:
        station_dict = {}
        station_dict['id'] = id
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def station_tobs_json():

    #Find the most recent date in the data set.
    most_recent_date = session.query(Measurement.date).order_by(desc(Measurement.date)).first()
    
    #Calculate the date one year from the last date in data set.
    last_year_start = dt.datetime.strptime(most_recent_date[0],'%Y-%m-%d').date() - dt.timedelta(days=365)

    """Last 12 months of temperature observation data for the most active station USC00519281"""
    last_year_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_year_start, Measurement.station == 'USC00519281').order_by(Measurement.date).all()

    temps = []
    for date, tobs in last_year_temp:
            tobs_dict = {}
            tobs_dict['date'] = date
            tobs_dict['tobs'] = tobs
            temps.append(tobs_dict)
        
    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def station_summary_start(start):

    #Capture start date
    start_date_only = dt.datetime.strptime(start,'%Y-%m-%d').date()
    
    temp_data_from_start = session.query(Measurement.date, func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        group_by(Measurement.date).filter(Measurement.date >= start_date_only).all()

    from_start =[]
    for date, tmin, tavg, tmax in temp_data_from_start:
        t_dict = {}
        t_dict['date'] = date
        t_dict['tmin'] = tmin
        t_dict['tmax'] = tmax
        t_dict['tavg'] = tavg
        from_start.append(t_dict)

    return jsonify(from_start)


@app.route("/api/v1.0/<start>/<end>")
def station_summary_range(start, end):

    #Capture start and end date
    start_date = dt.datetime.strptime(start,'%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end,'%Y-%m-%d').date()
    
    temp_data_start_to_end = session.query(Measurement.date, func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        group_by(Measurement.date).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    start_to_end =[]
    for date, tmin, tavg, tmax in temp_data_start_to_end:
        trange_dict = {}
        trange_dict['date'] = date
        trange_dict['tmin'] = tmin
        trange_dict['tmax'] = tmax
        trange_dict['tavg'] = tavg
        start_to_end.append(trange_dict)

    return jsonify(start_to_end)
    


if __name__ == '__main__':
    app.run(debug=True)

session.close()