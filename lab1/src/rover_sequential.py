import requests
import json
import time


# API to extract rover moves based on number
def extract_rover_path(url: str, num: int):
    res = requests.get(url + f'/{num}')
    if res.status_code == 200:
        json_data = json.loads(res.text)
        # print(json_data['data']['moves'])
        return json_data['data']['moves']


# API to extract map into a 2D array
def extract_map_into_array(path: str):
    # read all integers in the map file
    map_contents = [int(i) for i in open(path).read().split() if i.isnumeric()]
    # first integer is number of rows, second integer is number of columns
    num_rows, num_columns = map_contents[0], map_contents[1]
    # after we've assigned these to variables, pop them off the array
    map_contents = map_contents[2:]
    # map_contents.pop(0)
    # Now we can take the remaining numbers (which should all be 1s and 0s)
    # and assign them to a 2D array based on numbers of rows and columns
    mine_map = [[None for j in range(num_columns)] for i in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_columns):
            mine_map[i][j] = map_contents.pop(0)
    # return the 2D array
    return num_rows, num_columns, mine_map


# API to create cartesian plane grid with map contents
def create_grid(rover_moves: str, mine_map: list):
    max_possible_moves_forward = rover_moves.count('M')
    return 0


# API to calculate the path of the rover
def create_path(rover_moves: str, rover_num: int, mine_map: list):
    # starting off by facing south
    current_direction = 0
    current_action = 0
    current_position = [0,0]
    grid = [[]]
    '''
    
    
    HOW TO CHANGE DIRECTION:
      south, east, north, west, will use index of this list to indicate direction
      the order of the directions is important, since the rover can only turn left
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
      apply this to all changes in direction. 
    
    MAKING MOVES
      since there are only two possibilities of moves, move forward and dig, all 
      that needs to be done is check which move we do and set current_action to 0 or
      1. In the event of encountering a mine, and we don't dig, the rover explodes.
      To test for this, every time the current_position coincides with a mine, we 
      look ahead to the next index in the string rover_moves and if it is not a 
      dig action, then we can break out of the loop and return the path_i.txt file.
      
    DRAWING THE path_i.txt FILE
      Note: I am operating under the assumption that if the rover is to go out of
      the boundaries of the given map, we are to assume that the rover is NOT to be
      brought back in on its own (think of pac-man going out of bounds on the right,
      he is automatically brought back in on the left). Instead the rover is allowed
      to travel freely outside of the map, and we just model its movements in a grid
      that is bigger than the map to accommodate this
      
      We need to draw the rover's path on the given map. The given map's domain is 
      [0, num_columns] for x and [0, num_rows] for y. This may be a smaller area 
      than the area the rover explores, so we need to dynamically expand the grid 
      as the rover explores. A quick way to check the dimensions we will need for 
      our grid is to check the amount of Ms in the given rover's path, and use that
      amount for our grid in every direction, that way our rover's path can fully be 
      mapped in our path_i.txt file. We will call the amount of Ms in a path L.
      
      One thing to consider to better represent the path of the rover is to show it
      on the cartesian plane. To do this, we will initialize a 2D array, each being 
      2L + 1 in length. The reason for this is to firstly allow for L moves in each 
      direction (N, S, E, W) which is where 2L comes from. The added 1 allows for an
      extra index that allows us to insert - and | characters, which will act as the
      grid lines. 
      
      We also have to consider how we print the array to the file. If we were to 
      print the array in sequential order, row by row, we would have to have the 
      highest row (in terms of y values) at the first index of our array. To ensure
      that our array is output to the file correctly, we have to coordinate both of
      our structure for printing and arranging our grid. A simple structure that
      ensures coordination is having the lowest y-values of the cartesian plane be
      in the last row of the 2D array. This means that y = L will correspond to the
      row grid[0] and y = -L will correspond to the row grid[2L]. Here is a quick
      show of how they will correspond:
      
      grid[0]       : y = L             greatest y-value
      grid[1]       : y = L - 1
      grid[2]       : y = L - 2
      ...
      grid[L - 1]   : y = 0
      grid[L]       : will be used to map the x-axis like: ----------------
      grid[L+1]     : y = -1
      grid[L+2]     : y = -2
      ....
      grid[2L]      : y = -L            lowest y-value    
      
      
    '''
    directions = ['S', 'E', 'N', 'W']
    # move forward, dig
    moves = ['M', 'D']
    # loop through the given rover's moves
    for i in range(len(rover_moves)):
        # first test if we are turning left or right
        if True:
            print('true')

    return 0


def main():
    rover_path_url = "https://coe892.reev.dev/lab1/rover"
    num_rows, nums_columns, map1_contents = extract_map_into_array('../map1.txt')
    print(f'map1_contents:{map1_contents}')
    rover_moves = []
    # get paths of all rovers, store in an array
    for i in range(1, 11):
        rover_moves.append(extract_rover_path(rover_path_url, i))
    print(f'rover_moves:{rover_moves}')


if __name__ == '__main__':
    main()
    exit(0)
