import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
    )

#precip_data = pd.read_sql("SELECT date,prcp FROM measurement WHERE date BETWEEN '2016-08-23' AND '2017-07-23' ORDER BY date DESC", conn)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    conn = engine.connect()
    # Query all precipitation
    precip_data = pd.read_sql("SELECT date, prcp FROM measurement WHERE date BETWEEN '2016-08-23' AND '2017-07-23' ORDER BY date DESC", conn)
    precip_data=precip_data.dropna()
    # Create a dictionary from the row data and append to a list of all_precip
    all_precip = []
    for index, row in precip_data.iterrows():
        precip_dict = {}
        precip_dict["Date"] = row['date']
        precip_dict["Precipitation"] = row['prcp']
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    conn = engine.connect()
    # Query all stations
    active_stations=pd.read_sql("SELECT station AS 'Station ID', COUNT(station) AS 'Total Appearance' FROM measurement GROUP BY station ORDER BY COUNT(station) DESC", conn)
    
    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for index, row in active_stations.iterrows():
        station_dict = {}
        station_dict["Station ID"] = row['Station ID']
        station_dict["Total Appearance"] = row['Total Appearance']
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    conn = engine.connect()

    # Query all stations
    temp_observed=pd.read_sql("SELECT station AS 'Station ID', tobs AS 'Temp Recorded', date FROM measurement WHERE station='USC00519281' AND date BETWEEN '2016-08-23' AND '2017-07-23' ORDER BY tobs DESC", conn)
    # Create a dictionary from the row data and append to a list of all_temp
    all_temp = []
    for index, row in temp_observed.iterrows():
        temp_dict = {}
        temp_dict["Station ID"] = row['Station ID']
        temp_dict["Temp Observed"] = row['Temp Recorded']
        temp_dict["Date"] = row['date']
        all_temp.append(temp_dict)

    return jsonify(all_temp)
if __name__ == "__main__":
    app.run(debug=True)