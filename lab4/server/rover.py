import copy
from enum import Enum
import threading


class RoverStatus(Enum):
    NOT_STARTED = "NOT STARTED"
    MOVING = "MOVING"
    ELIMINATED = "ELIMINATED"
    FINISHED = "FINISHED"

    def __str__(self):
        return self.value


class Rover:
    def __init__(self, rover_id: int, moves: str):
        self.rover_id = rover_id
        self.moves = moves
        self.current_x = 0
        self.current_y = 0
        self.current_direction = 0
        self.status = RoverStatus.NOT_STARTED
        self.executed_commands = ""
        self.remaining_commands = self.moves
        self.terminate_rover_event = threading.Event()
        self.pause_rover_thread_event = threading.Event()
        self.mines_defused = {}

    def __str__(self):
        return (f"ID:{self.rover_id}, commands:{self.moves}, current position: "
                f"[{self.current_x},{self.current_y}], status:{self.status}")

    def extended_str(self):
        return (f"ID:{self.rover_id}, commands executed:{self.executed_commands}, current position: "
                f"[{self.current_x},{self.current_y}], status:{self.status}, remaining commands:{self.remaining_commands}, mines defused:{self.mines_defused}")

    def update_command_string(self, additional_commands: str):
        if self.status == RoverStatus.NOT_STARTED:
            self.moves += additional_commands
            self.remaining_commands = self.moves
        else:
            self.remaining_commands += additional_commands

    def terminate_rover_thread(self):
        self.terminate_rover_event.set()

