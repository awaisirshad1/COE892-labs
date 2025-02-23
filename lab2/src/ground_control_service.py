from concurrent import futures
import time
import grpc
import ground_control_pb2
import ground_control_pb2_grpc
import rover_utils as rvr


class ground_control_servicer(ground_control_pb2_grpc.ground_controlServicer):
    # get the map into an array
    def get_map(self, request, context):
        return rvr.extract_map_into_array('../map_and_mines/map1.txt')

    def get_movements(self, request, context):
        rover_num = request.rover_number
        print()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    ground_control_pb2_grpc.add_ground_controlServicer_to_server(ground_control_servicer(), server)
    server.add_secure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

