# add dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################################
# 
#################################################################

# set up, connect and reflect database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################################
# start Flask app
#################################################################
app = Flask(__name__)


@app.route("/")
def welcome():
    """ List all available api routes. """
    return(
        f"Available Routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/startdate</br>"
        f"/api/v1.0/startdate/enddate</br>"
    )

@app.route("/api/v1.0/precipitation")
def get_last_year_precip():
    """ Return final year of precipitaion from dataset. """
    
    # open session for query
    session = Session(engine)
    # Perform a query to retrieve the data and precipitation scores
    last_12_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date < '2017-08-23')
    # close session to save resources
    session.close()
    # convert results to dictionary
    prev_year_precip = {}
    for date, prcp in last_12_precip:
        prev_year_precip[date] = prcp
        #prev_year_precip["Precipitation"] = prcp

    return(jsonify(prev_year_precip))

@app.route("/api/v1.0/stations")
def get_weather_stations():
    """ Return list of weather stations """
    # open session for query
    session = Session(engine)
    # Perform a query to retrieve the data and precipitation scores
    station_result = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)
    # close session to save resources
    session.close()

    station_list = []
    for station, name, latitude, longitude, elevation in station_result:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_list.append(station_dict)

    return jsonify(station_list)


if __name__ == '__main__':
    app.run(debug=True)
