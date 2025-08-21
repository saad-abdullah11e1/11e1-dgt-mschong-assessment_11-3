import tkinter as tk
import random

class Game:
    quit = False

    obstacles = []

    velocity = 0
    GRAVITY = 0.4
    JUMP_VELOCITY = -10

    game_speed = 10



    window: tk.Tk

    canvas: tk.Canvas

    floor: int

    score_label: int

    obstacles = []

    player: int
    
    def __init__(self):
        self.window = tk.Tk()

        self.window.title("Game")

        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=1400, height=800, background='white')

        self.canvas.pack()

        self.floor = self.canvas.create_rectangle(0, 600, 1400, 2000, fill='black')

        self.score_label = self.canvas.create_text(700, 50, text="Score: 0", font=("Arial", 24), fill="black")

        obstacle_width = random.randint(50, 150)

        self.obstacles = [self.canvas.create_rectangle(1000, 550, 1000+obstacle_width, 600, fill='red', outline='red')]

        self.player = self.canvas.create_rectangle(100, 550, 150, 600, fill='blue', outline='blue')

        self.window.bind('<space>', lambda event: self.player_jump())
        self.window.bind('<Down>', lambda event: self.player_duck())

    def game(self):
        while True:
            self.canvas.itemconfig(self.score_label, text=f"Score: {(10*(self.game_speed-10)):.0f}")

            for obstacle in self.obstacles:
                self.move_obstacle(obstacle)

            self.player_physics()  

            if self.quit == True:
                break

            self.game_speed += 0.005

            self.window.update()
            self.window.after(5)

        text = self.canvas.create_text(700, 400, text=f"Game Over\nScore: {(10*(self.game_speed-10)):.0f}", font=("Arial", 36), fill="Red")

        self.window.mainloop()


    def move_obstacle(self, obstacle):
        self.canvas.move(obstacle, -self.game_speed, 0)
        if self.canvas.coords(obstacle)[0] < -150:
            # canvas.delete(obstacle)
            # self.obstacles.remove(obstacle)
            self.canvas.move(obstacle, 1000, 0)

        obstacle = self.canvas.bbox(obstacle)
        if obstacle == None: return
        overlapping_items = self.canvas.find_overlapping(*obstacle)
        if self.player in overlapping_items:
            self.quit = True


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

    def player_duck(self):
        self.velocity = -2 * self.JUMP_VELOCITY

if __name__ == "__main__":
    Game().game()