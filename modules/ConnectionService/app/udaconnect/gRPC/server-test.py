from concurrent import futures

import grpc
import person_event_pb2
import person_event_pb2_grpc

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

class PersonServiceGrpc(person_event_pb2_grpc.PersonServiceGrpcServicer):

    def retrieve_all(self, request, context):
        print("retrieve_all has been requeted")
        print(request)

        # simulate db query with psycopg2
        # conn = psycopg2.connect(
        #     database="geoconnections", user='ct_admin', password='password', host='127.0.0.1', port= '5432'
        # )
        # cursor = conn.cursor()
        # cursor.execute('''SELECT * from person''')
        # result = cursor.fetchall()
        # print(result)

        # simulate db query with SQLAlchemy
        PersonList = [db.session.query(Person).all()]

        PersonListGRPC = []
        for person in PersonList:
         person = person_event_pb2.OrderMessage(
              id = person.id,
              first_name = person.first_name,
              last_name = person.last_name,
              company_name = person.company_name
         )
         PersonListGRPC.append(person)



        result = person_event_pb2.PersonMessageList()
        return result

    def retrieve(self, request, context):
        print("retrieve has been requeted")
        print(request)

        result = person_event_pb2.PersonMessage()
        return result


class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String, nullable=False)
    last_name = db.Column(String, nullable=False)
    company_name = db.Column(String, nullable=False)



# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_event_pb2_grpc.add_PersonServiceGrpcServicer_to_server(PersonServiceGrpc(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()