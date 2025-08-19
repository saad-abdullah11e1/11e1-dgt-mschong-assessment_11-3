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

    score_label = canvas.create_text(700, 50, text="Score: 0", font=("Arial", 24), fill="black")

    obstacle_width = random.randint(50, 150)

    obstacle = canvas.create_rectangle(1000, 550, 1000+obstacle_width, 600, fill='red', outline='red')

    obstacle_width = random.randint(50, 150)

    obstacle2 = canvas.create_rectangle(2500, 550, 2500+obstacle_width, 600, fill='red', outline='red')

    player = canvas.create_rectangle(100, 550, 150, 600, fill='blue', outline='blue')
    window.bind('<space>', lambda event: player_jump())
    window.bind('<Down>', lambda event: player_duck())

    while True:
        canvas.itemconfig(score_label, text=f"Score: {(10*(game_speed-10)):.0f}")

        move_obstacle(canvas, obstacle, player)
        move_obstacle(canvas, obstacle2, player)

        player_physics(canvas, player)

        if quit == True:
            break

        game_speed += 0.005

        window.update()
        window.after(5)

    text = canvas.create_text(700, 400, text=f"Game Over\nScore: {1}", font=("Arial", 36), fill="Red")

    window.mainloop()

def move_obstacle(canvas, obstacle, player):
    global quit
    canvas.move(obstacle, -game_speed, 0)
    if canvas.coords(obstacle)[0] < -150:
        obstacle_width = random.randint(50, 150)
        canvas.coords(obstacle, 1400, 550, 1400 + obstacle_width, 600)
        canvas.move(obstacle, 1400, 0)
    
    obstacle = canvas.bbox(obstacle)
    overlapping_items = canvas.find_overlapping(*obstacle)
    if player in overlapping_items:
        quit = True


def player_physics(canvas, player, ):
    global velocity
    global quit
    canvas.move(player, 0, velocity)

    if canvas.coords(player)[1] < 550:
        velocity += GRAVITY
    else:
        velocity = 0
        canvas.move(player, 0, 550 - canvas.coords(player)[1])
    

def player_jump():
    global velocity
    if velocity == 0:
        velocity = JUMP_VELOCITY

def player_duck():
    global velocity
    velocity = -2 * JUMP_VELOCITY

if __name__ == "__main__":
    game()