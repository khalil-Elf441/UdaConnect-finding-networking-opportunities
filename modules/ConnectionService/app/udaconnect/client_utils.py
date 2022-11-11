import grpc

# import person_event_pb2
# import person_event_pb2_grpc

from app.udaconnect import person_event_pb2
from app.udaconnect import person_event_pb2_grpc


import asyncio

import psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from typing import Dict, List


DB_USERNAME = "ct_admin"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "geoconnections"

# SQLALCHEMY_DATABASE_URI = (
#     f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# )

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""


print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = person_event_pb2_grpc.PersonServiceGrpcStub(channel)


class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String, nullable=False)
    last_name = db.Column(String, nullable=False)
    company_name = db.Column(String, nullable=False)



def grpc_client_retrieve_all() -> List[Person]:
    rpcPersonlist = stub.retrieve_all(person_event_pb2.Empty())
    # print(rpcPersonlist)
    PersonlistModel = []
    for rpcPerson in rpcPersonlist.persons:
        PersonlistModel.append(rpc_to_model(rpcPerson))
    return PersonlistModel


def grpc_client_retrieve(person_id: int) -> Person :
    personID = person_event_pb2.PersonID(value=person_id)
    rpcPerson = stub.retrieve(personID)
    personModel = rpc_to_model(rpcPerson)
    return personModel


def rpc_to_model(rpc_Person) -> Person:
    new_person = Person()
    new_person.id = rpc_Person.id
    new_person.first_name = rpc_Person.first_name
    new_person.last_name = rpc_Person.last_name
    new_person.company_name = rpc_Person.company_name
    return new_person

try:
    print("Person list")
    print(grpc_client_retrieve_all())

    print("Person by id")
    person = grpc_client_retrieve(1)
    print(person.first_name)

except Exception as e:
    print(e)





