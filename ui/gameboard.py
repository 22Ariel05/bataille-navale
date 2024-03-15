import tkinter as tk

class MyButton(tk.Button):
    def __init__(self, master, t):
        self.text = t
        tk.Button.__init__(self, master, text= self.text)
        self.configure(width= 20, height= 2)
        self.configure(bg= 'turquoise', fg= 'white')
        self.configure(font= ('Times New Roman', 20, 'bold'))
        self.configure(command= self.fonction)

    def fonction(self):
        print(f'Vous avez appuyé sur le bouton {self.text[1]}.')

class GameChoice(tk.Frame):
    def __init__(self, master,):
        tk.Frame.__init__(self, master, width= 100, height= 100)
        self.configure(bg= 'light blue')
        self.button_list = [MyButton(self, text) for text in ('Player Vs Player','Player Vs Bot', 'Leave the game')]
        for k, button in enumerate(self.button_list):
            button.grid(row= k, column= 0, padx= 20, pady= 20)

class TitleText(tk.Label):
    def __init__(self, master, t=None):
        tk.Label.__init__(self, master)
        self.configure(text=t)
        self.configure(bg= "light blue",fg='black')
        self.configure(font=('Times New Roman', 30,"bold"))
        

class Menu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(bg= 'light blue')
        self.state('zoomed')
        self.geometry('1000x800+400+0')
        # Création de la fenêtre
        self.title_label = TitleText(self, t="Bataille Navale")
        self.menu_frame = GameChoice(self)

        # Centrer la fenêtre
        self.title_label.place(relx=0.5, rely=0.15, anchor="center")
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

if __name__ == '__main__':
    app = Menu()
    app.mainloop()
