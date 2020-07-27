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

# Create our session (link) from Python to the DB
session = Session(engine)


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

# @app.route("/api/v1.0/precipitation")



# Perform a query to retrieve the data and precipitation scores
last_12_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date < '2017-08-23')

prev_year_precip = {}


if __name__ == '__main__':
    app.run(debug=True)
