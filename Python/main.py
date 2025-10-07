import tkinter as tk
from tkinter import messagebox
import games.dino
import games.snake
import games.shooter


window = tk.Tk()

window.title("Games Compendium")

name = ''

def run_game(game):
    game.Game(window).game()



dino_button = tk.Button(window, text="Dino Run", command=lambda: run_game(games.dino))
dino_button.pack(pady=20)

snake_button = tk.Button(window, text="Snake", command=lambda: run_game(games.snake))
snake_button.pack(pady=20)

shooter_button = tk.Button(window, text="Shooter", command=lambda: run_game(games.shooter))
shooter_button.pack(pady=20)

def close_name():
    global name

    name = name_entry.get()
    input.destroy()

input = tk.Toplevel(window)
input.focus()

input.title("Dialogue Box")

name_label = tk.Label(input, text="Enter your name:")
name_label.pack(pady=10)

name_entry = tk.Entry(input, width=30)
name_entry.pack(pady=5, padx=5)
name_entry.focus_set()

submit_button = tk.Button(input, text="Submit", command=close_name)
submit_button.pack(pady=5)

def disable_event():
    if name_entry.get() == '':
        messagebox.showwarning("Input Required", "Please enter a username.")
    else:
        close_name()

input.protocol("WM_DELETE_WINDOW", disable_event)

input.wait_window()



window.mainloop()