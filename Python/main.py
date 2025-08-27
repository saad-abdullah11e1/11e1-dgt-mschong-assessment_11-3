import tkinter as tk
import games.dino

window = tk.Tk()

window.title("Hello World App")

def button_click(button):
    game = games.dino.Game(window)

    game.game()

button = tk.Button(window, text="Click Me!", command=lambda: button_click(button))
button.pack(pady=20)


window.mainloop()