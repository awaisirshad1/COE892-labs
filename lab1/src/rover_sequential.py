import requests, json, time

# API to extract rover based on number
def extract_rover_path(url: str, num: int):
    res = requests.get(url+f'/{num}')
    if(res.status_code == 200):
        json_data = json.loads(res.text)
        # print(json_data['data']['moves'])
        return json_data['data']['moves']

# API to extract map into a 2D array
def extract_map(path:str):
    # read all integers in the map file
    map_contents = [int(i) for i in open(path).read().split() if i.isnumeric()]
    # first integer is number of rows, second integer is number of columns
    num_rows, num_columns = map_contents[0], map_contents[1]
    # after we've assigned these to variables, pop them off the array
    map_contents.pop(0)
    map_contents.pop(0)
    # Now we can take the remaining numbers (which should all be 1s and 0s) and assign them to a 2D array based on numbers of rows and columns
    map = [[None for j in range(num_columns)] for i in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_columns):
            map[i][j] = map_contents.pop(0)
    # return the 2D array
    return map

# API to calculate the path of the rover
def create_path(moves:str, rover_num:int):
    return 0


def main():
    map1_contents = extract_map('../map1.txt')
    print(f'map1_contents:{map1_contents}')
    rover_path = extract_rover_path("https://coe892.reev.dev/lab1/rover",5)
    print(f'rover_path:{rover_path}')


if __name__ == '__main__':
    main()
    exit(0)