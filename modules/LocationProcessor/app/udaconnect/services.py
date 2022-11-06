import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

from kafka import KafkaConsumer


TOPIC_NAME = 'locations'
KAFKA_SERVER = 'localhost:9092'

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("LocationProcessor-api")

class LocationProcessor:
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(TOPIC_NAME)

        while not self.stop_event.is_set():
            for location in consumer:
                db.session.add(location)
                db.session.commit()
                if self.stop_event.is_set():
                    break

        consumer.close()

