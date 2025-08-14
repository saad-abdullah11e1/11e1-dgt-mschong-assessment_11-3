import tkinter as tk

window = tk.Tk()

greeting = tk.Label(window, text="Hello, World!")
greeting.pack()

button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)
button.bind("<Button-1>", lambda event: greeting.config(text="Button Clicked!"))
button.bind("<ButtonRelease>", lambda event: greeting.config(text="Hello, World!"))

button.pack()

window.mainloop()