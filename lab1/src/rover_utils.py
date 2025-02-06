import requests
import json
import copy

'''
HOW TO CHANGE DIRECTION:
    south, east, north, west, will use index of 'directions' to indicate the
    current direction through the variable current_direction

    The order of the directions is important, since the rover can only turn left
    or right, start off as if the rover is facing south, then turning left will 
    would make you face west. Four consecutive left turns, starting from facing 
    south, will have you facing east, north, west and south again. Therefore, we
    can simulate turning left by adding 1 to the current_direction variable, and
    modulo it by 4 so that we don't ever get an index that is out of bounds from
    the directions array. Similarly, turning right will have the opposite effect, 
    so we can subtract 1 from current_direction and modulo it by 4 again. However,
    in the event, we get a negative value from doing this, such as going from 
    south to west, we can simply add 4 to it, then modulo it by 4. In the case of
    south to west, current_direction would go from 0 to -1. Adding 4 to it would 
    give you 3, 3 % 4 = 3, so we successfully go from south to west. This method
    also works for positive numbers. Going from south to east gets you from 0 to
    1, adding 4 gets you 5, 5 % 4 = 1, which is still east. Therefore, we can
    apply this to all changes in direction. As such: 
    direction = 0 (south)
    new_direction = (direction + 4 + 1/-1 (left/right) % 4 

MAKING MOVES
    Since there are only two possibilities of moves, move forward and dig, all 
    that needs to be done is check which move we do and set current_action to 0 or
    1. In the event of encountering a mine, and we don't dig, the rover explodes.
    To test for this, every time the current_position coincides with a mine, we 
    look ahead to the next index in the string rover_moves and if it is not a 
    dig action, then we can break out of the loop and return the path_i.txt file.
    
    We start facing south at the indices [0,0] of our movemap. Based on the state
    of the current_direction variable, a forward move changes our indices. If the
    rover's movement would result in it going out of bounds, we disregard the move.
    This is done by checking the indices for whether they are equal to 0 or one of
    num_rows-1 and num_columns-1, and if they are, disregard it. Otherwise, we can
    add the value of the following map to the current_position variable:
    
    change_in_position = { 'N': (-1,0), 'S': (1,0), 'E': (0,1), 'W': (0,-1) }

    The value of each key-value pair corresponds to the change in current_position
    that would be the result of a movement forward in the respective direction. A
    movement forward in the north direction would result in us going 1 row upward, 
    which would be achieved by decrementing the row index, which corresponds to 
    current_position = [i, j] + [-1, 0]. 
    
DRAWING THE path_i.txt FILE
    I am operating under the assumption that the rover can't go out of bounds of
    the defined map. If it attempts to move forward out of the boundaries, that 
    move will simply be disregarded. 

    Drawing the rover's path on the given map is simple. Create an empty array the
    size of the given map. Initialize it with all 0s. Iterate over the rover's 
    moves and adjust the current_position and current_direction variables 
    accordingly. If we do not encounter any mines, set the value of the array to
    '*' to indicate the rover's path. If a mine is encountered, and if the next 
    character in the string of the rover's moves is not to dig, set the value of
    the resulting array's element corresponding to the rover's current_position
    to 'X' to indicate the rover blowing up and disregard all the rover's remaining
    moves. If the rover blows up, we should check all elements in the resulting 
    array where the rover did not pass over that correspond to mines on the map 
    and set their values to 1 to indicate mines it didn't encounter. 

    Iterating over the string representation of the rover's moves, by index, allows
    for us to look one character ahead when we encounter a mine. We will always have
    current_position, a 2-element array, be the indices we want to set the value of
    the resulting array to. 
'''


# API to extract rover moves based on number
def extract_rover_moves(url: str, num: int):
    res = requests.get(url + f'/{num}')
    if res.status_code == 200:
        json_data = json.loads(res.text)
        # print(json_data['data']['moves'])
        return json_data['data']['moves']


# API to extract map into a 2D array
def extract_map_into_array(file_path: str):
    # read all integers in the map file
    map_contents = [int(i) for i in open(file_path).read().split() if i.isnumeric()]
    # first integer is number of rows, second integer is number of columns
    num_rows, num_columns = map_contents[0], map_contents[1]
    # after we've assigned these to variables, pop them off the array
    map_without_dimensions = map_contents[2:]
    # Now we can take the remaining numbers (which should all be 1s and 0s)
    # and assign them to a 2D array based on numbers of rows and columns
    map_txt_contents = [[None for j in range(num_columns)] for i in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_columns):
            map_txt_contents[i][j] = map_without_dimensions.pop(0)
    # return the 2D array
    return map_txt_contents


# API to draw moves in 'result' array for a given rover
def draw_rover_path(rover_moves: str, map_txt: list, disarm_all_mines: bool):
    # deep copy the map_txt so that the original is never modified:
    map_copy = copy.deepcopy(map_txt)
    current_direction = 0
    directions = ['S', 'E', 'N', 'W']
    current_position = [0, 0]
    change_in_position = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    num_rows = len(map_copy)
    num_columns = len(map_copy[0])
    right_boundary = num_columns - 1
    lower_boundary = num_rows - 1
    # the following boolean value is set to true upon encountering D for part 2
    dig_instruction_given = False
    # the result will be stored in this array
    result = [[None for j in range(num_columns)] for k in range(num_rows)]
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
                        # if we are on a mine, blow up, unless we've been given the continuous dig instruction
                        if map_copy[current_position[0]][current_position[1]] == 1 and not dig_instruction_given:
                            result[current_position[0]][current_position[1]] = 'X'
                            break
                        # otherwise, move forward
                        else:
                            result[current_position[0]][current_position[1]] = '*'
                            current_position = [current_position[idx] + change_in_position.get(directions[current_direction])[idx] for idx in range(2)]
                # if we aren't changing directions or moving forward, only possible instruction is to dig
                elif rover_moves[i] == 'D':
                    if disarm_all_mines: dig_instruction_given = True
                    # are we on a mine? if yes, it is disarmed
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
        # print(f'map_txt:{map_txt}')
        # print(f'map_copy:{map_copy}')
        return result
    except ValueError:
        print(f'error:{ValueError}')


# API to print the resulting array to a text file, called path_i.txt
def print_path_to_file(path: str, i: int, path_array: list):
    # print(f'path_array:{path_array}\n')
    f = open(f'{path}/path_{i}.txt', 'w')
    for j in range(len(path_array)):
        for k in range(len(path_array[j])):
            f.writelines(path_array[j][k]+' ')
        f.write('\n')

