import logging
from datetime import datetime, timedelta
from typing import Dict, List
import json

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from datetime import datetime

from kafka import KafkaProducer

TOPIC_NAME = 'locations'
KAFKA_SERVER = '127.0.0.1:9092'

DATE_FORMAT = "%Y-%m-%d"

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("LocationService-api")


# @TODO refacto as independent service
class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        # validation_results: Dict = LocationSchema().validate(location)
        # if validation_results:
        #     logger.warning(f"Unexpected data format in payload: {validation_results}")
        #     raise Exception(f"Invalid payload: {validation_results}")
        # creation_time : SELECT FORMAT(GetDate(),'yyyy-mm-dd')
        

        new_location = {
            "person_id": location["person_id"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "creation_time": str(location["creation_time"])
            }
            
        try:    
            location_encode_data = json.dumps(new_location, indent=2).encode('utf-8')
            producer.send(TOPIC_NAME, location_encode_data)
            producer.flush()
            return {"OK"}
        except :
            return {"ERROR"}


    @staticmethod
    def retrieve_person_datediff(person_id: int, start_date: datetime, end_date: datetime) -> Location:
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        return locations

