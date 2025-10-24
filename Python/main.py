"""The main game compendium."""
import tkinter as tk
from tkinter import messagebox
import games.dino
import games.snake
import games.shooter
from PIL import Image, ImageTk
import pyglet

# Make window
window = tk.Tk()

# Name variable
name = ""

# Set tile
window.title("Games Compendium")

pyglet.font.add_file('VCR.ttf')


def game_frame(game, title, desc, photo):
    """Create game frame."""
    base_colour = "#5A5A5A"
    hover_colour = "#474747"

    # Create frame for game
    frame = tk.Frame(window, bg="#5A5A5A")

    # Label title
    label = tk.Label(frame, bg="#5A5A5A", text=title, font=('', 18))
    label.pack(pady=20)

    # Photo
    photo_label = tk.Label(frame, image=photo)

    photo_label.pack()

    # Play button
    button_frame = tk.Frame(frame, bg="#66B185")
    button_frame.pack(fill="both", expand=True)

    button = tk.Label(
        button_frame, text="Click to Play", bg="#66B185"
    )
    button.pack(pady=10)

    button_frame.bind("<Button-1>", lambda _: run_game(game))
    button.bind("<Button-1>", lambda _: run_game(game))

    def more_info():
        """Spawn the More Info window."""
        box = tk.Toplevel(window)

        desc_label = tk.Label(box, text=desc, wraplength=200)
        desc_label.pack(padx=15, pady=15)

    # More info
    info_button_frame = tk.Frame(frame, bg="#5A5A5A")
    info_button_frame.pack(fill="both", expand=True)

    info_button = tk.Label(
        info_button_frame, text="More Info", bg="#5A5A5A"
    )
    info_button.pack(pady=10)

    info_button_frame.bind("<Button-1>", lambda _: more_info())
    info_button.bind("<Button-1>", lambda _: more_info())

    def on_enter(frame, button, colour):
        """Ran when the mouse enters."""
        frame.config(bg=colour)
        button.config(bg=colour)

    def on_leave(frame, button, colour):
        """Ran when the mouse exits."""
        frame.config(bg=colour)
        button.config(bg=colour)

    button_frame.bind(
        "<Enter>",
        lambda _: on_enter(button_frame, button, "#518D6A")
    )
    button_frame.bind(
        "<Leave>",
        lambda _: on_leave(button_frame, button, "#66B185")
    )
    button.bind(
        "<Enter>",
        lambda _: on_enter(button_frame, button, "#518D6A")
    )
    button.bind(
        "<Leave>",
        lambda _: on_leave(button_frame, button, "#66B185")
    )

    info_button_frame.bind(
        "<Enter>",
        lambda _: on_enter(info_button_frame, info_button, hover_colour)
    )
    info_button_frame.bind(
        "<Leave>",
        lambda _: on_leave(info_button_frame, info_button, base_colour)
    )
    info_button.bind(
        "<Enter>",
        lambda _: on_enter(info_button_frame, info_button, hover_colour)
    )
    info_button.bind(
        "<Leave>",
        lambda _: on_leave(info_button_frame, info_button, base_colour)
    )

    return frame


def close_name():
    """Submit the information."""
    global name

    if name_entry.get() == "" or any(i.isdigit() for i in name_entry.get()):
        msg = "You have entered a blank or invalid name (numbers)\n" \
              "Are you sure you want to continue"
        if messagebox.askyesno("Input Required", msg) is True:
            name = name_entry.get()
            input.destroy()

            return

        input.focus()
        name_entry.focus()

        return

    name = name_entry.get()
    input.destroy()

# Name input
input = tk.Toplevel(window)
input.focus()

input.title("Dialogue Box")

name_label = tk.Label(input, text="Enter your name:")
name_label.pack(pady=10)

name_entry = tk.Entry(input, width=30)
name_entry.pack(pady=5, padx=5)
name_entry.focus_set()

# Submit button
submit_button = tk.Button(input, text="Submit", command=close_name)
submit_button.pack(pady=5)

input.protocol("WM_DELETE_WINDOW", close_name)

input.bind("<Return>", lambda x: close_name())

input.wait_window()


def run_game(game):
    """Run the game parameter."""
    game.Game(window, name).game()

# Actual game menu
name_label = tk.Label(window, text="Hello, " + name, font=("", 20))
name_label.grid(row=1, column=2, pady=20)

# Load game
# Save photo as variable so it doesn't get GC'd
dino = Image.open("dino.png")
dino.thumbnail((350, 350))
dino = ImageTk.PhotoImage(dino)
game_frame(
    games.dino,
    "Dino Game",
    "A fun game where you player as a dinosoar dodging boxes."
    "Space to jump, down arrow to quickfall",
    dino
).grid(row=2, column=1, padx=10, pady=10)

snake = Image.open("snake.png")
snake.thumbnail((350, 350))
snake = ImageTk.PhotoImage(snake)
game_frame(
    games.snake,
    "Snake Game",
    "The basic snake game. Use the arrow keys to move, eat the "
    "apples, don't hit yourself or the walls",
    snake
).grid(row=2, column=2, padx=10, pady=10)

shooter = Image.open("shooter.png")
shooter.thumbnail((350, 350))
shooter = ImageTk.PhotoImage(shooter)
game_frame(
    games.shooter,
    "Shooter Game",
    "A helicopter shooter game. Move around with the arrow keys and "
    "press space to shoot. You need to dodge the bullets and enemy aircraft.",
    shooter
).grid(row=2, column=3, padx=10, pady=10)

window.mainloop()
