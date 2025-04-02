import copy
class Mine:
    def __init__(self, serial_num, x, y, id):
        self.serial_num = serial_num
        self.x = x
        self.y = y
        self.id = id

    def __str__(self):
        return f"ID:{self.id}, serial_num:{self.serial_num}, coords:[{self.x},{self.y}]"

    def copy(self):
        return copy.copy(self)
