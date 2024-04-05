from ship.ship import ShipOrientation, ShipType, Ship
from ship.case import Case, CaseState
import random


class Player:
    def __init__(self, id, match, game_instance):
        self.id = id
        self.match = match
        self.game = game_instance
        self.ship_orientation = ShipOrientation.HORIZONTAL
        self.ships = []
        self.cases = []
        self.selected_ship = None
        self.add_default_ships()
        self.add_default_cases()
        self.selected_ship = self.ships[0]


    def get_id(self):
        return self.id

    def get_game(self):
        return self.game

    def get_match(self):
        return self.match

    def get_ship_orientation(self):
        return self.ship_orientation

    def set_ship_orientation(self, orientation):
        self.ship_orientation = orientation

    def switch_ship_orientation(self):
        if self.ship_orientation == ShipOrientation.HORIZONTAL:
            self.ship_orientation = ShipOrientation.VERTICAL
        else:
            self.ship_orientation = ShipOrientation.HORIZONTAL

    def get_ships(self):
        return self.ships

    def get_selected_ship(self):
        return self.selected_ship

    def get_ship(self, x, y):
        for ship in self.ships:
            for case in ship.get_cases():
                if case.get_x() == x and case.get_y() == y:
                    return ship
        return None

    def add_ship(self, ship):
        self.ships.append(ship)

    def add_default_ships(self):
        for ship_type in ShipType:
            for i in range(ship_type.get_max_number()):
                ship = Ship(len(self.ships), ship_type)
                self.ships.append(ship)

    def add_default_cases(self):
        for x in range(10):
            for y in range(10):
                case = Case(self.match, x, y)
                self.cases.append(case)

    def get_case(self, x, y):
        for case in self.cases:
            if case.get_x() == x and case.get_y() == y:
                return case
        return None

    def get_case_with_ship_case(self, x, y):
        for ship in self.ships:
            for case in ship.get_cases():
                if case.get_x() == x and case.get_y() == y:
                    return case
        return None

    def all_ships_placed(self):
        for ship in self.ships:
            if not ship.is_placed():
                return False
        return True

    def all_ships_sunk(self):
        for ship in self.ships:
            if not ship.is_sunk():
                return False
        return True

    def attack(self, opponent, x, y):
        opponent_case = opponent.get_case(x, y)
        if opponent_case is None:
            print("Case is None")
            return False

        if opponent_case.get_state() != CaseState.EMPTY and opponent_case.get_state() != CaseState.SHIP:
            print("Case already hit or missed")
            return False

        if opponent_case.get_state() == CaseState.EMPTY:
            opponent_case.set_state(CaseState.MISS)
            print("Miss")
            return True

        opponent_case.set_state(CaseState.HIT)

        return True

    def place_ship(self, x, y):
        ship = self.selected_ship

        if ship is None:
            print("No ship selected")
            return False

        if ship.is_placed():
            print("Ship already placed")
            return False

        if self.ship_orientation == ShipOrientation.HORIZONTAL:
            for i in range(ship.get_length()):
                case = self.get_case(x + i, y)
                if case is None or case.get_state() != CaseState.EMPTY:
                    return False
            for i in range(ship.get_length()):
                case = self.get_case(x + i, y)
                case.set_state(CaseState.SHIP)
                ship.add_case(case)
        else:
            for i in range(ship.get_length()):
                case = self.get_case(x, y + i)
                if case is None or case.get_state() != CaseState.EMPTY:
                    return False
            for i in range(ship.get_length()):
                case = self.get_case(x, y + i)
                case.set_state(ship)
                ship.add_case(case)

        print(f"Ship {ship.get_name()} placed at {x}, {y}")

        self.selected_ship = self.get_random_ship_to_place()

        return True

    def get_random_ship_to_place(self):
        for ship in self.ships:
            if not ship.is_placed():
                return ship
        return None

    def select_ship(self, ship):
        self.selected_ship = ship


    def get_cases(self):
        return self.cases


class AIPlayer(Player):
    def __init__(self, id, match, game_instance):
        super().__init__(id, match, game_instance)
        self.place_random_ships()

    def get_id(self):
        return self.id

    def get_fleet(self):
        return self.fleet

    def get_ship_orientation(self):
        return self.ship_orientation

    def place_random_ships(self):
        while not self.all_ships_placed():
            for ship in self.ships:
                if not ship.is_placed():
                    x = random.randint(0, 10)
                    y = random.randint(0, 10)
                    orrientation = random.choice([ShipOrientation.HORIZONTAL, ShipOrientation.HORIZONTAL])
                    self.set_ship_orientation(orrientation)
                    self.place_ship(x, y)

    def attack(self, opponent, x, y):
        opponent_case = opponent.get_case(x, y)
        if opponent_case is None:
            print("Case is None")
            return False

        if opponent_case.get_state() != CaseState.EMPTY and opponent_case.get_state() != CaseState.SHIP:
            print("Case already hit or missed")
            return False

        if opponent_case.get_state() == CaseState.EMPTY:
            opponent_case.set_state(CaseState.MISS)
            print("Miss")
            return True

        opponent_case.set_state(CaseState.HIT)

        return True
    
    def selectShotMedium(self):
        if not self.previousShots:
            # If there are no previous shots, shoot randomly
            row, col = self.selectShotRandom()
            self.previousShots.append((row, col))
            return row, col
        else:
            # If there are previous shots, shoot around successful shots
            for shot in self.previousShots:
                row, col = shot
                # Check neighboring cells around successful shots
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        new_row, new_col = row + i, col + j
                        if (0 <= new_row < 10) and (0 <= new_col < 10) and (new_row, new_col) not in self.previousShots:
                            # Shoot at an untried neighboring cell
                            self.previousShots.append((new_row, new_col))
                            return new_row, new_col
        # If all neighboring cells have been shot, shoot randomly
        row, col = self.selectShotRandom()
        self.previousShots.append((row, col))
        return row, col
    
    def selectShotDensityBased(self):
        # Create a set to store all cells adjacent to shots that have already been taken
        adjacent_cells = set()
        for shot in self.previousShots:
            row, col = shot
            # Iterate over the adjacent cells of the current shot
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_row, new_col = row + i, col + j
                    # Check if the adjacent cell is within the bounds of the board
                    if (0 <= new_row < 10) and (0 <= new_col < 10):
                        adjacent_cells.add((new_row, new_col))

        # Calculate the density of ships around each cell
        density_map = {}
        for i in range(10):
            for j in range(10):
                if (i, j) not in self.previousShots:
                    density = 0
                    # Iterate over the adjacent cells of the current cell
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            new_row, new_col = i + k, j + l
                            # Check if the adjacent cell has been shot at
                            if (new_row, new_col) in adjacent_cells:
                                density += 1
                    density_map[(i, j)] = density
        
        # Sort cells based on decreasing density
        sorted_density_map = sorted(density_map.items(), key=lambda x: x[1], reverse=True)
        
        # Select the cell with the highest density that has not been shot before
        for shot, density in sorted_density_map:
            if shot not in self.previousShots:
                self.previousShots.append(shot)
                return shot
        # If all cells have been shot, shoot randomly
        return self.selectShotRandom()

    def set_ship_orientation(self, orientation):
        self.ship_orientation = orientation