import grpc
from concurrent import futures
import subprocess
from src.communication.grpc_services import worker_pb2
from src.communication.grpc_services import worker_pb2_grpc

class WorkerActions(worker_pb2_grpc.WorkerServiceServicer):
    def __init__(self):
        self.workers = {}

    def ManageWorker(self, request_iterator, context):
        print("Client connected for worker management.")
        for command in request_iterator:
            print(f"Command received: {command}")

            worker_id = command.worker_id
            action = command.action.upper()

            print(f"Received command: {action} for Worker ID: {worker_id}")

            if action == "START":
                status = self.start_worker(worker_id)
            elif action == "STOP":
                status = self.stop_worker(worker_id)
            elif action == "RESTART":
                status = self.restart_worker(worker_id)
            else:
                status = worker_pb2.WorkerStatus(
                    worker_id=worker_id, status="ERROR", message="Unknown action."
                )

            yield status

    def start_worker(self, worker_id):
        if worker_id in self.workers and self.workers[worker_id].poll() is None:
            return worker_pb2.WorkerStatus(worker_id=worker_id, status="RUNNING", message="Worker already running.")

        try:
            process = subprocess.Popen(["python3", "/home/eros/nedo-worker-lib/main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.workers[worker_id] = process
            return worker_pb2.WorkerStatus(worker_id=worker_id, status="RUNNING", message="Worker started successfully.")
        except Exception as e:
            return worker_pb2.WorkerStatus(worker_id=worker_id, status="ERROR", message=str(e))

    def stop_worker(self, worker_id):
        process = self.workers.get(worker_id)
        if process and process.poll() is None:
            process.terminate()
            process.wait()
            del self.workers[worker_id]
            return worker_pb2.WorkerStatus(worker_id=worker_id, status="STOPPED", message="Worker stopped successfully.")
        return worker_pb2.WorkerStatus(worker_id=worker_id, status="ERROR", message="No running Worker to stop.")

    def restart_worker(self, worker_id):
        stop_status = self.stop_worker(worker_id)
        if stop_status.status == "ERROR":
            return stop_status
        return self.start_worker(worker_id)