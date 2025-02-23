from concurrent import futures
import time
import grpc
import ground_control_pb2
import ground_control_pb2_grpc
import rover_utils as rvr


class GroundControlServicer(ground_control_pb2_grpc.ground_controlServicer):
    # get the map into an array
    def get_map(self, request, context):
        print(request)
        response = ground_control_pb2.land__array__pb2
        map_array = rvr.extract_map_into_array('../map_and_mines/map1.txt')
        print(f'map_array:{map_array}')
        response.values = map_array
        return response

    def get_movements(self, request, context):
        print(request)
        rover_num = request.rover_number
        print(f'rover_num:{rover_num}')

    def get_mine_serial_number(self, request, context):
        print(request)

    def rover_status(self, request, context):
        print(request)

    def share_mine_pin(self, request, context):
        print(request)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    ground_control_pb2_grpc.add_ground_controlServicer_to_server(GroundControlServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()


