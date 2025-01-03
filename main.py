import grpc
from concurrent import futures
import time

from resource.SystemInfo import SystemInfo
from communication.Protos import worker_server_pb2
from communication.Protos import worker_server_pb2_grpc

class WorkerServer(worker_server_pb2_grpc.WorkerServerServicer):
    def __init__(self):
        self.system_info = SystemInfo()

    def GetSystemInfo(self, request, context):
        common_info = self.system_info.get_common_info()

        response = worker_server_pb2.SystemInfoResponse(
            cpu_processor=common_info["cpu_processor"],
            cpu_physical_core=common_info["cpu_physical_core"],
            cpu_total_core=common_info["cpu_total_core"],
            system_platform=common_info["system_platform"],
            system_platform_version=common_info["system_platform_version"],
            system_ram=common_info["system_ram"],
        )
        for gpu in common_info["gpu"]:
            response.gpu.add(
                gpu_uuid=gpu["gpu_uuid"],
                gpu_name=gpu["gpu_name"],
                gpu_total_memory=gpu["gpu_total_memory"],
            )
        return response

    def SendCommand(self, request, context):
        # Handle commands based on the received type
        if request.command == worker_server_pb2.ControlCommand.START:
            print(f"Received command: START - Starting the worker.")
        elif request.command == worker_server_pb2.ControlCommand.STOP:
            print(f"Received command: STOP - Stopping the worker.")
        elif request.command == worker_server_pb2.ControlCommand.RESTART:
            print(f"Received command: RESTART - Restarting the worker.")
        else:
            print(f"Received unknown command: {request.command}")
        
        return worker_server_pb2.CommandResponse(
            status="SUCCESS",
            message=f"Command {worker_server_pb2.ControlCommand.CommandType.Name(request.command)} executed successfully."
        )

# Define the serve function to start the server
def serve():
    # Set up the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    worker_server_pb2_grpc.add_WorkerServerServicer_to_server(WorkerServer(), server)
    server.add_insecure_port("[::]:50051")
    print("Server is running on port 50051...")
    server.start()

    # Keep the server running
    try:
        while True:
            time.sleep(86400)  # Keep server running
    except KeyboardInterrupt:
        server.stop(0)
        print("Watchdog stopped.")

# Client code to send command requests to the server
def run_client():
    # Connect to the gRPC server
    channel = grpc.insecure_channel('localhost:50051')
    stub = worker_server_pb2_grpc.WorkerServerStub(channel)
    
    # Create and send a ControlCommandRequest with a START command
    command_request = worker_server_pb2.ControlCommandRequest(
        worker_id="worker_1",
        command=worker_server_pb2.ControlCommand.START
    )
    response = stub.SendCommand(command_request)
    print(f"Response: {response.status} - {response.message}")

    # You can repeat this for STOP or RESTART commands
    command_request.command = worker_server_pb2.ControlCommand.STOP
    response = stub.SendCommand(command_request)
    print(f"Response: {response.status} - {response.message}")

if __name__ == "__main__":
    # Start the server
    serve()
    # To run the client, you can uncomment the following line:
    run_client()
