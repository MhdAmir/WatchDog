from src.communication.grpc_server import create_grpc_server

if __name__ == "__main__":
    port = 50051
    server = create_grpc_server(port)
    print(f"Server running on port {port}")
    server.start()
    server.wait_for_termination()
