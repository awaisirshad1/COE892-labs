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