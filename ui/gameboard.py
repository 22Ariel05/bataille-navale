import tkinter as tk

class MyButton(tk.Button):
    def __init__(self, master, main_app, t):
        super().__init__(master, text=t, width=20, height=2, bg='turquoise', fg='white', font=('Times New Roman', 20, 'bold'))
        self.text = t
        self.main_app = main_app
        self.configure(command=self.fonction)

    def fonction(self):
        print(f'Vous avez appuyé sur le bouton {self.text}.')
        if self.text == "Leave the game":
            self.main_app.quit_game()
        elif self.text == "Player Vs Player":
            self.main_app.init_player_vs_player()

class GameChoice(tk.Frame):
    def __init__(self, master, main_app):
        super().__init__(master, bg='light blue')
        self.grid(row=0, column=0, sticky="nsew")
        self.main_app = main_app
        self.create_buttons()

    def create_buttons(self):
        texts = ['Player Vs Player', 'Player Vs Bot', 'Leave the game']
        for i, text in enumerate(texts):
            button = MyButton(self, self.main_app, text)
            button.grid(row=i, column=0, padx=20, pady=20)

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg='light blue')
        self.state('zoomed')
        self.geometry('1000x800+400+0')
        self.title("Bataille Navale")
        self.create_menu()

    def create_menu(self):
        self.title_label = TitleText(self, "Bataille Navale")
        self.title_label.place(relx=0.5, rely=0.15, anchor="center")
        self.menu_frame = GameChoice(self, self)
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def init_player_vs_player(self):
        self.clear_screen()
        # Initialiser l'interface pour le jeu Player Vs Player ici
        self.title_label = TitleText(self, "Bataille Navale - Joueur Vs Joueur")
        self.title_label.place(relx=0.5, rely=0.15, anchor="center")
        # Ajouter plus d'éléments pour le jeu

    def quit_game(self):
        self.quit()

class TitleText(tk.Label):
    def __init__(self, master, t):
        super().__init__(master, text=t, bg="light blue", fg='black', font=('Times New Roman', 30, "bold"))

if __name__ == '__main__':
    app = Menu()
    app.mainloop()
