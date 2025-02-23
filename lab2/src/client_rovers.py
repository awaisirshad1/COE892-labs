import grpc
import ground_control_pb2
import ground_control_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ground_control_pb2_grpc.ground_controlStub(channel)
        print('Enter the rover number:')
        rover_number = input()



if __name__ == '__main__':
    run()
