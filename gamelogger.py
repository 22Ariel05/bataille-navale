import csv

class GameLogger:
    def __init__(self, filename):
        self.filename = filename

    def log_game(self, winner, is_with_ai, num_turns, game_data):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write header row
            writer.writerow(["Winner", "Played with AI", "Number of Turns"])
            writer.writerow([winner, is_with_ai, num_turns])
            # Write turn header
            writer.writerow(["Turn Number", "Player 1 Turn", "Player 2 Turn"])
            # Write turn data
            for turn, (player1_turn, player2_turn) in enumerate(game_data, start=1):
                writer.writerow(["Turn {}".format(turn), player1_turn, player2_turn])