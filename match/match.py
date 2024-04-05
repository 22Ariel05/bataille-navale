from enum import Enum
import tkinter as tk
from player.player import Player, AIPlayer
import time
from color import Color
from ship.case import CaseState
import random

class Match:

    def __init__(self, id, name, game_instance):
        self.id = id
        self.name = name
        self.game = game_instance
        self.state = MatchState.PREPARATION
        self.board = MatchBoard(game_instance, self)
        self.info = MatchInfo(game_instance, self)

    def __init__(self, type, game_instance):
        self.id = type.get_id()
        self.name = type.get_display_name()
        self.game = game_instance
        self.state = MatchState.PREPARATION
        self.board = MatchBoard(game_instance, self)
        self.info = MatchInfo(game_instance, self)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_game(self):
        return self.game

    def get_board(self):
        return self.board

    def get_info(self):
        return self.info

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def refresh(self):
        for widget in self.game.winfo_children():
            widget.destroy()

        self.board.create_board()
        self.info.create_info()

    def start_game(self):
        self.refresh()

    def switch_player(self):
        pass


class MatchState(Enum):
    PREPARATION = "Préparation"
    BATTLE = "Bataille"
    FINISH = "Partie terminée"

    def __init__(self, display_name):
        self.display_name = display_name

    def get_display_name(self):
        return self.display_name


class MatchPlayerVsPlayer(Match):

    def __init__(self, game_instance):
        super().__init__(MatchType.PLAYER_VS_PLAYER, game_instance)
        self.player1 = Player(1, self, game_instance)
        self.player2 = Player(2, self, game_instance)
        self.current_player = self.player1

    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

    def get_current_player(self):
        return self.current_player

    def get_cases(self):
        return self.current_player.get_cases()

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def get_other_player_of_player(self, player):
        return self.player2 if player == self.player1 else self.player1

    def get_opponent(self):
        return self.player2 if self.current_player == self.player1 else self.player1

    def start_game(self):
        self.refresh()

    def all_ships_of_players_placed(self):
        return self.player1.all_ships_placed() and self.player2.all_ships_placed()

    def get_player_all_ships_sunk(self):
        if self.get_opponent().all_ships_sunk():
            return self.get_opponent()

    def start(self):
        self.set_state(MatchState.BATTLE)
        self.refresh()


class MatchPlayerVsAI(Match):

    def __init__(self, game_instance):
        super().__init__(MatchType.PLAYER_VS_AI, game_instance)
        self.player = Player(1, self, game_instance)
        self.ai = AIPlayer(2, self, game_instance)

    def get_player(self):
        return self.player

    def get_ai(self):
        return self.ai

    def get_current_player(self):
        return self.player

    def get_other_player_of_player(self, player):
        return self.ai if player == self.player else self.player

    def all_ships_of_players_placed(self):
        return self.player.all_ships_placed()

    def get_player_all_ships_sunk(self):
        if self.ai.all_ships_sunk():
            return self.ai
        elif self.player.all_ships_sunk():
            return self.player

    def get_opponent(self):
        return self.ai

    def start(self):
        self.set_state(MatchState.BATTLE)
        self.refresh()

    def switch_player(self):
        x = random.randint(0, 10)
        y = random.randint(0, 10)

        if not self.ai.attack(self.player, x, y):
            self.switch_player()
        else:
            self.refresh()



class MatchType(Enum):
    PLAYER_VS_PLAYER = ("Player Vs Player", 1)
    PLAYER_VS_AI = ("Player Vs AI", 2)

    def __init__(self, display_name, id):
        self.display_name = display_name
        self.id = id

    def get_id(self):
        return self.id

    def get_display_name(self):
        return self.display_name

    def get_match(self, game_instance):
        if self == MatchType.PLAYER_VS_PLAYER:
            return MatchPlayerVsPlayer(game_instance)
        elif self == MatchType.PLAYER_VS_AI:
            return MatchPlayerVsAI(game_instance)
        else:
            return None


