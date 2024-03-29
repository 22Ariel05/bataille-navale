import random

class Ai:
    
    def __init__(self):
        self.previousShots = []

    def InitializeAiBoard(self, board, fleet):
        self.placeFleet(board, fleet)

    def placeFleet(self, board, fleet):
        ships = [fleet.airCarry, fleet.cruser, fleet.destroy1, fleet.destroy2, fleet.sub1, fleet.sub2]
        for ship in ships:
            valid_placement = False
            while not valid_placement:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                rotate = random.choice([True, False])
                if board.isValidPlacement((row, col), rotate, ship):
                    board.placeShip((row, col), rotate, ship)
                    valid_placement = True

    def selectShotRandom(self):
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if (row, col) not in self.previousShots:
                self.previousShots.append((row, col))
                return (row, col)
            
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