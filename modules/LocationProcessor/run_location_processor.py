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
import traceback

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

app = Flask(__name__)

CORS(app)  # Set CORS for development

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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
    app.logger.info("="*12+"New create Query"+"="*12)
    app.logger.info('{}'.format(location))
    try:
        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()
        app.logger.info("New location has been inserted!")
    except Exception as e:
        app.logger.error("ERROR: Unable to insert the query")
        app.logger.error(e)
        pass
        
    

@app.route("/health", methods = ['GET'])
def health():
    return jsonify("healthy LocationProcessor")



class LocationProcessor(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.consumer = None
    
    
    def stop(self):
        self.stop_event.set()

    def diag(self):
        return {"bootstrap_connected":self.consumer.bootstrap_connected(), "current subscription": self.consumer.subscription()}

    def run(self):
        try:
            if self.consumer is None:
               self.consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER, group_id='my_group')
               app.logger.info("====> Creating Kafka consumer - LocationProcessor")
               app.logger.info("  _                    _   _             ____                                         ")
               app.logger.info(" | |    ___   ___ __ _| |_(_) ___  _ __ |  _ \ _ __ ___   ___ ___  ___ ___  ___  _ __ ")
               app.logger.info(" | |   / _ \ / __/ _` | __| |/ _ \| '_ \| |_) | '__/ _ \ / __/ _ \/ __/ __|/ _ \| '__|")
               app.logger.info(" | |__| (_) | (_| (_| | |_| | (_) | | | |  __/| | | (_) | (_|  __/\__ \__ \ (_) | |   ")
               app.logger.info(" |_____\___/ \___\__,_|\__|_|\___/|_| |_|_|   |_|  \___/ \___\___||___/___/\___/|_|   ")
               app.logger.info("                                                                                      ")
                
            while not self.stop_event.is_set():
                app.logger.info("listenning to the topic(s):")
                app.logger.info(self.consumer.subscription())
                app.logger.info("Is Consumer bootstrap_connected:")
                app.logger.info(self.consumer.bootstrap_connected())
                
                for location in self.consumer:
                    location_message = location.value.decode('utf-8')
                    location_message = json.loads(location_message)
                    insertLocation(location_message)
                    if self.stop_event.is_set():
                        break
            self.consumer.close()
            app.logger.warn("consumer has closed")
        except Exception as e:
            app.logger.error("consumer generate Exception")
            traceback.print_exc()
            app.logger.error("Issue with getting locations from queue" )
            app.logger.error(e)


consumer_process = None

@app.route("/admin/start", methods = ['POST'])
def start():
    app.logger.info('Request start consumer')
    global consumer_process
    if consumer_process is None:
        try:
            consumer_process = LocationProcessor()
            consumer_process.start()
            consumer_process.join()
            return jsonify(f"Consumer is finished"), 200
        except Exception as e:
            traceback.print_exc()
            print(e)

    return jsonify(f"Unable to create consumer process"), 500


@app.route("/admin/status", methods = ['GET'])
def status():
    app.logger.info('Request Status consumer')
    global consumer_process
    if consumer_process is not None and isinstance(consumer_process, multiprocessing.Process):
        try:
            if consumer_process.is_alive():
               return jsonify(f"consumer is alive on {consumer_process.pid}"), 200
        except Exception as e:
            print(e)
            return jsonify(f"Unable to get consumer status"), 500

    return jsonify("consumer_process is not running"), 200


@app.route("/admin/destroy", methods = ['POST'])
def stop():
    app.logger.info('Request Destroy consumer')
    global consumer_process
    if consumer_process is not None:
        if consumer_process.is_alive():
            consumer_process.stop()
        
        consumer_process = None
        return jsonify("consumer_process is destroyed"), 200
        
    return jsonify("Unable to destroy consumer_process"), 500

# Diag kafka Consumer - UNF
#@app.route("/sub", methods = ['GET'])
#def sub():
#    app.logger.info('Destroy consumer')
#    global consumer_process
#    if consumer_process is not None and consumer_process.is_alive():
#        return jsonify(consumer_process.diag()), 200
#        
#    return jsonify("unable to get the current topic subscription"), 500


def run_app():
    # lowest-severity log message (DEBUG)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', debug=True, port=5000)



run_app_process = multiprocessing.Process(target=run_app)



if __name__ == '__main__':
    run_app_process.start()
    run_app_process.join()


    
    

