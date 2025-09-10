import tkinter as tk
import games.dino
import games.snake

window = tk.Tk()

window.title("Hello World App")


def run_game(game):
    game.game()

dino_button = tk.Button(window, text="Dino Run", command=lambda: run_game(games.dino.Game(window)))
dino_button.pack(pady=20)

snake_button = tk.Button(window, text="Snake", command=lambda: run_game(games.snake.Game(window)))
snake_button.pack(pady=20)

window.mainloop()