from concurrent import futures

import grpc

from app.udaconnect import person_event_pb2
from app.udaconnect import person_event_pb2_grpc

import psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from typing import Dict, List


# DB_USERNAME = "ct_admin"
# DB_PASSWORD = "password"
# DB_HOST = "localhost"
# DB_PORT = "5432"
# DB_NAME = "geoconnections"


DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


# SQLALCHEMY_DATABASE_URI = (
#     f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# )

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PersonServiceGrpc(person_event_pb2_grpc.PersonServiceGrpcServicer):

    def retrieve_all(self, request, context):
        print("retrieve_all has been requeted")
        PersonList = db.session.query(Person).all()
        db.session.commit()
        PersonListGRPC = person_event_pb2.PersonMessageList()
        for person in PersonList:
             rpc_person = person_event_pb2.PersonMessage(
                  id = int(person.id),
                  first_name = person.first_name,
                  last_name = person.last_name,
                  company_name = person.company_name
             )
             PersonListGRPC.persons.append(rpc_person)

        return PersonListGRPC

    def retrieve(self, request, context):
        print("retrieve has been requeted")
        person_id = request.value
        person = db.session.query(Person).get(person_id)
        db.session.commit()
        rpc_person = person_event_pb2.PersonMessage(
            id = int(person.id),
            first_name = person.first_name,
            last_name = person.last_name,
            company_name = person.company_name
        )

        return rpc_person


class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String, nullable=False)
    last_name = db.Column(String, nullable=False)
    company_name = db.Column(String, nullable=False)



# Initialize gRPC server
def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    person_event_pb2_grpc.add_PersonServiceGrpcServicer_to_server(PersonServiceGrpc(), server)

    print("Server starting on port 5005...")
    server.add_insecure_port("[::]:5005")
    server.start()
    server.wait_for_termination()