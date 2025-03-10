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


def draw_rover_path(rover_num: int, rover_moves: str, map_txt: list, stub: ground_control_pb2_grpc.GroundControlStub):
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
    autodig = True
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
                        # if we are on a mine, fetch serial number from server, compute pin and disarm
                        if map_copy[current_position[0]][current_position[1]] == 1:
                            print(f'encountered mine at [{current_position[0]},{current_position[1]}], fetching serial number then computing pin...' )
                            serial_num = get_mine_serial_number_from_server(rover_num, stub)
                            if serial_num not in mines:
                                mines.append(serial_num)
                            valid_pins.append(rvr.compute_pin_for_given_mine_sequential(mines[mine_counter-1]))
                            print(f'found valid pin, now notifying server of the valid pin for this serial number')
                            # now inform the server of the valid pin
                            response = stub.ShareMinePin(ground_control_pb2.RoverNumberWithMineSerialAndPin(roverNumber=rover_num, mineSerialNumber=mines[mine_counter-1], minePin=valid_pins[-1]))
                            print(f'server response:{response}')
                            map_copy[current_position[0]][current_position[1]] = 0
                        # otherwise, move forward
                        else:
                            result[current_position[0]][current_position[1]] = '*'
                            current_position = [current_position[idx] + change_in_position.get(directions[current_direction])[idx] for idx in range(2)]
                # if we aren't changing directions or moving forward, only possible instruction is to dig
                elif rover_moves[i] == 'D':
                    # are we on a mine? if yes we compute the pin for part 2
                    if map_copy[current_position[0]][current_position[1]] == 1:
                        map_copy[current_position[0]][current_position[1]] = 0
                #       otherwise, do nothing
                # no conditions met, therefore input error
                else:
                    raise Exception('Invalid string input for rover moves: contains invalid character that is not L,'
                                    'R,M,D')
        # now fill in the rest of the map where the rover did not traverse
        # their values in the 'result' array will be None, so only replace values equal to None
        result = [[str(map_copy[x][y]) if result[x][y] is None else str(result[x][y]) for y in range(num_columns)] for x in range(num_rows)]
        # make a dictionary for each mine and its respective valid pin
        mines_and_their_valid_pins = dict(zip(mines, valid_pins))
        # print(f'map_txt:{map_txt}')
        # print(f'map_copy:{map_copy}')
        return result, mines_and_their_valid_pins
    except ValueError:
        print(f'error:{ValueError}')


def get_mine_serial_number_from_server(rover_number: int, stub: ground_control_pb2_grpc.GroundControlStub):
    response = stub.GetMineSerialNumber(ground_control_pb2.RoverNumber(number=rover_number))
    print(f'serial number response:{response}')
    return response.value


def share_mine_pin_with_server(rover_number: int, serial_number: str, pin: str,  stub: ground_control_pb2_grpc.GroundControlStub):
    response = stub.ShareMinePin(ground_control_pb2.RoverNumberWithMineSerialAndPin(rover_number=rover_number, mineSerialNumber=serial_number, minePin=pin))
    print(f'server response after sharing pin: {response}')
    return



def run():
    connection = pika.BlockingConnection
    with grpc.insecure_channel('localhost:50051',options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = ground_control_pb2_grpc.GroundControlStub(channel)
        print('Enter the rover number:')
        rover_number = int(input())
        # validate rover number is from 1-10
        if rover_number not in range(1,11):
            print('Invalid rover number')
            exit(1)
        # get the map
        response = stub.GetMap(ground_control_pb2.Empty())
        # extract it into an array and print
        rover_land_array = deserialize_map_into_array(response)
        print(f'rover_land_array:{rover_land_array}')
        # now get the movements for the given rover
        rover_movements = stub.GetRoverMovements(ground_control_pb2.RoverNumber(number=rover_number))
        print(f'rover_movements:{rover_movements}')
        # now start processing the rover's moves
        result, valid_pins = draw_rover_path(rover_number, rover_movements.value, rover_land_array, stub)
        print(f'result:{result},valid_pins:{valid_pins}')
        # now share the status with the server:
        rover_status = "failure" if all('X' in subs for subs in result) else "success"
        status_code = 1 if rover_status == "failure" else 0
        response = stub.RoverStatus(ground_control_pb2.Status(statusCode=status_code, message=rover_status))
        print(f'response from server:{response}')


# def publish_mine_to_demine_queue():



if __name__ == '__main__':

    run()
