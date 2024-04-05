from enum import Enum
from ship.case import CaseState


class Ship:

    def __init__(self, id, name, length):
        self.id = id
        self.name = name
        self.length = length
        self.cases = []

    def __init__(self, id, ship_type):
        self.id = id
        self.name = ship_type.get_display_name()
        self.length = ship_type.get_length()
        self.cases = []

    def get_id(self):
        return self.id

    def get_length(self):
        return self.length

    def get_name(self):
        return self.name

    def is_sunk(self):

        if len(self.cases) == 0:
            return False

        for case in self.cases:
            if case.get_state() != CaseState.HIT:
                return False
        return True

    def is_placed(self):
        return len(self.cases) == self.length

    def get_cases(self):
        return self.cases

    def get_case(self, x, y):
        for case in self.cases:
            if case.get_x() == x and case.get_y() == y:
                return case
        return None

    def add_case(self, case):
        self.cases.append(case)

    def get_color(self):
        if self.is_sunk():
            return CaseState.HIT.get_color()

        return CaseState.SHIP.get_color()

    def show_info(self):
        print(f"Ship length: {self.length}, is sunk: {self.is_sunk()}, is placed: {self.is_placed()}")


class ShipOrientation(Enum):
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"

    def __init__(self, display_name):
        self.display_name = display_name

    def get_display_name(self):
        return self.display_name


class ShipType(Enum):
    CARRIER = ("Carrier", 5, 1)
    CRUISER = ("Cruiser", 4, 1)
    SUBMARINE = ("Submarine", 2, 2)
    DESTROYER = ("Destroyer", 3, 2)

    def __init__(self, display_name, length, max_number):
        self.display_name = display_name
        self.length = length
        self.max_number = max_number

    def get_display_name(self):
        return self.display_name

    def get_length(self):
        return self.length

    def get_max_number(self):
        return self.max_number

