import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Climate App<br/>" 
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query all precipitation
    date_prcp = session.query(Measurement.date, Measurement.prcp).all()

    precipitation = []
    for result in date_prcp:
        precipitation_dict = {}
        precipitation_dict["Date"] = result[0]
        precipitation_dict["Precipitation"] = result[1]
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    station_info = session.query(Station.longitude, Station.name, Station.id, Station.elevation,
    Station.latitude, Station.station).all()

    stations = []
    for result in station_info:
        station_dict = {}
        station_dict["longitude"] = result[0]
        station_dict["name"] = result[1]
        station_dict["id"] = result[2]
        station_dict["elevation"] = result[3]
        station_dict["latitude"] = result[4]
        station_dict["station"] = result[5]
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query all tobs from last 12 months 
    last_twelve = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date>"2016-08-23").all()

    tobs = []
    for result in last_twelve:
        tob_dict = {}
        tob_dict["station"] = result[0]
        tob_dict["tobs"] = result[1]
        tobs.append(tob_dict)

    return jsonify(tobs)

@app.route("/api/v1.0/start/<start>")
def start_date(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    temp_info = []
    for result in results:
        temp_info_dict = {}
        temp_info_dict["Min"] = result[0]
        temp_info_dict["Avg"] = result[1]
        temp_info_dict["Max"] = result[2]
        temp_info.append(temp_info_dict)

    return jsonify(temp_info)

@app.route("/api/v1.0/<start>/<end>")
def start_date_end_date(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temp_info = []
    for result in results:
        temp_info_dict = {}
        temp_info_dict["Min"] = result[0]
        temp_info_dict["Avg"] = result[1]
        temp_info_dict["Max"] = result[2]
        temp_info.append(temp_info_dict)

    return jsonify(temp_info)


if __name__ == '__main__':
    app.run(debug=True)