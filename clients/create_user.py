import grpc
import sys
sys.path.insert(0, "../protos")

import user_pb2_grpc
from user_pb2 import CreateUserRequest

def create_user_success(channel: grpc.Channel):
    name = "Jim Chen"
    password = "AaBbCcDdEeFf123"
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = CreateUserRequest(name=name, password=password)
    response = stub.CreateUser(request)
    # print("Response Object: ", response)
    print("\n\nCreate User Success")
    print("User Id: ", response.id)
    print("User Name: ", response.name)
    print("User Token: ", response.token)

def create_user_duplicate_name_error(channel: grpc.Channel):
    name = "Jim Chen"
    password = "AaBbCcDdEeFf123"
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = CreateUserRequest(name=name, password=password)
    try:
        response = stub.CreateUser(request)
    except grpc.RpcError as e:
        # print("Error Object: ", e)
        print("\n\nCreate User Duplicate Name Error")
        print("Error Code: ", e.code())
        print("Error Details: ", e.details())
        print("Debug String: ", e.debug_error_string())

def create_user_name_too_short_error(channel: grpc.Channel):
    name = "a"   # length < 3
    password = "AaBbCcDdEeFf123"
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = CreateUserRequest(name=name, password=password)
    try:
        response = stub.CreateUser(request)
    except grpc.RpcError as e:
        # print("Error Object: ", e)
        print("\n\nCreate User Name Too Short Error")
        print("Error Code: ", e.code())
        print("Error Details: ", e.details())
        print("Debug String: ", e.debug_error_string())

def create_user_name_too_long_error(channel: grpc.Channel):
    name = "abcdefghijklmnopqrstuvwxyz0123456789"   # length > 32
    password = "AaBbCcDdEeFf123"
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = CreateUserRequest(name=name, password=password)
    try:
        response = stub.CreateUser(request)
    except grpc.RpcError as e:
        # print("Error Object: ", e)
        print("\n\nCreate User Name Too Long Error")
        print("Error Code: ", e.code())
        print("Error Details: ", e.details())
        print("Debug String: ", e.debug_error_string())

def create_user_password_too_short_error(channel: grpc.Channel):
    name = "Fail Case"
    password = "abcd"   # length < 8
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = CreateUserRequest(name=name, password=password)
    try:
        response = stub.CreateUser(request)
    except grpc.RpcError as e:
        # print("Error Object: ", e)
        print("\n\nCreate User Password Too Short Error")
        print("Error Code: ", e.code())
        print("Error Details: ", e.details())
        print("Debug String: ", e.debug_error_string())

def create_user_password_too_long_error(channel: grpc.Channel):
    name = "Fail Case"
    password = "abcdefghijklmnopqrstuvwxyz0123456789"   # length > 32
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = CreateUserRequest(name=name, password=password)
    try:
        response = stub.CreateUser(request)
    except grpc.RpcError as e:
        # print("Error Object: ", e)
        print("\n\nCreate User Password Too Long Error")
        print("Error Code: ", e.code())
        print("Error Details: ", e.details())
        print("Debug String: ", e.debug_error_string())

def create_user_password_format_error(channel: grpc.Channel):
    name = "Fail Case"
    password = "A0123456789"   # Without Lowercase Letter
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = CreateUserRequest(name=name, password=password)
    try:
        response = stub.CreateUser(request)
    except grpc.RpcError as e:
        # print("Error Object: ", e)
        print("\n\nCreate User Password Format Error")
        print("Error Code: ", e.code())
        print("Error Details: ", e.details())
        print("Debug String: ", e.debug_error_string())

if __name__ == '__main__':
    channel = grpc.insecure_channel('localhost:50051')
    
    create_user_success(channel)
    
    create_user_duplicate_name_error(channel)
    
    create_user_name_too_short_error(channel)
    create_user_name_too_long_error(channel)
    
    create_user_password_too_short_error(channel)
    create_user_password_too_long_error(channel)
    
    create_user_password_format_error(channel)
