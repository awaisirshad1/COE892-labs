from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
import rover_utils as rvr
import os
from mine import Mine


class ExpansionRequest(BaseModel):
    x_param: int
    y_param: int


app = FastAPI()
# maps
map_original = os.path.dirname(os.path.abspath(__file__)) + "/map1.txt"
map_copy = os.path.dirname(os.path.abspath(__file__)) + "/map_copy.txt"
map_path = map_original

mines_original = os.path.dirname(os.path.abspath(__file__)) + "/mines.txt"
mines_copy = os.path.dirname(os.path.abspath(__file__)) + "/mines_copy.txt"
mines_path = mines_original

if os.path.exists(map_copy):
    os.remove(map_copy)

if os.path.exists(mines_copy):
    os.remove(mines_copy)

map_array = rvr.extract_map_into_array(map_original)
mine_serial_numbers = rvr.extract_mines_to_array(mines_path)
mines = rvr.assign_mines(map_array, mine_serial_numbers)


# Map operations
# get entire map
@app.get("/map")
def get_map_as_array():
    global map_array
    if map_array is None:
        map_array = rvr.extract_map_into_array(map_path)
    return {"map": f"{str(map_array)}"}


# expand map
@app.put("/map")
def expand_field(request: ExpansionRequest):
    global map_path, map_array, map_copy
    if not os.path.exists(map_copy):
        rvr.create_map_copy(map_copy)
    print("expanding map")
    rvr.expand_map_file(map_path, map_copy, request.x_param, request.y_param)
    map_path = map_copy
    map_array = rvr.extract_map_into_array(map_path)
    return {"map": [str(row) for row in map_array]}


# get all mines
@app.get("/mines")
def get_all_mines():
    global mines
    print(mines)
    return {"mines": [str(mine) for mine in mines]}


# get mine by id
@app.get("/mines/{mine_id}")
def get_mine_by_id(mine_id):
    global mines
    mine_int = int(mine_id)
    for mine in mines:
        if mine.id == mine_int:
            return {"mine:": str(mine)}
    return JSONResponse(content={"error": "mine with given id does not exist"}, status_code=status.HTTP_404_NOT_FOUND)


# delete mine by id
@app.delete("/mines/{mine_id}")
def delete_mine_by_id(mine_id):
    global mines
    mine_int = int(mine_id)
    for i in range(len(mines)):
        mine = mines[i]
        if mine.id == mine_int:
            print(f"deleting mine:{mine}...")
            map_array[mine.x][mine.y] = 0
            mines.pop(i)
            # TODO update map.txt file
            return {"mines": [str(mine) for mine in mines]}
    return JSONResponse(content={"error": "mine with given id does not exist"}, status_code=status.HTTP_404_NOT_FOUND)


# create mine
@app.post("/mines")
def create_mine(x, y, serial_num):
    x = int(x)
    y = int(y)
    if not (x < len(map_array) and y < len(map_array[0])):
        return JSONResponse(content={"error": "coordinates out of bounds, please expand map first"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    # to create a mine, the coordinates at which we wish to create the mine must not be occupied
    if map_array[x][y] == 1:
        return JSONResponse(content={"error": "mine already exists at those x and y coordinates, "
                                              "please use update instead"},
                            status_code=status.HTTP_409_CONFLICT)
    # to create a mine, the serial number must not exist, must not be assigned already
    if any(serial_num == mine.serial_num for mine in mines):
        return JSONResponse(content={"error": "mine already exists with that serial number"},
                            status_code=status.HTTP_409_CONFLICT)
    print("creating mine...")
    global map_path, map_copy, mines_path, mines_copy
    if serial_num in mine_serial_numbers:
        print("serial number exists but is not assigned, assigning...")
    else:
        mine_serial_numbers.append(serial_num)
    if not os.path.exists(mines_copy):
        with open(mines_copy, "w") as file:
            pass
        mines_path = mines_copy
    if not os.path.exists(map_copy):
        print(f"map copy doesnt exist, creating it...")
        rvr.create_map_copy(map_copy)
        map_path = map_copy
        print(f"map path after: {map_path}")

    new_id = len(mines) + 1
    mine = Mine(serial_num, x, y, new_id)
    mines.append(mine)
    map_array[x][y] = 1
    print(f"map_path:{map_path}")
    rvr.write_map_array_to_text_file(map_array, map_path)
    rvr.update_mines(mine_serial_numbers, mines_path)
    return {"successfully created mine": mine}


@app.put("/mines/{mine_id}")
def update_mine_by_id(mine_id):
    if mine_id > len(mines):
        return JSONResponse(content={"error": "mine with that ID does not exist"},
                            status_code=status.HTTP_404_NOT_FOUND)
    print("")

