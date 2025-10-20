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

    PLAYER_ANIM_SPEED = 0.075
    
    def __init__(self, root: tk.Tk, name):
        self.quit = False

        self.name = name

        self.velocity = 0

        self.game_speed = self.GAME_SPEED

        self.obstacles = []
        self.obstacle_image = PIL.Image.open("sprites/obstacle.png")
        self.obstacle_image = self.obstacle_image.resize((50, 50), PIL.Image.NEAREST)
        self.obstacle_image = PIL.ImageTk.PhotoImage(self.obstacle_image)

        self.root = root

        self.window = tk.Toplevel(self.root)
        self.window.focus()

        self.window.title("Game")

        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background='#AFCFC2')

        self.canvas.pack()

        self.floor_image = PIL.Image.open("sprites/floor.png")
        self.floor_image = self.floor_image.resize((50, 50), PIL.Image.NEAREST)
        self.floor_image = PIL.ImageTk.PhotoImage(self.floor_image)

        for y in range(self.HEIGHT-200, self.HEIGHT+50, 50):
            for x in range(0, self.WIDTH+50, 50):
                tile = self.canvas.create_image(x, y, image=self.floor_image, anchor="nw")

        self.score_label = self.canvas.create_text(self.WIDTH/2, 50, text="Score: 0", font=("Arial", 24), fill="black")

        #self.player = self.canvas.create_rectangle(100, 550, 150, 600, fill='blue', outline='blue')

        self.player_anim_state = 0

        self.player_animations = [1, 2, 3]

        player_image = PIL.Image.open("sprites/dino_stand.png")
        player_image = player_image.resize((51, 51), PIL.Image.NEAREST)
        self.player_animations[0] = PIL.ImageTk.PhotoImage(player_image)

        player_image = PIL.Image.open("sprites/dino_0.png")
        player_image = player_image.resize((51, 51), PIL.Image.NEAREST)
        self.player_animations[1] = PIL.ImageTk.PhotoImage(player_image)
        
        player_image = PIL.Image.open("sprites/dino_1.png")
        player_image = player_image.resize((51, 51), PIL.Image.NEAREST)
        self.player_animations[2] = PIL.ImageTk.PhotoImage(player_image)


        self.player = self.canvas.create_image(100, 550, image=self.player_animations[0], anchor="nw")

        self.window.bind('<space>', lambda event: self.player_jump())
        # self.window.bind('<KeyRelease-space>', lambda event: self.player_stop_jump())

        self.window.bind('<Down>', lambda event: self.player_duck())

    def game(self):
        self.obstacle_spawn_timer = tktimer.Timer(random.randint(int(10-self.game_speed/10), 20)/5)
        self.player_anim_timer = tktimer.Timer(self.PLAYER_ANIM_SPEED)

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
            # self.canvas.move(obstacle, 1000, 0)


    def player_physics(self):
        if self.player_anim_timer.finished() == True:
            self.player_anim_timer = tktimer.Timer(self.PLAYER_ANIM_SPEED)

            if self.player_anim_state == 0:
                self.canvas.itemconfig(self.player, image=self.player_animations[2])

                self.player_anim_state = 1
            elif self.player_anim_state == 1:
                self.canvas.itemconfig(self.player, image=self.player_animations[1])

                self.player_anim_state = 0


        self.canvas.move(self.player, 0, self.velocity)

        if self.canvas.coords(self.player)[1] < 550:
            self.velocity += self.GRAVITY

            self.canvas.itemconfig(self.player, image=self.player_animations[0])
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
            self.obstacle_spawn_timer = tktimer.Timer(random.randint(int(10-self.game_speed/10), 20)/5)

            obstacle_width = random.randint(1, 3)
            obstacle_height = random.randint(1, 4-obstacle_width)

            for w in range(1, obstacle_width+1):
                for h in range(1, obstacle_height+1):
                    obstacle = self.canvas.create_image(1500-w*50, 601-h*50, image=self.obstacle_image, anchor="nw")
                    self.obstacles.append(obstacle)

        self.canvas.itemconfig(self.score_label, text=f"Score: {(10*(self.game_speed-self.GAME_SPEED)):.0f}")

        for obstacle in self.obstacles[:]:
            self.move_obstacle(obstacle)

        self.player_physics()  

        if self.quit == True:
            self.quit_game()
            return

        self.game_speed += self.GAME_PACE*self.game_speed

        self.window.after(10, self.game_loop)

if __name__ == "__main__":
    Game().game()