import tkinter as tk
import random
import time
from . import tktimer

class Game:
    WIDTH = 1400
    HEIGHT = 800

    GRAVITY = 0.4
    JUMP_VELOCITY = -12.5
    GAME_PACE = 0.00025
    GAME_SPEED = 5
    
    def __init__(self, root: tk.Tk):
        self.quit = False

        self.velocity = 0

        self.game_speed = self.GAME_SPEED

        self.obstacles = []

        self.root = root

        self.window = tk.Toplevel(self.root)
        self.window.focus()

        self.window.title("Game")

        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background='white')

        self.canvas.pack()

        self.floor = self.canvas.create_rectangle(0, self.HEIGHT-200, self.WIDTH, self.HEIGHT, fill='black')

        self.score_label = self.canvas.create_text(self.WIDTH/2, 50, text="Score: 0", font=("Arial", 24), fill="black")

        self.player = self.canvas.create_rectangle(100, 550, 150, 600, fill='blue', outline='blue')

        self.window.bind('<space>', lambda event: self.player_jump())
        # self.window.bind('<KeyRelease-space>', lambda event: self.player_stop_jump())

        self.window.bind('<Down>', lambda event: self.player_duck())

    def game(self):
        obstacle_spawn_timer = tktimer.Timer(random.randint(int(10-self.game_speed/10), 20)/10)

        while True:
            if obstacle_spawn_timer.finished():
                obstacle_spawn_timer = tktimer.Timer(random.randint(int(10-self.game_speed/10), 20)/10)

                obstacle_width = random.randint(50, 150)
                obstacle_height = random.randint(50, 200-obstacle_width)

                obstacle = self.canvas.create_rectangle(1500, 600, 1500+obstacle_width, 600-obstacle_height, fill='red', outline='red')

                self.obstacles.append(obstacle)

            self.canvas.itemconfig(self.score_label, text=f"Score: {(10*(self.game_speed-self.GAME_SPEED)):.0f}")

            for obstacle in self.obstacles:
                self.move_obstacle(obstacle)

            self.player_physics()  

            if self.quit == True:
                break

            self.game_speed += self.GAME_PACE*self.game_speed

            self.window.update()
            self.window.after(5)

        with open("dino_highscore.txt") as f:
            highscore = f.read()

        if int(highscore) < int(10*(self.game_speed-self.GAME_SPEED)):
            with open("dino_highscore.txt", "w") as f:
                highscore = f"{(10*(self.game_speed-self.GAME_SPEED)):.0f}"
                f.write(highscore)
        


        text = self.canvas.create_text(700, 400, text=f"Game Over\nScore: {(10*(self.game_speed-self.GAME_SPEED)):.0f}\nHighscore: {highscore}", font=("Arial", 36), fill="Red")
        
        self.window.bind('<space>', lambda event: self.restart())

        self.window.wait_window()
        self.window.destroy()

        
    def move_obstacle(self, obstacle):
        self.canvas.move(obstacle, -self.game_speed, 0)
        
        obstacle_box = self.canvas.bbox(obstacle)

        overlapping_items = self.canvas.find_overlapping(*obstacle_box)
        if self.player in overlapping_items:
            self.quit = True
        
        if self.canvas.coords(obstacle)[0] < -150:
            self.canvas.delete(obstacle)
            self.obstacles.remove(obstacle)
            # self.canvas.move(obstacle, 1000, 0)


    def player_physics(self):
        self.canvas.move(self.player, 0, self.velocity)

        if self.canvas.coords(self.player)[1] < 550:
            self.velocity += self.GRAVITY
        else:
            self.velocity = 0
            self.canvas.move(self.player, 0, 550 - self.canvas.coords(self.player)[1])
    

    def player_jump(self):
        if self.velocity == 0:
            self.velocity = self.JUMP_VELOCITY

    def player_stop_jump(self):
        self.velocity *= 0.1

    def player_duck(self):
        self.velocity = -2 * self.JUMP_VELOCITY
    
    def restart(self):
        old_window = self.window
        self.__init__(self.root)
        old_window.destroy()
        self.game()
        

if __name__ == "__main__":
    Game().game()