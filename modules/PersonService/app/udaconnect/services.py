import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

from app.udaconnect.server_utils import PersonServiceGrpc

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("PersonService-api")


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.id = int(person["id"])
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        # person = PersonServiceGrpc.retrieve(person_id)
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        # person = PersonServiceGrpc.retrieve(person_id)
        return db.session.query(Person).all()
