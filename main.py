import grpc
from concurrent import futures

from pypb2 import user_pb2_grpc
from service.user_service import UserService

def serve():
    thread_pool = futures.ThreadPoolExecutor(max_workers=10)
    server = grpc.server(thread_pool=thread_pool)
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()