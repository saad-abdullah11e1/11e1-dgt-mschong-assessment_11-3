import tkinter as tk
import time

window = tk.Tk()

count = 0

old_time = time.time()

greeting = tk.Label(window, text=count)
greeting.pack()

button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)

def on_click(event):
    global count
    global old_time
    count += 1

def update_clicks():
    global count
    global old_time
    greeting.config(text=int(count/(time.time()-old_time)))
    print(count)
    button.after(100, update_clicks)

def reset_timer():
    global old_time
    old_time = time.time()
    global count
    count = 0
    greeting.config(text=int(count/(time.time()-old_time)))
    print(count)
    button.after(1000, reset_timer)

button.bind("<Button-1>", on_click)
button.after(1000, reset_timer)
button.after(100, update_clicks)


button.pack()

window.mainloop()