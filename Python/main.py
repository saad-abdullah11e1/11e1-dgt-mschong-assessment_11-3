import tkinter as tk
from tkinter import messagebox
import games.dino
import games.snake
import games.shooter
from PIL import Image, ImageTk

window = tk.Tk()

name = ""

window.title("Games Compendium")

def game_frame(game, title, desc, photo):
    base_colour = "#5A5A5A"
    hover_colour = "#8B8B8B"

    frame = tk.Frame(window, bg="#5A5A5A")
    # frame.pack(padx=20, pady=20)

    label = tk.Label(frame, bg="#5A5A5A", text=title)
    label.pack(pady=20)

    photo_label = tk.Label(frame, image=photo)

    photo_label.pack()

    button_frame = tk.Frame(frame, bg="#5A5A5A")
    button_frame.pack(fill="both", expand=True)

    button = tk.Label(
        button_frame, text="Click to Play", bg="#5A5A5A"
    )
    button.pack(pady=10)

    button_frame.bind("<Button-1>", lambda _: run_game(game))
    button.bind("<Button-1>", lambda _: run_game(game))

    def on_enter(event):
        button_frame.config(bg=hover_colour)
        button.config(bg=hover_colour)

    def on_leave(event):
        button_frame.config(bg=base_colour)
        button.config(bg=base_colour)

    button_frame.bind("<Enter>", on_enter)
    button_frame.bind("<Leave>", on_leave)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return frame

def close_name():
    global name

    if name_entry.get() == "" or any(i.isdigit() for i in name_entry.get()):
        messagebox.showwarning("Input Required", "Please enter a valid name.\n(No numbers)")

        input.focus()
        name_entry.focus()

        return

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

input.protocol("WM_DELETE_WINDOW", close_name)

input.bind("<Return>", lambda x: close_name())

input.wait_window()


def run_game(game):
    game.Game(window, name).game()


name_label = tk.Label(window, text="Hello, " + name, font=("", 20))
name_label.grid(row=1, column=2, pady=20)

dino = ImageTk.PhotoImage(Image.open("snake.jpeg"))
game_frame(games.dino, "Dino Game", "fun", dino).grid(row=2, column=1, padx=10, pady=10)

snake = ImageTk.PhotoImage(Image.open("snake.jpeg"))
game_frame(games.snake, "Snake Game", "fun", snake).grid(row=2, column=2, padx=10, pady=10)

shooter = ImageTk.PhotoImage(Image.open("snake.jpeg"))
game_frame(games.shooter, "Shooter Game", "fun", shooter).grid(row=2, column=3, padx=10, pady=10)

window.mainloop()
