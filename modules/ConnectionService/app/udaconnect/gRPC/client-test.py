import grpc
import person_event_pb2
import person_event_pb2_grpc


"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""


print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = person_event_pb2_grpc.PersonServiceGrpcStub(channel)



# response = stub.retrieve_all(person_event_pb2.Empty())
# print(response)

personID = person_event_pb2.PersonID(value=1)
response = stub.retrieve(personID)
print(response)



