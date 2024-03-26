from functools import partial
from fleet import Fleet
import tkinter as tk
import sys
import os

# Assurez-vous que le chemin d'accès est correct pour importer Board
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from board import Board

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
        self.p1Fleet = Fleet()
        self.p2Fleet = Fleet()
        self.current_player = 1
        self.selected_ship = None
        self.ship_orientation = 'H'
        self.current_phase = "setup"
        self.init_UI()

    def init_UI(self):
        self.clear_screen()
        self.create_ship_selection_area()
        self.create_orientation_selection_area()
        self.create_game_board_area()
        tk.Button(self, text="Start Player Vs Player", command=self.init_player_vs_player, bg='turquoise', width=20, height=2).pack(side=tk.TOP, pady=10)
        tk.Button(self, text="Leave the game", command=self.quit, bg='turquoise', width=20, height=2).pack(side=tk.TOP, pady=10)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_ship_selection_area(self):
        self.ship_selection_frame = tk.Frame(self, bg='light blue')
        self.ship_selection_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        spacer = tk.Frame(self.ship_selection_frame, height=200, bg='light blue')
        spacer.pack(side=tk.TOP, fill=tk.X)

    def create_orientation_selection_area(self):
        self.orientation_selection_frame = tk.Frame(self, bg='light blue')
        self.orientation_selection_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 0))
        if self.current_phase == "setup":
            horizontal_button = tk.Button(self.orientation_selection_frame, text="Horizontal", command=lambda: self.set_orientation('H'), bg='sky blue', width=15, height=1)
            horizontal_button.pack(side=tk.LEFT, padx=10)
            vertical_button = tk.Button(self.orientation_selection_frame, text="Vertical", command=lambda: self.set_orientation('V'), bg='sky blue', width=15, height=1)
            vertical_button.pack(side=tk.LEFT, padx=10)
            self.orientation_buttons = [horizontal_button, vertical_button]
        else:
            self.orientation_buttons = []

    def create_game_board_area(self):
        self.game_board_frame = tk.Frame(self, bg='light blue')
        self.game_board_frame.pack(side=tk.LEFT, padx=(50, 10))

    def select_ship(self, ship_name):
        self.selected_ship = ship_name
        print(f"Selected ship: {ship_name}")

    def set_orientation(self, orientation):
        self.ship_orientation = orientation
        print(f"Orientation set to: {orientation}")

    def init_player_vs_player(self):
        self.current_phase = "setup"
        self.setup_preparation_phase()

    def setup_preparation_phase(self):
        self.clear_screen()
        self.create_ship_selection_area()
        self.show_ship_selection()
        self.create_game_board_area()
        self.create_orientation_selection_area()
        self.display_board()

    def show_ship_selection(self):
        for ship_name in ['airCarrier', 'cruiser', 'destroyer1', 'destroyer2', 'submarine1', 'submarine2']:
            if getattr(self.p1Fleet if self.current_player == 1 else self.p2Fleet, ship_name).is_placed() == False:
                button_cmd = partial(self.select_ship, ship_name)
                tk.Button(self.ship_selection_frame, text=f"Place {ship_name}", command=button_cmd, bg='sky blue', width=15, height=1).pack(pady=20)

    def display_board(self):
        # Supprime le contenu précédent du cadre du plateau de jeu s'il existe
        for widget in self.game_board_frame.winfo_children():
            widget.destroy()

        # Création d'un nouveau cadre pour le plateau dans le cadre principal 'game_board_frame'
        self.board_frame = tk.Frame(self.game_board_frame, bg='navy')
        self.board_frame.pack(side=tk.TOP, pady=0)

        # Ajout des labels pour les numéros de ligne sur le côté gauche de la grille
        for row in range(1, 11):
            label = tk.Label(self.board_frame, text=str(row), bg='navy', fg='white', width=2)
            label.grid(row=row, column=0, sticky="e")

        # Ajout des labels pour les lettres de colonne en haut de la grille
        for col in range(1, 11):
            label = tk.Label(self.board_frame, text=chr(64 + col), bg='navy', fg='white', width=2)
            label.grid(row=0, column=col, sticky="n")
        
        # Initialisation du dictionnaire pour stocker les références des Canvas (cases du jeu)
        self.canvas_refs = {}

        # Génération de la grille de jeu avec un Canvas pour chaque cellule
        for i in range(10):
            for j in range(10):
                cell = tk.Canvas(self.board_frame, bg='white', width=40, height=40, highlightbackground="black")
                cell.grid(row=i+1, column=j+1, padx=1, pady=1)  # +1 pour compenser les labels de ligne/colonne
                cell.bind("<Button-1>", lambda event, row=i, col=j: self.place_ship(row, col))
                self.canvas_refs[(i, j)] = cell

    def place_ship(self, row, col):
        if not self.selected_ship:
            print("No ship selected.")
            return

        fleet = self.p1Fleet if self.current_player == 1 else self.p2Fleet
        ship = getattr(fleet, self.selected_ship, None)
        if not ship or ship.is_placed():
            print("Ship not available or already placed.")
            return

        rotate = self.ship_orientation == 'V'  # True si 'V', sinon False
        board = self.p1Board if self.current_player == 1 else self.p2Board

        if board.isValidPlacement((row, col), rotate, ship):
            if rotate:  # Placement vertical
                for i in range(ship.get_length()):
                    self.draw_ship_part(row + i, col)
                    board.playzone[row + i][col] = 1  # Marquez la case comme occupée
            else:  # Placement horizontal
                for i in range(ship.get_length()):
                    self.draw_ship_part(row, col + i)
                    board.playzone[row][col + i] = 1  # Marquez la case comme occupée

            ship.set_placed(True)
            print(f"{self.selected_ship} placed.")
        else:
            print("Invalid placement. Try again.")

    def draw_ship_part(self, row, col):
        cell = self.canvas_refs.get((row, col))
        if cell:
            cell.configure(bg='gray')
        else:
            print(f"Unable to find canvas at row {row}, column {col}.")

    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
            self.p1Fleet = Fleet()  # Réinitialisation de la flotte pour le nouveau joueur
        else:
            self.current_player = 1
            self.p2Fleet = Fleet()  # Réinitialisation de la flotte pour le joueur 2
        self.setup_preparation_phase()

    def start_game(self):
        self.current_phase = "game"
        print("Game started. Player 1 begins.")

    def quit_game(self):
        self.quit()

if __name__ == '__main__':
    app = Menu()
    app.mainloop()