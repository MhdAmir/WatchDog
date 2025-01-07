from concurrent import futures
import grpc
from src.actions.worker_actions import WorkerActions
from src.communication.grpc_services import worker_pb2_grpc

class GRPCServer(worker_pb2_grpc.WorkerServiceServicer):
    def __init__(self):
        self.worker_actions = WorkerActions()

    def ManageWorker(self, request_iterator, context):
        print("Incoming request at ManageWorker")
        return self.worker_actions.ManageWorker(request_iterator, context)

def create_grpc_server(port):
    grpc_server = GRPCServer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    worker_pb2_grpc.add_WorkerServiceServicer_to_server(grpc_server, server)
    server.add_insecure_port(f"[::]:{port}")
    return server
