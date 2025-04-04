from concurrent import futures
import threading
import ground_control_pb2
import ground_control_pb2_grpc
import grpc
import pika
import rover_utils as rvr


class GroundControlServicer(ground_control_pb2_grpc.GroundControlServicer):
    rover_serial_numbers_tracking = {key: 0 for key in range(1, 11)}
    # rover_pins_found = [{} for i in range(1, 11)]
    # rover_statuses = {key: None for key in range(1, 11)}
    mine_serial_numbers = rvr.extract_mines_to_array('../map_and_mines/mines.txt')
    def GetMap(self, request, context):
        print(f'received request to get map: {request}')
        map_array = rvr.extract_map_into_array('../map_and_mines/map1.txt')
        # print(f'map_array:{map_array}')
        response = ground_control_pb2.TwoDimensionalIntArray()
        for row in map_array:
            current_row = ground_control_pb2.IntArray(values=row)
            response.row.append(current_row)
        print(f'got map, returning response...')
        # print(f'response:{response}')
        return response

    def GetRoverMovements(self, request, context):
        rover_path_url = "https://coe892.reev.dev/lab1/rover"
        rover_num = request.number
        print(f'received request for rover movements from rover number: {rover_num}')
        rover_moves = rvr.extract_rover_moves(rover_path_url, rover_num)
        response = ground_control_pb2.String(value=rover_moves)
        print(f'forwarding rover movements...')
        return response

    def GetMineSerialNumber(self, request, context):
        rover_num = int(request.number)
        if GroundControlServicer.rover_serial_numbers_tracking[rover_num] == 10:
            print('already evaluated all serial numbers for the given rover once, restarting from beginning of list')
            GroundControlServicer.rover_serial_numbers_tracking[rover_num] = 0
        serial_num = GroundControlServicer.mine_serial_numbers[GroundControlServicer.rover_serial_numbers_tracking[rover_num]]
        print(f'received request for mine serial number from rover: {request}, returning serial number:{serial_num}')
        GroundControlServicer.rover_serial_numbers_tracking[rover_num] += 1
        # if this serial number is not already in the dictionary for the given rover number, add it
        # for pins_found_rover_n in GroundControlServicer.rover_pins_found[rover_num]:
        #     if serial_num not in pins_found_rover_n:
        #         pins_found_rover_n[serial_num] = None
        response = ground_control_pb2.String(value=serial_num)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    ground_control_pb2_grpc.add_GroundControlServicer_to_server(GroundControlServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    print('server started')
    server.wait_for_termination()


def print_defused_mine(ch, method, properties, body):
    msg = body.decode('utf-8')
    print(f'mine defused: {msg}')


def rabbitmq_defused_mines_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    defused_queue_name = 'defused_mines'
    exchange_name = 'lab3'
    routing_key = 'defuse_info'
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
    channel.queue_declare(queue=defused_queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=defused_queue_name, routing_key=routing_key)
    channel.basic_consume(queue=defused_queue_name, on_message_callback=print_defused_mine, auto_ack=True)
    print('starting consumer')
    channel.start_consuming()


if __name__ == '__main__':
    rabbitmq_thread = threading.Thread(target=rabbitmq_defused_mines_consumer)
    rabbitmq_thread.start()
    serve()