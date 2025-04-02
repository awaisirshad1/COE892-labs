import copy
from enum import Enum


class RoverStatus(Enum):
    NOT_STARTED = "NOT STARTED"
    MOVING = "MOVING"
    ELIMINATED = "ELIMINATED"
    FINISHED = "FINISHED"


class Rover:
    def __init__(self, rover_id: int, moves: str):
        self.rover_id = rover_id
        self.moves = moves
        self.current_x = 0
        self.current_y = 0
        self.status = RoverStatus.NOT_STARTED

    def __str__(self):
        return (f"ID:{self.rover_id}, commands:{self.moves}, current position: "
                f"[{self.current_x},{self.current_y}], status:{self.status}")

