import logging
import os
import sys

import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.functions import ST_AsText, ST_Point
from kafka import KafkaConsumer
from flask_cors import CORS

import multiprocessing

from datetime import datetime

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry.point import Point
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String

from sqlalchemy.ext.hybrid import hybrid_property



DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

# DB_USERNAME = "ct_admin"
# DB_PASSWORD = "password"
# DB_HOST = "localhost"
# DB_PORT = "5432"
# DB_NAME = "geoconnections"


# TOPIC_NAME = 'locations'
# KAFKA_SERVER = '127.0.0.1:9092'



app = Flask(__name__)

CORS(app)  # Set CORS for development

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#logging.basicConfig(level=logging.WARNING)
#logger = logging.getLogger("LocationProcessor-api")

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

@app.route("/health", methods = ['GET'])
def health():
    return jsonify("healthy LocationProcessor")



class LocationProcessor(multiprocessing.Process):
    consumer = None

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def getConsumer(self):
        global consumer
        return consumer

    def run(self):
        global consumer
        try:
            consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, group_id='my_group')
            consumer.subscribe([TOPIC_NAME])
            while not self.stop_event.is_set():
                for location in consumer:
                    location_message = location.value.decode('utf-8')
                    print('{}'.format(location_message))
                    location_message = json.loads(location_message)
                    insertLocation(location_message)
                    if self.stop_event.is_set():
                        break
            consumer.close()
            print("consumer has closed")
            logging.warn("consumer has closed")
        except Exception as e:
            print("consumer generate Exception")
            logging.info("Issue with getting locations from queue" )
            logging.error(e)


consumer_process = None

@app.route("/start", methods = ['POST'])
def start():
    app.logger.info('request start consumer')
    global consumer_process
    if consumer_process is None:
        try:
            consumer_process = LocationProcessor()
            consumer_process.start()
            return jsonify(f"Run consumer on {consumer_process.pid}"), 200
        except Exception as e:
            print(e)

    return jsonify(f"Unable to create consumer process"), 500


@app.route("/status", methods = ['GET'])
def status():
    app.logger.info('request status consumer')
    global consumer_process
    if consumer_process is not None and isinstance(consumer_process, multiprocessing.Process):
        try:
            if not consumer_process.is_alive():
                return jsonify(f"consumer is alive on {consumer_process.pid}"), 200
        except Exception as e:
            print(e)
            return jsonify(f"Unable to get consumer status"), 500

    return jsonify("consumer_process is not running"), 200


@app.route("/destroy", methods = ['POST'])
def stop():
    app.logger.info('Destroy consumer')
    if consumer_process is not None and consumer_process.is_alive():
        consumer_process.stop()
        consumer_process = None
        return jsonify("consumer_process is destroyed"), 200
        
    return jsonify("consumer_process is not running"), 500


def run_app():
    app.run(host='0.0.0.0', debug=True, port=5000)


run_app_process = multiprocessing.Process(target=run_app)



if __name__ == '__main__':
    run_app_process.start()
    run_app_process.join()


    
    

