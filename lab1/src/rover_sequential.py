import requests, json, time
# API to extract rover based on number
def extract_rover(url: str, num: int):

    res = requests.get(url+f'/{num}')
    if(res.status_code == 200):
        json_data = json.loads(res.text)
        # print(json_data)
        print(json_data['data']['moves'])

# API to calculate the path of the rover
def calculate_path(moves:str):
    return 0


def main():
     # = open('../map1.txt').read()


    map1_contents = [ int(i) for i in open('../map1.txt').read().split() if i.isnumeric()]
    num_rows, num_columns = map1_contents[0], map1_contents[1]
    print(f'num_rows:{num_rows}')
    print(f'map1_contents:{map1_contents}')
    extract_rover("https://coe892.reev.dev/lab1/rover",5)

if __name__ == '__main__':
    main()