import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

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
        f"Check out info about Hawaii's Weather<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).all()
    precipitation = {date: prcp for date, prcp in scores}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_list = session.query(Station.station).all()
    stations = list(np.ravel(station_list))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_obs():
    session = Session(engine)
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    temps = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year).all()
    temp_list = list(np.ravel(temps))
    return jsonify(temp_list)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def date_temps(start=None, end=None):
    session = Session(engine)
    stats = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        start_date = session.query(*stats).filter(Measurement.date >= start).all()
        info = list(np.ravel(start_date))
        return jsonify(info)

    end_date = session.query(*stats).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    info2 = list(np.ravel(end_date))
    return jsonify (info2)

if __name__== '__main__':
    app.run()