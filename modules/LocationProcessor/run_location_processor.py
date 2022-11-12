import logging
import os


import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.functions import ST_AsText, ST_Point
from kafka import KafkaConsumer

from multiprocessing import Process

from dataclasses import dataclass
from datetime import datetime

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry.point import Point
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.hybrid import hybrid_property



DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("LocationProcessor-api")



db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)

class Location(db.Model):
    __tablename__ = "location"

    id = Column(BigInteger, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    coordinate = Column(Geometry("POINT"), nullable=False)
    creation_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    _wkt_shape: str = None

    @property
    def wkt_shape(self) -> str:
        # Persist binary form into readable text
        if not self._wkt_shape:
            point: Point = to_shape(self.coordinate)
            # normalize WKT returned by to_wkt() from shapely and ST_AsText() from DB
            self._wkt_shape = point.to_wkt().replace("POINT ", "ST_POINT")
        return self._wkt_shape

    @wkt_shape.setter
    def wkt_shape(self, v: str) -> None:
        self._wkt_shape = v

    def set_wkt_with_coords(self, lat: str, long: str) -> str:
        self._wkt_shape = f"ST_POINT({lat} {long})"
        return self._wkt_shape

    @hybrid_property
    def longitude(self) -> str:
        coord_text = self.wkt_shape
        return coord_text[coord_text.find(" ") + 1 : coord_text.find(")")]

    @hybrid_property
    def latitude(self) -> str:
        coord_text = self.wkt_shape
        return coord_text[coord_text.find("(") + 1 : coord_text.find(" ")]

def insertLocation(location):

    new_location = Location()
    new_location.person_id = location["person_id"]
    new_location.creation_time = location["creation_time"]
    new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
    db.session.add(new_location)
    db.session.commit()
    print("new location has been inserted")


consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER, group_id='my_group')

def consumer_main():
    # check if the consumer would be listing the topics
    topics = consumer.topics()

    if not topics:
        raise RuntimeError()

    for location in consumer:
        location_message = location.value.decode('utf-8')
        print('{}'.format(location_message))
        location_message = json.loads(location_message)
        insertLocation(location_message)
        
def run_app():
    app.run(debug=False, port=5001)

consumer_process = Process(name="consumer_process", target=consumer_main)
run_app_process = Process(target=run_app)

@app.route("/health")
def health():
    return jsonify("healthy LocationProcessor")

@app.route("/start")
def start():
    if not consumer_process.is_alive():
        consumer_process.start()
        consumer_process.join()

    return jsonify(f"Run {consumer_process.name} on {consumer_process.pid}")

# STOP the consumer remotly - UNF
#@app.route("/stop")
#def stop():
#    if t_consumer.is_alive():
#        consumer.close()
#        t_consumer.stop()
#    return jsonify("stop consumer")


if __name__ == '__main__':
    run_app_process.start()
    run_app_process.join()


    
    

