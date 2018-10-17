from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from datetime import date
import numpy as np
import pandas as pd

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return (
        f"<strong>Welcome to the Hawaiian Climate API!<br/><br/></strong>"
        f"<strong>Here are the Routes:<br/><br/></strong>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Tobs: /api/v1.0/tobs<br/><br/>"
        f"Start: /api/v1.0/<start><br/>"
        f"Start End: /api/v1.0/<start>/<end><br/><br/>" 
        )

@app.route("/api/v1.0/precipitation")
def precipitation():

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation= session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        order_by(Measurement.date).all()

    prcp_totals = []
    for result in precipitation:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        prcp_totals.append(row)

    return jsonify(prcp_totals)


@app.route("/api/v1.0/stations")
def stations():
    stations= session.query(Station.name, Station.station).all()

    stations_totals =[]
    for result in stations:
        row = {}
        row["name"] = result[0]
        row["station"] = result[1]
        stations_totals.append(row)

    return jsonify(stations_totals)


@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.station, Measurement.tobs).\
                filter(Measurement.date >= last_year).\
                filter(Measurement.date <= "2017-08-23").all()

    tobs_totals = []
    for result in tobs:
        row = {}
        row["date"] = result[0]
        row["tobs"] = result[1]
        tobs_totals.append(row)

    return jsonify(tobs_totals)


@app.route("/api/v1.0/<start>")

def startdate(start):
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    start_date = []
    for result in results:
        row={}
        row["Start Date"] = start
        row["Min Temp"] = float(result[0])
        row["Avg Temp"] = float(result[1])
        row["Max Temp"] = float(result[2])
        start_date.append(row)

    return jsonify(start_date)



@app.route("/api/v1.0/<start>/<end>")

def startend(start, end):
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    start_end = []
    for result in results:
        row={}
        row["Start Date"] = start
        row["End Date"] = end
        row["Min Temp"] = float(result[0])
        row["Avg Temp"] = float(result[1])
        row["Max Temp"] = float(result[2])
        start_end.append(row)

    return jsonify(start_end)
    

    return jsonify()

if __name__ == '__main__':
    app.run(debug=True)
