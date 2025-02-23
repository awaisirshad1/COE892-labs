import grpc
import ground_control_pb2
import ground_control_pb2_grpc
import google


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ground_control_pb2_grpc.ground_controlStub(channel)
        # print('Enter the rover number:')
        # rover_number = input()
        empty_param = google.protobuf.empty_pb2.Empty()
        response = stub.get_map(empty_param)
        print(response)



if __name__ == '__main__':
    run()
