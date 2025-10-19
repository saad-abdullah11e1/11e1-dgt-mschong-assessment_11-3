import tkinter as tk
import random
import time
from . import tktimer
import PIL

class Game:
    WIDTH = 1400
    HEIGHT = 800

    GRAVITY = 0.4
    JUMP_VELOCITY = -12.5
    GAME_PACE = 0.00025
    GAME_SPEED = 5
    
    def __init__(self, root: tk.Tk, name):
        self.quit = False

        self.name = name

        self.velocity = 0

        self.game_speed = self.GAME_SPEED

        self.obstacles = []
        self.obstacle_images = []

        self.root = root

        self.window = tk.Toplevel(self.root)
        self.window.focus()

        self.window.title("Game")

        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background='white')

        self.canvas.pack()

        self.floor = self.canvas.create_rectangle(0, self.HEIGHT-200, self.WIDTH, self.HEIGHT, fill='black')

        self.score_label = self.canvas.create_text(self.WIDTH/2, 50, text="Score: 0", font=("Arial", 24), fill="black")

        #self.player = self.canvas.create_rectangle(100, 550, 150, 600, fill='blue', outline='blue')

        self.player_image = PIL.Image.open("snake.jpeg")
        self.player_image = self.player_image.resize((51, 51))
        self.player_image = PIL.ImageTk.PhotoImage(self.player_image)
        self.player = self.canvas.create_image(100, 550, image=self.player_image, anchor="nw")

        self.window.bind('<space>', lambda event: self.player_jump())
        # self.window.bind('<KeyRelease-space>', lambda event: self.player_stop_jump())

        self.window.bind('<Down>', lambda event: self.player_duck())

    def game(self):
        self.obstacle_spawn_timer = tktimer.Timer(random.randint(int(10-self.game_speed/10), 20)/10)

        self.game_loop()

    def quit_game(self):
        with open("dino_highscore.txt") as f:
            name, highscore = f.read().split(':')

        if int(highscore) < int(10*(self.game_speed-self.GAME_SPEED)):
            with open("dino_highscore.txt", "w") as f:
                highscore = f"{(10*(self.game_speed-self.GAME_SPEED)):.0f}"
                name = self.name
                f.write(self.name+":"+highscore)
        


        text = self.canvas.create_text(700, 400, text=f"Game Over\nScore: {(10*(self.game_speed-self.GAME_SPEED)):.0f}\nHighscore: {highscore} by {name}", font=("Arial", 36), fill="Red")
        
        self.window.bind('<space>', lambda event: self.restart())

        
    def move_obstacle(self, obstacle):
        self.canvas.move(obstacle, -self.game_speed, 0)
        
        obstacle_box = self.canvas.bbox(obstacle)

        overlapping_items = self.canvas.find_overlapping(*obstacle_box)
        if self.player in overlapping_items:
            self.quit = True
        
        if self.canvas.coords(obstacle)[0] < -150:
            self.canvas.delete(obstacle)
            self.obstacles.remove(obstacle)
            self.obstacle_images.pop(0)
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
        self.__init__(self.root, self.name)
        old_window.destroy()
        self.game()
    
    def game_loop(self):
        if self.obstacle_spawn_timer.finished():
            self.obstacle_spawn_timer = tktimer.Timer(random.randint(int(10-self.game_speed/10), 20)/10)

            obstacle_width = random.randint(50, 150)
            obstacle_height = random.randint(50, 200-obstacle_width)

            obstacle_image = PIL.Image.open("snake.jpeg")
            obstacle_image = obstacle_image.resize((obstacle_width, obstacle_height+1))
            self.obstacle_images.append(PIL.ImageTk.PhotoImage(obstacle_image))
            obstacle = self.canvas.create_image(1500, 600-obstacle_height, image=self.obstacle_images[-1], anchor="nw")

            #obstacle = self.canvas.create_rectangle(1500, 600, 1500+obstacle_width, 600-obstacle_height, fill='red', outline='red')

            self.obstacles.append(obstacle)

        self.canvas.itemconfig(self.score_label, text=f"Score: {(10*(self.game_speed-self.GAME_SPEED)):.0f}")

        for obstacle in self.obstacles:
            self.move_obstacle(obstacle)

        self.player_physics()  

        if self.quit == True:
            self.quit_game()
            return

        self.game_speed += self.GAME_PACE*self.game_speed

        self.window.after(10, self.game_loop)

if __name__ == "__main__":
    Game().game()