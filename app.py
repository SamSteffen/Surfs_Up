#import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#access the sqlite database
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database in our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#create a variable for each of the classes so we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from Python to our database
session = Session(engine)

#define the Flask application
app = Flask(__name__)

#define the welcome route
@app.route("/")

#create a function to add routing info for other routes
def welcome():
    return('''
    Welcome to the Climate Analysis API! 
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations  
    /api/v1.0/tob 
    /api/v1.0/temp/start/end
    ''')

#create the second route (precipitation)
@app.route("/api/v1.0/precipitation")

# create the precipitation function
# make sure the function collects precipitation data from the last year
# add the collected data to a dictionary
# use jsonify to convert the dictionary data to a json file
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#create the third route (stations)
@app.route("/api/v1.0/stations")

#create the stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create the fourth route
@app.route("/api/v1.0/tobs")

#create a temp_monthly() function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#create the fifth route, with starting and ending routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#create a function to retrieve the data
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)