from concurrent import futures
import time
import grpc
import ground_control_pb2
import ground_control_pb2_grpc
import rover_utils as rvr
import land_array_pb2


class GroundControlServicer(ground_control_pb2_grpc.ground_controlServicer):
    # get the map into an array
    def get_map(self, request, context):
        print(request)
        arr = land_array_pb2.land_array()
        map_array = rvr.extract_map_into_array('../map_and_mines/map1.txt')
        print(f'map_array:{map_array}')
        for sub_map in map_array:
            arr.land_array.extend(sub_map)
        print(arr)
        return arr

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
    server.add_insecure_port('localhost:50051')
    server.start()
    print('server started')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()