class MatchBoard(tk.Frame):
    def __init__(self, game_instance, match):
        super().__init__(game_instance, bg='light blue')
        self.match = match
        self.game = game_instance
        self.pack(side=tk.TOP, padx=50)

    def get_game(self):
        return self.game

    def create_board(self):
        self.game.clear()

        if self.match.get_state() == MatchState.FINISH:
            player = self.match.get_player_all_ships_sunk()
            label = tk.Label(self.game, text=f"Joueur {player.get_id()} a perdu", bg='light blue', fg='black',
                             font=('Times New Roman', 20))
            label.pack()
            return

        if self.match.get_state() == MatchState.BATTLE:
            self.create_view()

        self.create_game()

    def create_game(self):
        current_player = self.match.get_current_player()

        column_frame = tk.Frame(self.game, bg='light blue')
        column_frame.pack()
        for col in range(1, 11):
            label = tk.Label(column_frame, text=chr(64 + col), bg='navy', fg='white', width=4, padx=7)
            label.pack(side=tk.LEFT)

        for row in range(1, 11):
            row_frame = tk.Frame(self.game, bg='light blue')
            row_frame.pack()

            row_label = tk.Label(row_frame, text=str(row), bg='navy', fg='white', width=7)
            row_label.pack(side=tk.LEFT)

            for col in range(1, 11):
                case = current_player.get_case(row - 1, col - 1)
                if case is not None:
                    state = case.get_state()
                    color = Color.WHITE

                    if state == CaseState.SHIP or state == CaseState.HIT:
                        color = Color.GREEN
    

                    button = tk.Button(row_frame, bg=color.value, highlightbackground="black", width=5)
                    button.pack(side=tk.LEFT)
                    button.bind("<Button-1>", lambda event, x=case.get_x(), y=case.get_y(): self.handle_button(x, y))
                else:
                    print("Case is None")

    def create_view(self):
        current_player = self.match.get_current_player()

        column_frame = tk.Frame(self.game, bg='light gray')
        column_frame.pack()
        for col in range(1, 11):
            label = tk.Label(column_frame, text=chr(64 + col), bg='navy', fg='white', width=4, padx=7)
            label.pack(side=tk.LEFT)

        for row in range(1, 11):
            row_frame = tk.Frame(self.game, bg='light gray')
            row_frame.pack()

            row_label = tk.Label(row_frame, text=str(row), bg='navy', fg='white', width=7)
            row_label.pack(side=tk.LEFT)

            for col in range(1, 11):
                case = self.match.get_other_player_of_player(self.match.get_current_player()).get_case(row - 1, col - 1)
                if case is not None:
                    state = case.get_state()
                    color = Color.WHITE

                    if(state == CaseState.HIT):
                        color = Color.RED
                    elif(state == CaseState.MISS):
                        color = Color.BLUE

                    button = tk.Button(row_frame, bg=color.value, highlightbackground="black", width=5)
                    button.pack(side=tk.LEFT)
                else:
                    print("Case is None")

    def handle_button(self, x, y):

        if self.match.get_state() == MatchState.PREPARATION:
            self.match.get_current_player().place_ship(x, y)
            self.match.refresh()
        elif self.match.get_state() == MatchState.BATTLE:
            attack = self.match.get_current_player().attack(self.match.get_opponent(), x, y)

            if attack:
                if self.match.get_player_all_ships_sunk() is not None:
                    self.match.set_state(MatchState.FINISH)
                else:
                    self.match.switch_player()
                self.match.refresh()

            else:
                self.match.refresh()


class MatchInfo(tk.Frame):

    def __init__(self, game_instance, match):
        super().__init__(game_instance, bg='light blue')
        self.match = match
        self.game = game_instance
        self.pack(side=tk.RIGHT, padx=50)

    def create_info(self):

        if self.match.get_state() == MatchState.FINISH:
            player = self.match.get_other_player_of_player(self.match.get_player_all_ships_sunk())
            label = tk.Label(self.game, text=f"Joueur {player.get_id()} a Gagné", bg='light blue', fg='black',
                             font=('Times New Roman', 20))
            label.pack()

            return

        if self.match.get_state() == MatchState.BATTLE:
            self.button = tk.Button(self.game, text="Passer", bg='light blue', fg='black', font=('Times New Roman', 20))
            self.button.pack(side=tk.BOTTOM)
            self.button.bind("<Button-1>", lambda event: self.pass_turn())
        elif self.match.get_state() == MatchState.PREPARATION and self.match.get_current_player().all_ships_placed() and not self.match.get_other_player_of_player(
                self.match.get_current_player()).all_ships_placed():
            self.button = tk.Button(self.game, text="Prêt", bg='light blue', fg='black', font=('Times New Roman', 20))
            self.button.pack(side=tk.BOTTOM)
            self.button.bind("<Button-1>", lambda event: self.pass_turn())
        elif self.match.get_state() == MatchState.PREPARATION and self.match.all_ships_of_players_placed():
            self.button = tk.Button(self.game, text="Commencer", bg='light blue', fg='black',
                                    font=('Times New Roman', 20))
            self.button.pack(side=tk.BOTTOM)
            self.button.bind("<Button-1>", lambda event: self.start())

        if self.match.get_state() == MatchState.PREPARATION:
            self.swith_orrientation = tk.Button(self.game,
                                                text=self.match.get_current_player().get_ship_orientation().get_display_name(),
                                                bg='light blue', fg='black', font=('Times New Roman', 20))
            self.swith_orrientation.pack(side=tk.BOTTOM)
            self.swith_orrientation.bind("<Button-1>", lambda event: self.switch_orientation())

        self.state = tk.Label(self.game, text="Etat: " + self.match.get_state().get_display_name(), bg='light blue',
                              fg='black', font=('Times New Roman', 20))
        self.state.pack(side=tk.BOTTOM)

        self.player = tk.Label(self.game, text=f"Joueur:  {self.match.get_current_player().get_id()}", bg='light blue',
                               fg='black', font=('Times New Roman', 20))

        self.player.pack(side=tk.BOTTOM)

        if self.match.get_state() == MatchState.PREPARATION:
            ship = self.match.get_current_player().get_selected_ship()
            if ship is not None:
                self.ship = tk.Label(self.game, text=f"Navire sélectionné: {ship.get_name()}",
                                     bg='light blue', fg='black', font=('Times New Roman', 20))
                self.ship.pack(side=tk.BOTTOM)

        self.title = tk.Label(self.game, text="Bataille Navale", bg='light blue', fg='black',
                              font=('Times New Roman', 30, "bold"))
        self.title.pack(side=tk.BOTTOM)

        if self.match.get_state() == MatchState.PREPARATION:
            for ship in self.match.get_current_player().get_ships():
                if ship.is_placed():
                    continue

                button = tk.Button(self.game, text=f"{ship.get_name()} {ship.get_length()}", bg='light blue',
                                   fg='black', font=('Times New Roman', 20))
                button.pack(side=tk.LEFT)
                button.bind("<Button-1>", lambda event, selected_ship=ship: self.select_ship(selected_ship))

    def select_ship(self, ship):
        self.match.get_current_player().select_ship(ship)
        self.match.refresh()

    def switch_orientation(self):
        self.match.get_current_player().switch_ship_orientation()
        self.match.refresh()

    def pass_turn(self):
        self.match.switch_player()
        self.match.refresh()

    def start(self):
        self.match.start()
