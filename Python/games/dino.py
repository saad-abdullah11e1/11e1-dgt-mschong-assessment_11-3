import tkinter as tk
import random

quit = False

floor = None
obstacle = None

velocity = 0
GRAVITY = 0.4
JUMP_VELOCITY = -10

game_speed = 10

def game():
    global game_speed
    window = tk.Tk()

    window.title("Game")

    window.resizable(False, False)

    canvas = tk.Canvas(window, width=1400, height=800, background='white')

    canvas.pack()

    floor = canvas.create_rectangle(0, 600, 1400, 2000, fill='black')

    obstacle_width = random.randint(50, 150)

    obstacle = canvas.create_rectangle(1000, 550, 1000+obstacle_width, 600, fill='red', outline='red')

    obstacle_width = random.randint(50, 150)

    obstacle2 = canvas.create_rectangle(2000, 550, 2000+obstacle_width, 600, fill='red', outline='red')

    player = canvas.create_rectangle(100, 550, 150, 600, fill='blue', outline='blue')
    window.bind('<space>', lambda event: player_jump(canvas, player))
    window.bind('<Down>', lambda event: player_duck(canvas, player))

    while True:
        move_obstacle(canvas, obstacle)
        move_obstacle(canvas, obstacle2)

        player_physics(canvas, player, obstacle)

        if quit == True:
            break

        game_speed += 0.005

        window.update()
        window.after(5)

    text = canvas.create_text(700, 400, text="Game Over", font=("Arial", 36), fill="Red")

    window.mainloop()

def move_obstacle(canvas, obstacle):
    canvas.move(obstacle, -game_speed, 0)
    if canvas.coords(obstacle)[0] < -150:
        obstacle_width = random.randint(50, 150)
        canvas.coords(obstacle, 1400, 550, 1400 + obstacle_width, 600)
        canvas.move(obstacle, 1400, 0)

def player_physics(canvas, player, obstacle):
    global velocity
    global quit
    canvas.move(player, 0, velocity)

    if canvas.coords(player)[1] < 550:
        velocity += GRAVITY
    else:
        velocity = 0
        canvas.move(player, 0, 550 - canvas.coords(player)[1])
    
    obstacle = canvas.bbox(obstacle)
    overlapping_items = canvas.find_overlapping(*obstacle)
    if player in overlapping_items:
        quit = True

    

def player_jump(canvas, player):
    global velocity
    if velocity == 0:
        velocity = JUMP_VELOCITY

def player_duck(canvas, player):
    global velocity
    velocity = -2 * JUMP_VELOCITY

if __name__ == "__main__":
    game()