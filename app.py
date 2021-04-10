import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from flask import Flask, jsonify
import datetime as dt

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
    return jsonify(prcp_data)

if __name__ == "__main__":
    app.run(debug=True)
    