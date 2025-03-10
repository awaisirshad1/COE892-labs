import grpc
import pika

import ground_control_pb2
import ground_control_pb2_grpc
import rover_utils as rvr
import copy


def deserialize_map_into_array(response: ground_control_pb2.TwoDimensionalIntArray):
    arr = []
    for val in response.row:
        arr.append(val.values)
    return arr


def draw_rover_path(rover_num: int, rover_moves: str, map_txt: list, stub: ground_control_pb2_grpc.GroundControlStub, rabbit_channel, demine_queue: str, exchange_name: str, routing_key: str):
    # deep copy the map_txt so that the original is never modified:
    map_copy = copy.deepcopy(map_txt)
    mines = []
    current_direction = 0
    directions = ['S', 'E', 'N', 'W']
    current_position = [0, 0]
    change_in_position = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    num_rows = len(map_copy)
    num_columns = len(map_copy[0])
    right_boundary = num_columns - 1
    lower_boundary = num_rows - 1
    mine_counter = 0
    # the result will be stored in this array
    result = [[None for j in range(num_columns)] for k in range(num_rows)]
    # valid pins will be stored in this array
    valid_pins = []
    i = 0
    try:
        for i in range(len(rover_moves)):
            # direction change?
            if rover_moves[i] == 'R' or rover_moves[i] == 'L':
                # if we are turning left
                if rover_moves[i] == 'L':
                    current_direction = (current_direction + 5) % 4
                # if we are turning right
                else:
                    current_direction = (current_direction + 3) % 4
            # no direction change
            else:
                # are we moving forward?
                if rover_moves[i] == 'M':
                    # if we are not at a border
                    # if we are facing south (0) and not at the lower boundary OR
                    # if we are facing north (2) and not at the upper boundary OR
                    # if we are facing east (1) and not at the right boundary OR
                    # if we are facing west (3) and not at the left boundary
                    # THEN we may move forward depending on if we are on a mine
                    if (current_direction == 0 and current_position[0] != lower_boundary) or (
                            current_direction == 2 and current_position[0] != 0) or (
                            current_direction == 1 and current_position[1] != right_boundary) or (
                            current_direction == 3 and current_position[1] != 0):
                        # print(f'current_position:{current_position}')
                        # if we are on a mine, publish the encountered mine to demine-queue and continue moving
                        if map_copy[current_position[0]][current_position[1]] == 1:
                            print(f'encountered mine at [{current_position[0]},{current_position[1]}], fetching serial number then computing pin...' )
                            map_copy[current_position[0]][current_position[1]] = 0
                            serial_num = get_mine_serial_number_from_server(rover_num, stub)
                            if serial_num not in mines:
                                mines.append(serial_num)
                            publish_mine_to_demine_queue(rabbit_channel, rover_num, current_position, mine_counter, serial_num, demine_queue, exchange_name, routing_key)
                        # move forward
                        current_position = [current_position[idx] + change_in_position.get(directions[current_direction])[idx] for idx in range(2)]
                # if we aren't changing directions or moving forward, only possible instruction is to dig
                elif rover_moves[i] == 'D':
                    print('D command encountered, auto dig enabled, ignoring dig command...')
                    # do nothing
                # no conditions met, therefore input error
                else:
                    raise Exception('Invalid string input for rover moves: contains invalid character that is not L,'
                                    'R,M,D')
    except ValueError:
        print(f'error:{ValueError}')


def get_mine_serial_number_from_server(rover_number: int, stub: ground_control_pb2_grpc.GroundControlStub):
    response = stub.GetMineSerialNumber(ground_control_pb2.RoverNumber(number=rover_number))
    print(f'serial number response:{response}')
    return response.value


def publish_mine_to_demine_queue(channel, rover_number: int, coordinates: list, mine_id: int, serial_number: str, demine_queue: str, exchange_name: str, routing_key: str):
    message = f'CLIENT: rover_number={rover_number},encountered_mine_id={mine_id},serial_number={serial_number},coordinates={coordinates}'
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)



def run():
    ran_rovers = []
    with grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        while(True):
            # grpc stub
            stub = ground_control_pb2_grpc.GroundControlStub(channel)
            # rabbitmq publisher setup
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            rabbit_channel = connection.channel()
            demine_queue = 'demine_queue'
            exchange_name = 'lab3'
            routing_key = 'demine_info'
            rabbit_channel.exchange_declare(
                exchange=exchange_name,
                exchange_type='direct',
                durable=True,
                auto_delete=False
            )
            rabbit_channel.queue_declare(queue=demine_queue, durable=True)
            rabbit_channel.queue_bind(exchange=exchange_name,queue=demine_queue, routing_key=routing_key)
            print('Enter the rover number:')
            rover_number = int(input())
            # validate rover number is from 1-10
            if rover_number not in range(1, 11):
                print('Invalid rover number')
                exit(1)
            if rover_number in ran_rovers:
                print(f'Already computed path for rover number {rover_number}')
                continue
            # get the map
            response = stub.GetMap(ground_control_pb2.Empty())
            # extract it into an array and print
            rover_land_array = deserialize_map_into_array(response)
            print(f'rover_land_array:{rover_land_array}')
            # now get the movements for the given rover
            rover_movements = stub.GetRoverMovements(ground_control_pb2.RoverNumber(number=rover_number))
            print(f'rover_movements:{rover_movements}')
            # now start processing the rover's moves
            draw_rover_path(rover_number, rover_movements.value, rover_land_array, stub, rabbit_channel, demine_queue, exchange_name, routing_key)
            uinput = input('rover path computed, enter \'exit\' if you wish to exit, otherwise press enter: ')
            if(uinput.lower()=='exit'):
                rabbit_channel.close()
                connection.close()
                print('Goodbye!')
                break
            else:
                continue



if __name__ == '__main__':
    run()
