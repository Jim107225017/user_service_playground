from concurrent import futures
from mongoengine.errors import ValidationError, NotUniqueError
from datetime import datetime, timedelta
from calendar import timegm
from hashlib import pbkdf2_hmac
import grpc
import hmac
import os
import jwt
import sys
sys.path.insert(0, "../protos")
sys.path.insert(0, "../models")

import user_pb2_grpc
from user_pb2 import UserResponse
from user_model import User
from validator import NameValidator, PasswordValidator



class UserService(user_pb2_grpc.UserServiceServicer):

    _JWT_TOKEN_PRIVATE_KEY = """
    MIICXAIBAAKBgQCBQXI//Bq0kPqBFnXJkOnYcjlFY6O8pMs+YOaGSEke9e1EoMkX
    YSmXHSfxYZis9IyZJcFYdR89J52xIjl5pxkEPIM9j3hxNecwgA5R4crfe4eQanjf
    ROPoxSLRdzRmCQlYWDkU6s2VQ0atvxDVqgbEFXPbB09LpQT/o9PG/CEhIwIDAQAB
    AoGAYuOLYWCjndn9jZ19aEUyY6KgJnJg5wa9aHACbmIHb2R/rq3Eq9puU2q/EHG2
    uTwwBUtZbS/OQp94ifjBOE2bWQaCvmiAI+5zGANGPoSDHerf+FK5r9uNAc6xJ3MV
    qC2Mv3cD2HMbWWHIn6DMMsPgsYJ8hLvFufDeLLqOCmQW0oECQQDKB0Xaakm8cBPT
    4R3d0ZmMt2El2o27FX5jxfX1ZuWWN2E64oHaxy/huosS69u0jD03cl0YOjL0Smk0
    MgSERUoTAkEAo8k+K3lkZyanacADf0x71sQT+Cpiqq7A1OZfrqqANR49RKfW7tbE
    e/wWCzvknd4UunB5NvqEgnM+GolJzKCusQJBALg8O6p75TRP7PT6xRbFDscxcAlq
    LnfemPz5yVv6cwIzDJr7droBjZvHVw5xQlF61lSbGWR/pnn65cewmUfaPDsCQFag
    C1em/qln0kemHLNpWl4+mmk40bKAdtCjf5u75c8yTSlQs+bihE0nCOmsJcAxQzlQ
    X2vql8b++KvETNoDaiECQESVet25Ce1zogsVz3pMgChAJOctEl5EklrZNno0hTGy
    p0hTAC7NI8VHxBx+bdAGzVWX2LT5i0y9yYwpafxBbIQ=
    """

    PBKDF2_ITERATIONS = 104450
    DK_LEN = 32

    def CreateUser(self, request, context):
        try:
            NameValidator(name=request.name).validate()
        except ValidationError as err:
            context.set_code(grpc.StatusCode.UNKNOWN)
            context.set_details(f"Name Format Error: {err}")
            return
        
        try:
            PasswordValidator(password=request.password).validate()
        except ValidationError as err:
            context.set_code(grpc.StatusCode.UNKNOWN)
            context.set_details(f"Passoword Format Error: {err}")
            return
        
        now_time = datetime.utcnow()
        expire_time_seconds = timegm((now_time + timedelta(hours=1)).utctimetuple())
        
        salt = os.urandom(32).hex()
        hash_password = self.hash_generator(request.password, salt)
        user = User(name=request.name, password=hash_password, salt=salt)

        try:
            user.save()
        except NotUniqueError as err:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(f"Username [{request.name}] already exists")
            return
        except Exception as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Unexcept Error: {err}")
            return
        
        payload = {
            "token_type": "JWT",
            "user_id": str(user.id),
            "user_name": str(user.name),
            "iat": timegm(now_time.utctimetuple()),
            "exp": expire_time_seconds,
        }
        token = jwt.encode(payload, self._JWT_TOKEN_PRIVATE_KEY, algorithm="HS256")
        response = UserResponse(id=str(user.id), name=user.name, token=token)
        return response

    def GetUser(self, request, context):
        user = User.objects(name=request.name).first()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Username [{request.name}] Login Error")
            return
        
        if not self.hash_comparator(request.password, user.salt, user.password):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Username [{request.name}] Login Error")
            return

        now_time = datetime.utcnow()
        expire_time_seconds = timegm((now_time + timedelta(hours=1)).utctimetuple())
        payload = {
            "token_type": "JWT",
            "user_id": str(user.id),
            "user_name": str(user.name),
            "iat": timegm(now_time.utctimetuple()),
            "exp": expire_time_seconds,
        }
        token = jwt.encode(payload, self._JWT_TOKEN_PRIVATE_KEY, algorithm="HS256")
        response = UserResponse(id=str(user.id), name=user.name, token=token)
        return response
    
    def hash_generator(self, password: str, salt: str) -> str:
        hash_password = pbkdf2_hmac("sha256", 
                                    password=password.encode(), 
                                    salt=salt.encode(), 
                                    iterations=self.PBKDF2_ITERATIONS, 
                                    dklen=self.DK_LEN).hex()
        return hash_password
    
    def hash_comparator(self, password: str, salt: str, db_hash_password: str) -> bool:
        input_hash_password = self.hash_generator(password, salt)
        return hmac.compare_digest(input_hash_password, db_hash_password)

def serve():
    thread_pool = futures.ThreadPoolExecutor(max_workers=10)
    server = grpc.server(thread_pool=thread_pool)
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()