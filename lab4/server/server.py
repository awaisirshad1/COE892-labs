from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
import rover_utils as rvr
import os
import copy
from mine import Mine
from rover import Rover


class ExpansionRequest(BaseModel):
    x_param: int
    y_param: int


class MineCreation(BaseModel):
    new_x: int
    new_y: int
    new_serial_num: str


class MineUpdate(BaseModel):
    new_x: Optional[int] = None
    new_y: Optional[int] = None
    new_serial_num: Optional[str] = None


class RoverCreationRequest(BaseModel):
    command_string: str


app = FastAPI()
rover_path_url = "https://coe892.reev.dev/lab1/rover"
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

rovers = rvr.extract_all_rovers_moves_to_map_with_ids(rover_path_url, 10)
next_rover_id = 11


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
    try:
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
        return JSONResponse(content={"error": "mine with given id does not exist"},
                            status_code=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return JSONResponse(content={"error": "please enter a numerical ID greater than 0"},
                            status_code=status.HTTP_400_BAD_REQUEST)


# create mine
@app.post("/mines")
def create_mine(request: MineCreation):
    x = int(request.x)
    y = int(request.y)
    if not (x < len(map_array) and y < len(map_array[0])):
        return JSONResponse(content={"error": "coordinates out of bounds, please expand map first"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    # to create a mine, the coordinates at which we wish to create the mine must not be occupied
    if map_array[x][y] == 1:
        return JSONResponse(content={"error": "mine already exists at those x and y coordinates, "
                                              "please use update instead"},
                            status_code=status.HTTP_409_CONFLICT)
    # to create a mine, the serial number must not exist, must not be assigned already
    if any(request.serial_num == mine.serial_num for mine in mines):
        return JSONResponse(content={"error": "mine already exists with that serial number"},
                            status_code=status.HTTP_409_CONFLICT)
    print("creating mine...")
    global map_path, map_copy, mines_path, mines_copy
    if request.serial_num in mine_serial_numbers:
        print("serial number exists but is not assigned, assigning...")
    else:
        mine_serial_numbers.append(request.serial_num)
    if not os.path.exists(mines_copy):
        mines_path = mines_copy
        rvr.create_txt_file(mines_path)
    if not os.path.exists(map_copy):
        rvr.create_txt_file(map_copy)
        map_path = map_copy
    new_id = len(mines) + 1
    mine = Mine(request.serial_num, x, y, new_id)
    mines.append(mine)
    map_array[x][y] = 1
    print(f"map_path:{map_path}")
    rvr.write_map_array_to_text_file(map_array, map_path)
    rvr.update_mines(mine_serial_numbers, mines_path)
    return {"successfully created mine": mine}


# update mine
@app.put("/mines/{mine_id}")
def update_mine_by_id(mine_id, request: MineUpdate):
    try:
        print(f"length:{len(mines)}")
        mine_id_int = int(mine_id)
        if mine_id_int <= 0:
            return JSONResponse(content={"error": "ID can't be 0 or negative numbers"},
                                status_code=status.HTTP_400_BAD_REQUEST)
        elif mine_id_int > len(mines):
            return JSONResponse(content={"error": "mine with that ID does not exist"},
                                status_code=status.HTTP_404_NOT_FOUND)
        if not (request.new_x or request.new_y or request.new_serial_num):
            return JSONResponse(content={"error": "no fields included to update, please include at least one field"},
                                status_code=status.HTTP_400_BAD_REQUEST)
        mine = None
        serial_number_taken = False
        mine_idx = -1
        for index, mine_curr in enumerate(mines):
            if mine_curr.id == mine_id_int:
                mine = mine_curr
                mine_idx = index
            if request.new_serial_num is not None:
                if mine_curr.serial_num == request.new_serial_num:
                    serial_number_taken = True
        if mine is None:
            return JSONResponse(content={"error": "could not find mine for given ID"},
                                status_code=status.HTTP_404_NOT_FOUND)
        if serial_number_taken and not mine.serial_num == request.new_serial_num:
            return JSONResponse(content={"error": "that serial number is already taken"},
                                status_code=status.HTTP_409_CONFLICT)
        new_mine = mine.copy()

        new_mine.x = mine.x if request.new_x is None else request.new_x
        new_mine.y = mine.y if request.new_y is None else request.new_y
        new_mine.serial_num = mine.serial_num if request.new_serial_num is None else request.new_serial_num
        print(f"updated mine:{new_mine}")
        global mines_path, mines_copy, map_path, map_copy
        if not os.path.exists(mines_copy):
            mines_path = mines_copy
            rvr.create_txt_file(mines_path)
        if not os.path.exists(map_copy):
            rvr.create_txt_file(map_copy)
            map_path = map_copy
        # update data structures
        map_array[mine.x][mine.y] = 0
        map_array[new_mine.x][new_mine.y] = 1
        if new_mine.serial_num not in mine_serial_numbers:
            mine_serial_numbers.append(new_mine.serial_num)
        # now replace the old mine

        mines[mine_idx] = new_mine
        # now update the txt files
        rvr.write_map_array_to_text_file(map_array, map_path)
        rvr.update_mines(mine_serial_numbers, mines_path)
        return {"updated mines": [str(curr) for curr in mines]}
    except ValueError:
        return JSONResponse(content={"error": "Please only enter numeric values for "
                                              "ID and coordinates, string value for serial number"})


# rover routes
@app.get("/rovers")
def get_all_rovers():
    return JSONResponse(content={"rovers": [str(rover) for rover in rovers.values()]},
                        status_code=status.HTTP_200_OK)


@app.get("/rovers/{rover_id}")
def get_rover_by_id(rover_id):
    rover_id_int = int(rover_id)
    try:
        if rover_id_int == 0:
            return JSONResponse(content={"error": "rover IDs only take on values of 1 or greater."},
                                status_code=status.HTTP_400_BAD_REQUEST)
        rover = rovers[rover_id_int]
        return JSONResponse(content={"rover": str(rover)},
                            status_code=status.HTTP_200_OK)
    except ValueError:
        return JSONResponse(content={"error": "please enter a numerical ID"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return JSONResponse(content={"error": "please enter an existing ID"},
                            status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/rovers")
def create_rover(request: RoverCreationRequest):
    global next_rover_id
    if request.command_string == "":
        return JSONResponse(content={"error": "rover moves can't be empty"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    allowed_chars = set("MDLRmdlr")
    rover_moves = None
    if all(c in allowed_chars for c in request.command_string):
        rover_moves = request.command_string.upper()
    else:
        return JSONResponse(content={"error": "The rover's movement contains invalid characters. "
                                              "Only M, D, L, R are allowed."},
                            status_code=status.HTTP_400_BAD_REQUEST)
    rover = Rover(next_rover_id, rover_moves)
    rovers[rover.rover_id] = rover
    next_rover_id += 1
    return JSONResponse(content={"rover": str(rover)},
                        status_code=status.HTTP_200_OK)


@app.delete("/rovers/{rover_id}")
def delete_rover_by_id(rover_id: int) -> JSONResponse:
    try:
        if rover_id not in rovers.keys():
            return JSONResponse(content={"error": "please enter an existing ID"},
                                status_code=status.HTTP_400_BAD_REQUEST)
        rover = rovers.pop(rover_id)
        return JSONResponse(content={"deleted rover": str(rover)},
                            status_code=status.HTTP_200_OK)
    except ValueError:
        return JSONResponse(content={"error": "please enter a numerical ID"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return JSONResponse(content={"error": "please enter an existing ID"},
                            status_code=status.HTTP_400_BAD_REQUEST)


# @app.put("/rovers/{rover_id}")
# def update_rover_by_id(request: )