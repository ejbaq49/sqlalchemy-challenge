# add dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

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
        f"/api/v1.0/YYYY-MM-DD</br>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD</br>"
    )

@app.route("/api/v1.0/precipitation")
def get_last_year_precip():
    """ Return final year of precipitaion from dataset. """
    
    # open session for query
    session = Session(engine)
    # Perform a query to retrieve the data and precipitation scores
    last_12_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date < '2017-08-23').all()
    # close session to save resources
    session.close()
    return(jsonify(last_12_precip))

@app.route("/api/v1.0/stations")
def get_weather_stations():
    """ Return list of weather stations """
    # open session for query
    session = Session(engine)
    # Perform a query to retrieve stations that recorded measurements (use JOIN)
    station_result = session.query(Station.name).filter(Station.station==Measurement.station).group_by(Station.name).all()
    # close session to save resources
    session.close()
    return jsonify(station_result)

@app.route("/api/v1.0/<start_date>")
def get_temp_start(start_date):
    session = Session(engine)
    temp_from_start = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date).all()
    session.close
    return jsonify(temp_from_start)


@app.route("/api/v1.0/tobs")
def get_temp_obs():
    # Determine latest observation date for this station
    # most_active_latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).\
    #     filter(Measurement.station=="USC00519281").\
    #     first()
    end_date = '2017-08-18'
    start_date = dt.datetime(2017,8,18) - dt.timedelta(days=365)
    session = Session(engine)
    station_measures = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        filter(Measurement.station=='USC00519281').order_by(Measurement.date).all()
    session.close()
    return(jsonify(station_measures))

if __name__ == '__main__':
    app.run(debug=True)
