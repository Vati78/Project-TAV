import tkinter as tk
from tkinter import ttk

class PongMenu(tk.Tk):
    def __init__(self, itemList):
        super().__init__()
        self.title("Pong - Menu")
        self.resizable(False, False)

        self.itemList = itemList

        # Variables
        self.ball_speed = tk.IntVar(value=5)
        self.ball_size = tk.IntVar(value=30)
        self.human_players = tk.IntVar(value=1)
        self.bot_difficulty = tk.IntVar(value=5)
        self.bonus_freq = tk.IntVar(value=10)
        self.item_vars = {item: tk.BooleanVar(value=True) for item in itemList}

        self.build_ui()

    def slider(self, parent, text, var, from_, to, row):
        ttk.Label(parent, text=text).grid(row=row, column=0, sticky="w")
        slider = tk.Scale(parent, from_=from_, to=to, orient=tk.HORIZONTAL, variable=var)
        slider.set(var.get())
        slider.grid(row=row, column=1, padx=5, sticky="ew")

    def build_ui(self):
        frame = ttk.Frame(self, padding=15)
        frame.grid()
        frame.columnconfigure(1, weight=1)

        self.slider(frame, "Vitesse balle:", self.ball_speed, 1, 15, 0)
        self.slider(frame, "Taille balle:", self.ball_size, 5, 60, 1)
        self.slider(frame, "Nombre de joueurs:", self.human_players, 0, 2, 2)
        self.slider(frame, "Difficulté IA:", self.bot_difficulty, 1, 20, 3)
        self.slider(frame, "Fréquence bonus:", self.bonus_freq, 0, 80, 4)

     #   ttk.Label(frame, text="Joueurs humains").grid(row=4, column=0, sticky="w")
     #   ttk.Spinbox(frame, from_=0, to=2, textvariable=self.human_players, width=5).grid(row=4, column=1, sticky="w")

        ttk.Label(frame, text="Bonus disponibles:").grid(row=6, column=0, sticky="w", pady=(10, 0))

        bonus_frame = ttk.Frame(frame)
        bonus_frame.grid(row=7, column=0, columnspan=3, sticky="w")

        for i, (item, var) in enumerate(self.item_vars.items()):
            ttk.Checkbutton(
                bonus_frame, text=item, variable=var
            ).grid(row=i // 2, column=i % 2, sticky="w", padx=5)

        ttk.Button(
            frame, text="Tout", command=lambda: self.toggle_all(True)
        ).grid(row=8, column=0, pady=10)

        ttk.Button(
            frame, text="Rien", command=lambda: self.toggle_all(False)
        ).grid(row=8, column=1, pady=10, sticky="w")

        ttk.Button(
            frame, text="Lancer la partie", command=self.launch
        ).grid(row=9, column=0, columnspan=3, pady=10)

    def toggle_all(self, state):
        for var in self.item_vars.values():
            var.set(state)

    def launch(self):
        self.config = {
            "ball_speed": self.ball_speed.get(),
            "ball_size": self.ball_size.get(),
            "human_players": self.human_players.get(),
            "bot_difficulty": self.bot_difficulty.get(),
            "bonus_frequency": self.bonus_freq.get(),
            "active_items": [item for item, var in self.item_vars.items() if var.get()]
        }

        print("CONFIG:", self.config)
        self.quit()
        # start_game(config)


if __name__ == "__main__":
    import variants, inspect
    itemList = ["Portal"]
    for name, objet in inspect.getmembers(variants):
        if inspect.isclass(objet) and objet.variant:
            itemList.append(name)
    m = PongMenu(itemList)
    m.mainloop()
    import game
    jeu = game.Game(m.config)
    m.destroy()
    jeu.run()


#menu = PongMenu(itemList)
#menu.mainloop()

#config = menu.config   # récupéré après fermeture
#menu.destroy()