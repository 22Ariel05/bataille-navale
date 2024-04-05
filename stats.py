import pandas as pd
import matplotlib.pyplot as plt

class GameStatistics:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        return pd.read_csv(self.filename)
    
    def calculate_stats(self):
        data = self.load_data()

        # Calculate the number of successful shots per turn
        successful_shots_per_turn = []
        for _, row in data.iterrows():
            player1_turns = row['Player 1 Turn'].split('|')
            player2_turns = row['Player 2 Turn'].split('|')
            num_turns = max(len(player1_turns), len(player2_turns))
            successful_shots = [1 if 'Hit' in player1_turns[i] else 0 for i in range(num_turns)]
            successful_shots += [1 if 'Hit' in player2_turns[i] else 0 for i in range(num_turns)]
            successful_shots_per_turn.extend(successful_shots)

        # Plot a bar chart for successful shots per turn
        plt.figure(figsize=(10, 6))
        plt.bar(range(1, len(successful_shots_per_turn) + 1), successful_shots_per_turn, color='skyblue')
        plt.title('Number of Successful Shots per Turn')
        plt.xlabel('Turn')
        plt.ylabel('Number of Successful Shots')
        plt.grid(axis='y')
        plt.show()