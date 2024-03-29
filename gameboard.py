from functools import partial
from fleet import Fleet
from board import Board
from ship import Ship
import tkinter as tk
import sys
import os

# Assurez-vous que le chemin d'accès est correct pour importer Board
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


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
        self.current_mode = 'placing'
        self.currentPlayerText = tk.StringVar()  # Ajouté pour gérer l'affichage du joueur actuel
        self.init_UI()



    def init_UI(self):
        self.clear_screen()
        # Ne créez pas les boutons d'orientation ici
        self.create_ship_selection_area()  # Cela peut rester si vous voulez initialement cacher cette zone aussi
        self.create_game_board_area()
        currentPlayerLabel = tk.Label(self, textvariable=self.currentPlayerText, font=('Times New Roman', 20), bg='light blue')
        currentPlayerLabel.pack(side=tk.TOP, pady=10)
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
        # Création du label pour afficher le joueur actuel uniquement pendant cette phase
        currentPlayerLabel = tk.Label(self, textvariable=self.currentPlayerText, font=('Times New Roman', 20), bg='light blue')
        currentPlayerLabel.pack(side=tk.TOP, pady=10)
        # Mise à jour du texte en fonction du joueur actuel
        if self.current_player == 1:
            self.currentPlayerText.set("Joueur 1 joue")
        else:
            self.currentPlayerText.set("Joueur 2 joue")
        # Continuation de la méthode avec la création de la zone de sélection des navires, etc.
        self.create_ship_selection_area()
        self.create_orientation_selection_area() 
        self.create_game_board_area()
        self.show_ship_selection()
        self.display_board()
        # Ajout du bouton "Retirer"
        tk.Button(self, text="Retirer", command=self.remove_ship, bg='red', width=15, height=2).pack(side=tk.TOP, pady=10)
        tk.Button(self, text="Prêt", command=self.finalize_preparation, bg='green', width=10, height=2).pack(side=tk.BOTTOM, pady=20)
        
    def finalize_preparation(self):
        # Vérification si le joueur actuel est le joueur 1
        if self.current_player == 1:
            # Vérification si tous les navires du joueur 1 sont placés
            if self.p1Fleet.all_ships_placed():
                self.current_player = 2  # Passer au joueur 2
                self.setup_preparation_phase()  # Réinitialiser la phase de préparation pour le joueur 2
            else:
                print("Tous les navires doivent être placés.")
        else:
            # Pour le joueur 2, vérifier si tous ses navires sont placés
            if self.p2Fleet.all_ships_placed():
                self.start_game()  # Tous les navires sont placés, démarrer le jeu
            else:
                print("Tous les navires doivent être placés.")

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

        rotate = self.ship_orientation == 'V'
        board = self.p1Board if self.current_player == 1 else self.p2Board

        if board.isValidPlacement((row, col), rotate, ship):
            list_of_coords = []
            if rotate:
                for i in range(ship.get_length()):
                    self.draw_ship_part(row + i, col, "gray")
                    board.playzone[row + i][col] = 1
                    list_of_coords.append((row + i, col))
            else:
                for i in range(ship.get_length()):
                    self.draw_ship_part(row, col + i, "gray")
                    board.playzone[row][col + i] = 1
                    list_of_coords.append((row, col + i))

            ship.set_placed(True)
            ship.when_placed(list_of_coords)
            print(f"{self.selected_ship} placed.")
        else:
            print("Invalid placement. Try again.")


    def remove_ship_from_grid(self, row, col):
        if not self.selected_ship:
            print("Veuillez sélectionner un navire à retirer.")
            return

        fleet = self.p1Fleet if self.current_player == 1 else self.p2Fleet
        ship = getattr(fleet, self.selected_ship, None)

        if ship and ship.is_placed():
            for node in ship.ship_nodes:
                x, y = node.get_coords()
                # Réinitialisation de la case de manière conditionnelle
                if self.current_player == 1:
                    self.p1Board.playzone[x][y] = 0
                else:
                    self.p2Board.playzone[x][y] = 0
                # Effacer visuellement la case sur la grille
                self.draw_ship_part(x, y, "white")

            ship.set_placed(False)
            ship.ship_nodes = []
            print(f"Navire {self.selected_ship} retiré avec succès.")
        else:
            print("Le navire sélectionné n'est pas placé ou n'existe pas.")


    def remove_ship(self):
        if not self.selected_ship:
            print("Aucun navire sélectionné pour être retiré.")
            return

        fleet = self.p1Fleet if self.current_player == 1 else self.p2Fleet
        ship = getattr(fleet, self.selected_ship, None)

        if ship and ship.is_placed():
            for node in ship.ship_nodes:
                x, y = node.get_coords()
                if self.current_player == 1:
                    self.p1Board.playzone[x][y] = 0
                else:
                    self.p2Board.playzone[x][y] = 0
                self.draw_ship_part(x, y, "white")

            ship.set_placed(False)
            ship.ship_nodes = []
            print(f"Navire {self.selected_ship} retiré.")
            self.selected_ship = None  # Réinitialiser le navire sélectionné
        else:
            print("Le navire sélectionné n'est pas placé ou n'existe pas.")

    def clear_ship_from_grid(self, ship):
        # Identifier les cases occupées par le navire dans self.playzone
        board = self.p1Board if self.current_player == 1 else self.p2Board
        ship_id = ship.ship_id  # Supposons que chaque navire a un attribut ship_id unique

        for row in range(10):
            for col in range(10):
                if board.playzone[row][col] == ship_id:  # Vérifie si la case appartient au navire
                    board.playzone[row][col] = 0  # Réinitialise la case
                    self.draw_ship_part(row, col, "white")  # Réinitialise visuellement la case

        # Vous pourriez vouloir réinitialiser l'état du navire ici
        ship.set_placed(False)

    def draw_ship_part(self, row, col, color="gray"):
        cell = self.canvas_refs.get((row, col))
        if cell:
            cell.configure(bg=color)
        else:
            print(f"Unable to find canvas at row {row}, column {col}.")

    def identify_and_remove_ship(self, row, col):
        board = self.p1Board if self.current_player == 1 else self.p2Board
        if board.playzone[row][col] > 0:  # Supposons qu'un ID unique > 0 indique un navire
            ship_id = board.playzone[row][col]
            # Effacer le navire de la grille et de la visualisation
            for r in range(10):
                for c in range(10):
                    if board.playzone[r][c] == ship_id:
                        board.playzone[r][c] = 0
                        self.draw_ship_part(r, c, "white")  # Réinitialiser la couleur de la case
                        
            # Trouver et marquer le navire correspondant comme non placé
            for ship_name in ['airCarrier', 'cruiser', 'destroyer1', 'destroyer2', 'submarine1', 'submarine2']:
                ship = getattr(self.p1Fleet if self.current_player == 1 else self.p2Fleet, ship_name)
                if ship_id == ship.ship_id:  # Si l'ID correspond, marquez comme non placé
                    ship.set_placed(False)
                    print(f"{ship_name} retiré de la grille.")
                    break
        else:
            print("Aucun navire à cet emplacement.")

    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
            self.currentPlayerText.set("Joueur 2 joue")
            self.p1Fleet = Fleet()  # Réinitialisation de la flotte pour le nouveau joueur
        else:
            self.current_player = 1
            self.currentPlayerText.set("Joueur 1 joue")
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