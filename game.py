from match.match import MatchType
import tkinter as tk
import sys
import os

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
        self.match = None
        self.init_ui()

    def init_ui(self):
        self.clear()
        TitleText(self, "Bataille Navale").pack(side=tk.TOP, pady=50)

        button = tk.Button(self, text=f"Start {MatchType.PLAYER_VS_PLAYER.get_display_name()}", command=None, bg='turquoise', width=20, height=2)
        button.bind("<Button-1>", lambda event: self.select_match(MatchType.PLAYER_VS_PLAYER))
        button.pack(side=tk.TOP, pady=10)

        button = tk.Button(self, text=f"Start {MatchType.PLAYER_VS_AI.get_display_name()}", command=None, bg='turquoise', width=20, height=2)
        button.bind("<Button-1>", lambda event: self.select_match(MatchType.PLAYER_VS_AI))
        button.pack(side=tk.TOP, pady=10)

        tk.Button(self, text="Leave the game", command=self.quit, bg='turquoise', width=20, height=2).pack(side=tk.TOP, pady=10)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def select_match(self, type):
        print(f"Starting {type.get_display_name()} match.")
        self.match = type.get_match(self)
        self.match.start_game()

    def quit_game(self):
        self.quit()

if __name__ == '__main__':
    app = Menu()
    app.mainloop()