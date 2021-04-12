import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from flask import Flask, jsonify
import datetime as dt
import pandas as pd
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session=Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

oneYearFromDate= '2016-08-23'

#################################################
# Flask Routes
#################################################
@app.route("/")
def Welcome():
    return(
        f"Availabel routs: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"

    )

#Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > oneYearFromDate).order_by(Measurement.date).all()

    precipitation_dic=[]  
    for date, precipitation in prcp_data:
        prcp_dic={}
        prcp_dic["date"]=date
        prcp_dic["precipitation"]= precipitation
        precipitation_dic.append(prcp_dic)
    return jsonify(precipitation_dic)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.station).all()
    stations =list(np.ravel(stations_query))
    return jsonify(stations)


if __name__ == "__main__":
    app.run(debug=True)
    