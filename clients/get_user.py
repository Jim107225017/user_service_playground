import grpc
import sys
sys.path.insert(0, "../")

from pypb2 import user_pb2_grpc
from pypb2.user_pb2 import GetUserRequest

def get_user_success(channel: grpc.Channel):
    name = "Jim Chen"
    password = "AaBbCcDdEeFf123"
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = GetUserRequest(name=name, password=password)
    response = stub.GetUser(request)
    # print("Response Object: ", response)
    print("\n\Get User Success")
    print("User Id: ", response.id)
    print("User Name: ", response.name)
    print("User Token: ", response.token)

def get_user_incorrect_password_error(channel: grpc.Channel):
    name = "Jim Chen"
    password = "123"
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = GetUserRequest(name=name, password=password)
    try:
        response = stub.GetUser(request)
    except grpc.RpcError as e:
        # print("Error Object: ", e)
        print("\n\nGet User Incorrect Password Error")
        print("Error Code: ", e.code())
        print("Error Details: ", e.details())
        print("Debug String: ", e.debug_error_string())

def get_user_incorrect_name_error(channel: grpc.Channel):
    name = "Jimmy Chen"
    password = "123"
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = GetUserRequest(name=name, password=password)
    try:
        response = stub.GetUser(request)
    except grpc.RpcError as e:
        # print("Error Object: ", e)
        print("\n\nGet User Incorrect Name Error")
        print("Error Code: ", e.code())
        print("Error Details: ", e.details())
        print("Debug String: ", e.debug_error_string())


if __name__ == '__main__':
    channel = grpc.insecure_channel('localhost:50051')
    
    get_user_success(channel)
    
    get_user_incorrect_password_error(channel)
    get_user_incorrect_name_error(channel)
