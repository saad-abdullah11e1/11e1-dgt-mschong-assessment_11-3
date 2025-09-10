import tkinter as tk
import random
import time
from . import tktimer

class Game:
    WIDTH = 600
    HEIGHT = 600

    CELL_SIZE = 20

    GAME_SPEED = 500

    CELLY = int(HEIGHT/CELL_SIZE)
    CELLX = int(WIDTH/CELL_SIZE)

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

        self.window.bind('<Down>', lambda event: self.change_direction(0, 1))
        self.window.bind('<Up>', lambda event: self.change_direction(0, -1))
        self.window.bind('<Left>', lambda event: self.change_direction(-1, 0))
        self.window.bind('<Right>', lambda event: self.change_direction(1, 0))

    def game(self):
        game_tick_timer = tktimer.Timer(self.game_speed/1000)

        while True:
            if self.quit == True:
                break
            
            if game_tick_timer.finished():
                game_tick_timer = tktimer.Timer(self.game_speed/1000)

                for (i, box) in enumerate(self.snake[1:]):
                    print(i)
                    (x1, y1, _, _) = self.canvas.coords(self.snake[i])
                    (x, y, _, _) = self.canvas.coords(box)

                    print(x1)
                    print(x)

                    self.canvas.move(box, x1-x, y1-y)
                
                self.canvas.move(self.snake[0], self.direction[0]*self.CELL_SIZE, self.direction[1]*self.CELL_SIZE)

            self.window.update()
            self.window.after(5)

        self.window.wait_window()
        self.window.destroy()

    def get_cell_coord(self, x, y):
        return (x*self.CELL_SIZE, y*self.CELL_SIZE, (x+1)*self.CELL_SIZE, (y+1)*self.CELL_SIZE,)

    def change_direction(self, x, y):
        if -x == self.direction[0] or -y == self.direction[1]: return
        self.direction = (x, y)

    def restart(self):
        old_window = self.window
        self.__init__(self.root)
        old_window.destroy()
        self.game()
        

if __name__ == "__main__":
    Game().game()