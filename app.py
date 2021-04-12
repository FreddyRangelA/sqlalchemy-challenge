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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

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


@app.route("/api/v1.0/tobs")
def tobs():
#uery the dates and temperature observations of the most active station for the last year of data.
    mostAcvtive_tobs_data = session.query(Measurement.date, Measurement.tobs,Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).filter(Measurement.date > oneYearFromDate).first()
    x=mostAcvtive_tobs_data[2]
    avtive=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==x).filter(Measurement.date > oneYearFromDate).all()
    #Return a JSON list of temperature observations (TOBS) for the previous year.
    tobs=list(np.ravel(avtive))
    return jsonify(tobs)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
def start(start):

#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    start_temp=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start_date).all()
    temp_start_list=list(np.ravel(start_temp))
    return jsonify(temp_start_list)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>/<end>")
def start2(start,end):


    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date=dt.datetime.strptime(end, '%Y-%m-%d')
    start_end_temp=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()
    temp_start_end_list=list(np.ravel(start_end_temp))
    return jsonify(temp_start_end_list)



session.close()
#
if __name__ == "__main__":
    app.run(debug=True)
    