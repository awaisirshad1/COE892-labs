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
    for i in range(num_rows-1, -1, -1):
        for j in range(num_columns):
            mine_map[i][j] = map_contents.pop(0)
    # return the 2D array
    return num_rows, num_columns, mine_map


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
      than the area the rover explores, so we need a grid larger than the map.

      A quick way to check the dimensions we will need for 
      our grid is to check the amount of Ms in the given rover's path, and use that
      amount for our grid in every direction, that way our rover's path can fully be 
      mapped in our path_i.txt file. We will call the amount of Ms in a path L.

      One thing to consider to better represent the path of the rover is to show it
      on the cartesian plane. To do this, we will initialize a 2D array, each 
      subarray being 2L in length. The reason for this is to firstly allow for L moves 
      in each direction (N, S, E, W) which is where 2L comes from. 

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
      grid[L - 1]   : y = 0         will be used to map the x-axis like: ----------------
      grid[L+1]     : y = -1
      grid[L+2]     : y = -2
      ....
      grid[2L - 1]  : y = -L            lowest y-value    

      Similarly, for every row in the array, the first L - 1 elements (from index 0 
      to L - 2) will be used to represent the negative x values, index L - 1 will 
      represent the y-axis through | characters (or a 1 where there is a mine), 
      and the remaining indices from L to 2L - 1 will represent the positive x values.
      The API create_grid accomplishes this task. 

      To allow for easy mapping of the path of the rover to the grid, we will change
      the initial current position (starts at (0,0) on cartesian plane) to the some
      values that correspond to our array's origin, which will be (L-1, L-1) in terms
      of indices of the grid array.  If we move forward facing east, increase the 
      second index by 1, west decreases by 1. If we move northward, we decrease the 
      first index by 1, southward increases by 1. This will make it easy for us to
      insert the movements of the rover into our 2D array. Digging does nothing to 
      change the index. 

      Upon encountering a 'move forward', we need to check the current_direction the 
      rover is facing to know how to change the indices of the grid. Based on it's 
      value, we can know how much to change the current_location variable by. To do
      this, we can have a hashmap that maps the change to the current direction it is
      facing. We can represent it as follows: 

      change_in_position = { 'N': (-1,0), 'S': (1,0), 'E': (0,1), 'W': (0,-1) }

      By adding the value of each key-value pair to the current_position variable, 
      we get the new position of the rover in terms of indices of the grid array. It
      allows for quick changing of the contents of the grid array. 

    '''


# API to create cartesian plane grid with map contents
def create_grid(rover_moves: str, mine_map: list):
    # first count how many Ms we have in a rover's moves, the value of L
    L = rover_moves.count('M')
    print(f'printing L:{L}')
    # now create a 2D array that is 2L by 2L, all initialized to 0, except
    # for the contents of the map we are given and the x and y axes
    # if the location of a mine coincides with any of the x or y axes,
    # then replace the - or | with 1. The origin will be (L-1, L-1)
    origin = [L - 1, L - 1]
    # creating the array
    # grid = [[]]
    grid = [[None for j in range(2*L+1)] for i in range(2*L+1)]
    # print(f'printing grid[0][0]:{grid[0][0]}')
    # print(f'printing grid size:{len(grid[0])}')
    print(f'L - len(minemap) = {L - len(mine_map)}')
    print(f'len(minemap):{len(mine_map)}')
    # i indicates y coordinate, j indicates x coordinate
    for i in range((2*L)+1):
        for j in range((2*L)+1):
            if (i > (L - len(mine_map))) and (i <= L):
                if(j >= L) and (j < (L + len(mine_map[0]))):
                    grid[i][j] = mine_map[L-i][L+j]
            # if j is along y-axis (x=0 corresponds to j=L)
            elif j == L:
                grid[i][j] = '|'
            # if the next condition executes, j is not along the y-axis, now
            # check the x-axis (y=0 corresponds to i=L)
            elif i == L:
                grid[i][j] = '-'
            # if neither of the other 2 conditions are true, fill the current
            # element with a 0
            else:
                grid[i][j] = '0'
    return grid
    # return 0


# API to draw the path of the rover on path_i.txt file
def draw_path(rover_moves: str, rover_num: int, mine_map: list):
    # starting off by facing south
    current_direction = 0
    current_action = 0
    current_position = [0,0]
    grid = create_grid(rover_moves, mine_map)

    directions = ['S', 'E', 'N', 'W']
    # move forward, dig
    moves = ['M', 'D']
    # loop through the given rover's moves
    # for i in range(len(rover_moves)):
    #     # first test if we are turning left or right
    #     if True:
    #         print('true')
    with open(f'../sequential/path_{rover_num}.txt', 'w') as f:
        for r_row in grid:
            f.write("".join(r_row)+"\n")
    return 0


def main():
    rover_path_url = "https://coe892.reev.dev/lab1/rover"
    num_rows, nums_columns, map1_contents = extract_map_into_array('../map1.txt')
    print(f'map1_contents:{map1_contents}')
    rover_moves = []
    # get paths of all rovers, store in an array
    for i in range(1, 11):
        rover_moves.append(extract_rover_path(rover_path_url, i))
    # print(f'rover_moves:{rover_moves}')

    draw_path(rover_moves[0], 1, map1_contents)


if __name__ == '__main__':
    main()
    exit(0)
