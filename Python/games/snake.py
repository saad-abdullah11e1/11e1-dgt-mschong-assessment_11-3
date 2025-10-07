import tkinter as tk
import random
import time
from . import tktimer

class Game:
    WIDTH = 600
    HEIGHT = 600

    CELL_SIZE = 30

    GAME_SPEED = 150

    CELLY = int(HEIGHT/CELL_SIZE)
    CELLX = int(WIDTH/CELL_SIZE)

    GROW_SIZE = 5

    def __init__(self, root: tk.Tk):
        self.quit = False

        self.root = root

        self.game_speed = self.GAME_SPEED

        self.window = tk.Toplevel(self.root)
        self.window.focus()

        self.window.title("Game")

        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background='white')

        self.canvas.pack()

        for x in range(self.CELLX):
            for y in range(int(self.CELLY)):
                if (x+y) % 2 == 0: continue
                (x1, y1, x2, y2) = self.get_cell_coord(x, y)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='#DDD', outline='#FFFFFF')   

        self.snake = []

        (x1, y1, x2, y2) = self.get_cell_coord(int(self.CELLX/2), int(self.CELLY/2)) 
        self.snake.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00FF00", outline='#00FF00'))

        (x1, y1, x2, y2) = self.get_cell_coord(int(self.CELLX/2)-1, int(self.CELLY/2)) 
        self.snake.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00FF00", outline='#00FF00'))
        (x1, y1, x2, y2) = self.get_cell_coord(int(self.CELLX/2)-2, int(self.CELLY/2)) 
        self.snake.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00FF00", outline='#00FF00'))

        self.direction = (1, 0)
        self.new_directions = [(1, 0)]

        (x1, y1, x2, y2) = self.get_cell_coord(random.randint(0, self.CELLX-1), random.randint(0, self.CELLY-1)) 
        self.apple = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF0000", outline="#FF0000")

        self.window.bind('<Down>', lambda event: self.change_direction(0, 1))
        self.window.bind('<Up>', lambda event: self.change_direction(0, -1))
        self.window.bind('<Left>', lambda event: self.change_direction(-1, 0))
        self.window.bind('<Right>', lambda event: self.change_direction(1, 0))

        self.score_label = self.canvas.create_text(self.WIDTH/2, 50, text="Score: 0", font=("Arial", 24), fill="black")

    def game(self):
        self.game_tick_timer = tktimer.Timer(self.game_speed/1000)

        self.game_loop()
    
    def quit_game(self):
        with open("snake_highscore.txt") as f:
            highscore = f.read()

        if int(highscore) < len(self.snake):
            with open("snake_highscore.txt", "w") as f:
                highscore = f"{len(self.snake)}"
                f.write(highscore)
        
        text = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2, text=f"Game Over\nScore: {len(self.snake)}\nHighscore: {highscore}", font=("Arial", 36), fill="Red")
        
        self.window.bind('<space>', lambda event: self.restart())

    def get_cell_coord(self, x, y):
        return (x*self.CELL_SIZE, y*self.CELL_SIZE, (x+1)*self.CELL_SIZE, (y+1)*self.CELL_SIZE,)

    def change_direction(self, x, y):
        if len(self.new_directions) != 0:
            if -x == self.new_directions[0][0] or -y == self.new_directions[0][1]: return
        else:
            if -x == self.direction[0] or -y == self.direction[1]: return
        self.new_directions.append((x, y))

    def restart(self):
        old_window = self.window
        self.__init__(self.root)
        old_window.destroy()
        self.game()
        
    def game_loop(self):
        # print(self.new_directions)
        if len(self.new_directions) != 0:
            self.direction = self.new_directions[0]
            self.new_directions.pop(0)

        self.canvas.tag_raise(self.score_label)
        self.canvas.itemconfig(self.score_label, text=f"Score: {(len(self.snake)):.0f}")

        if self.quit == True:
            self.quit_game()
            return
        self.game_tick_timer = tktimer.Timer(self.game_speed/1000)

        staged_moves = []

        for (i, box) in enumerate(self.snake[1:]):
            (x1, y1, _, _) = self.canvas.coords(self.snake[i])
            (x, y, _, _) = self.canvas.coords(box)

            staged_moves.append((box, x1-x, y1-y))
            
        self.canvas.move(self.snake[0], self.direction[0]*self.CELL_SIZE, self.direction[1]*self.CELL_SIZE)
        for move in staged_moves:
            self.canvas.move(*move)
            
        if self.canvas.coords(self.snake[0]) == self.canvas.coords(self.apple):
            self.canvas.delete(self.apple)

            for i in range(self.GROW_SIZE):
                (x1, y1, x2, y2) = self.canvas.coords(self.snake[-1])
                self.snake.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00FF00", outline='#00FF00'))

            (x1, y1, x2, y2) = self.get_cell_coord(random.randint(0, self.CELLX-1), random.randint(0, self.CELLY-1))
            while [x1, y1, x2, y2] in [self.canvas.coords(part) for part in self.snake]:
                (x1, y1, x2, y2) = self.get_cell_coord(random.randint(0, self.CELLX-1), random.randint(0, self.CELLY-1))
            
            self.apple = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF0000", outline="#FF0000")

        for part in self.snake[1:]:
            if self.canvas.coords(self.snake[0]) == self.canvas.coords(part):
                self.quit = True

        (x1, y1, x2, y2) = self.canvas.coords(self.snake[0])

        if x1 < 0 or x2 > self.WIDTH or y1 < 0 or y2 > self.HEIGHT:
            self.quit = True

        self.window.after(self.game_speed, self.game_loop)

if __name__ == "__main__":
    Game().game()