from functools import partial
import tkinter as tk
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from board import Board
from fleat import Fleat

class Board:
    def __init__(self):
        self.playzone = [[0 for _ in range(10)] for _ in range(10)]

class Fleat:
    def __init__(self):
        self.ships = {'Destroyer': 2, 'Submarine': 3, 'Cruiser': 3, 'Battleship': 4, 'Carrier': 5}
        self.placed_ships = {}


class TitleText(tk.Label):
    def __init__(self, master, t):
        super().__init__(master, text=t, bg="light blue", fg='black', font=('Times New Roman', 30, "bold"))

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg='light blue')
        self.title("Bataille Navale")
        self.geometry("1200x600")
        self.p1Board = Board()
        self.p2Board = Board()
        self.p1Fleat = Fleat()
        self.p2Fleat = Fleat()
        self.current_player = 1
        self.selected_ship = None
        self.ship_orientation = 'H'
        self.init_UI()

    def init_UI(self):
        self.clear_screen()
        self.create_ship_selection_area()
        self.create_orientation_selection_area()
        self.create_game_board_area()
        tk.Button(self, text="Start Player Vs Player", command=self.init_player_vs_player, bg='turquoise', width=20, height=2).pack(side=tk.TOP, pady=10)
        tk.Button(self, text="Leave the game", command=self.quit, bg='turquoise', width=20, height=2).pack(side=tk.TOP, pady=10)

    def create_ship_selection_area(self):
        self.ship_selection_frame = tk.Frame(self, bg='light blue')
        self.ship_selection_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        # Ajouter un espace en haut pour descendre les boutons
        spacer = tk.Frame(self.ship_selection_frame, height=200, bg='light blue')
        spacer.pack(side=tk.TOP, fill=tk.X)

    def create_orientation_selection_area(self):
        # Ce cadre contiendra les boutons d'orientation
        self.orientation_selection_frame = tk.Frame(self, bg='light blue')
        self.orientation_selection_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 0))  # Réduisez pady pour rapprocher les boutons de la grille


    def create_game_board_area(self):
        self.game_board_frame = tk.Frame(self, bg='light blue')
        # Ajouter un espace à gauche de la grille pour la décaler vers la droite
        self.game_board_frame.pack(side=tk.LEFT, padx=(50, 10))  # Le premier élément de padx est l'espace à gauche

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def select_ship(self, ship_name):
        self.selected_ship = ship_name
        print(f"Selected ship: {ship_name}")

    def set_orientation(self, orientation):
        self.ship_orientation = orientation
        print(f"Orientation set to: {orientation}")

    def init_player_vs_player(self):
        self.clear_screen()
        self.setup_preparation_phase()

    def setup_preparation_phase(self):
        self.clear_screen()
        self.create_ship_selection_area()
        self.create_orientation_selection_area()
        self.create_game_board_area()
        self.show_ship_selection()
        self.display_board()


    def show_ship_selection(self):
        for ship_name, length in self.p1Fleat.ships.items():
            if ship_name not in self.p1Fleat.placed_ships:
                button_cmd = partial(self.select_ship, ship_name)
                tk.Button(self.ship_selection_frame, text=f"Place {ship_name}", command=button_cmd, bg='sky blue', width=15, height=1).pack(pady=20)
        # Placez les boutons d'orientation en haut à droite
        tk.Button(self.orientation_selection_frame, text="Orientation Horizontal", command=lambda: self.set_orientation('H'), bg='sky blue', width=20, height=1).pack(side=tk.LEFT, padx=30)
        tk.Button(self.orientation_selection_frame, text="Orientation Vertical", command=lambda: self.set_orientation('V'), bg='sky blue', width=20, height=1).pack(side=tk.LEFT, padx=30)
        
    def display_board(self):
        # Créer un cadre pour la grille de jeu dans le cadre principal 'game_board_frame'
        self.board_frame = tk.Frame(self.game_board_frame, bg='navy')
        self.board_frame.pack(side=tk.TOP, pady=0)
        
        # Ajouter des labels pour les numéros de ligne sur le côté gauche de la grille
        for row in range(1, 11):
            label = tk.Label(self.board_frame, text=str(row), bg='navy', fg='white', width=2)
            label.grid(row=row, column=0, sticky="e")

        # Ajouter des labels pour les lettres de colonne en haut de la grille
        for col in range(1, 11):
            label = tk.Label(self.board_frame, text=chr(64 + col), bg='navy', fg='white', width=2)
            label.grid(row=0, column=col, sticky="n")
        
        # Générer la grille de jeu
        self.canvas_refs = {}  # Dictionnaire pour stocker les références des Canvas
        for i in range(1, 11):
            for j in range(1, 11):
                cell = tk.Canvas(self.board_frame, bg='white', width=40, height=40, highlightbackground="black")
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.bind("<Button-1>", lambda event, row=i-1, col=j-1: self.place_ship(row, col))  # Les indices commencent à 1 dans l'interface
                self.canvas_refs[(i-1, j-1)] = cell  # Stocker la référence avec les coordonnées comme clé


    def place_ship(self, row, col):
        if not self.selected_ship:
            print("No ship selected.")
            return
        fleet = self.p1Fleat if self.current_player == 1 else self.p2Fleat
        length = fleet.ships[self.selected_ship]
        if self.validate_placement(row, col, length):
            self.update_board(row, col, length)
            fleet.placed_ships[self.selected_ship] = (row, col, self.ship_orientation)
            self.selected_ship = None
            if len(fleet.placed_ships) == len(fleet.ships):
                self.switch_player()
        else:
            print("Invalid placement. Try again.")

    def validate_placement(self, row, col, length):
        fleet = self.p1Fleat if self.current_player == 1 else self.p2Fleat
        board = self.p1Board if self.current_player == 1 else self.p2Board

        if self.ship_orientation == 'H':
            if col + length > 10:
                return False
            for i in range(col, col + length):
                if board.playzone[row][i] != 0:
                    return False
        else:  # Orientation 'V'
            if row + length > 10:
                return False
            for i in range(row, row + length):
                if board.playzone[i][col] != 0:
                    return False
        
        return True

    def update_board(self, row, col, length):
        fleet = self.p1Fleat if self.current_player == 1 else self.p2Fleat
        board = self.p1Board if self.current_player == 1 else self.p2Board
        
        if self.ship_orientation == 'H':
            for i in range(col, col + length):
                board.playzone[row][i] = 1  # Assuming 1 represents a ship part
                self.draw_ship_part(row, i)
        else:  # Orientation 'V'
            for i in range(row, row + length):
                board.playzone[i][col] = 1  # Assuming 1 represents a ship part
                self.draw_ship_part(i, col)

    def draw_ship_part(self, row, col):
        # Utiliser le dictionnaire de références pour accéder directement au Canvas désiré
        cell = self.canvas_refs.get((row, col))
        if cell:
            cell.configure(bg='gray')
        else:
            print(f"Unable to find canvas at row {row}, column {col}.")

        
        if cell:
            cell.configure(bg='gray')
        else:
            print(f"Unable to find canvas at row {row}, column {col}.")

    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
            self.p1Fleat = Fleat()  # Reset for new game setup
            self.setup_preparation_phase()
        else:
            self.start_game()

    def start_game(self):
        # Transition to game phase
        print("Starting the game...")

    def quit_game(self):
        self.quit()

if __name__ == '__main__':
    app = Menu()
    app.mainloop()
