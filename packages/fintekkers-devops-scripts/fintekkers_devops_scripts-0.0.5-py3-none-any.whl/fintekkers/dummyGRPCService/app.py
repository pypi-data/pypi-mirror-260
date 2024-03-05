from concurrent import futures
import grpc

from fintekkers.dummyGRPCService.generated import echo_pb2_grpc
from fintekkers.dummyGRPCService.grpc import Echoer

class Server:
    @staticmethod
    def run():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        echo_pb2_grpc.add_EchoServicer_to_server(Echoer(), server)
        server.add_insecure_port('[::]:50051')
        server.add_secure_port('[::]:50052', server_credentials=)
        server.start()
        server.wait_for_termination()
