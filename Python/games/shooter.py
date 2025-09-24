import tkinter as tk
import random
import time
import math
from . import tktimer

class Game:
    WIDTH = 600
    HEIGHT = 600

    GAME_SPEED = 10

    SPEED = 3
    FRICTION = 0.1
    ACCELERATION = 0.1

    BULLET_SPEED = 10
    SHOOT_COOLDOWN = 100

    ENEMY_BULLET_SPEED = 2

    ENEMY_SPEED = 2

    BIG_HELI_SHOOT_RATE = 3
    BIG_HELI_SPEED = 1
    BIG_HELI_MAX_HEALTH = 5

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

        self.player = self.canvas.create_rectangle(self.WIDTH/2, self.HEIGHT/2, self.WIDTH/2+25, self.HEIGHT/2+25, fill="#00FF00", outline='#00FF00')
        
        self.enemies = []
        self.lost_enemy_directions = {}

        self.enemies.append(self.canvas.create_rectangle(self.WIDTH/2, self.HEIGHT/4, self.WIDTH/2+25, self.HEIGHT/4+25, fill="#FF0000", outline="#FF0000"))

        self.big_helicopters = {}

        big_helicopter = self.canvas.create_rectangle(self.WIDTH/2, self.HEIGHT/4, self.WIDTH/2+40, self.HEIGHT/4+65, fill="#0000FF", outline="#0000FF")
        
        self.big_helicopters[big_helicopter] = [tktimer.Timer(self.BIG_HELI_SHOOT_RATE), [self.WIDTH/2, self.HEIGHT/4], self.BIG_HELI_MAX_HEALTH]

        self.enemy_bullets = {}

        self.bullets = []

        self.velocity = [0, 0]

        self.window.bind("<KeyPress>", self.key_pressed)
        self.window.bind("<KeyRelease>", self.key_released)

        self.window.bind("<space>", self.shoot)

        self.keyboard = {}

    def game(self):
        self.enemy_spawn_timer = tktimer.Timer(1)
        self.big_helicopter_spawn_timer = tktimer.Timer(10)

        while True:
            if self.quit == True:
                break

            if self.enemy_spawn_timer.finished() == True:
                x = random.randint(0, self.WIDTH-50)

                self.enemies.append(self.canvas.create_rectangle(x, -25, x+25, 0, fill="#FF0000", outline="#FF0000"))
                self.enemy_spawn_timer = tktimer.Timer(1)

            if self.big_helicopter_spawn_timer.finished() == True:
                x = random.randint(0, self.WIDTH-50)

                big_helicopter = self.canvas.create_rectangle(x-20, -65, x+20, 0, fill="#0000FF", outline="#0000FF")
                self.big_helicopters[big_helicopter] = [tktimer.Timer(self.BIG_HELI_SHOOT_RATE), [x, self.HEIGHT/4], self.BIG_HELI_MAX_HEALTH]

                self.big_helicopter_spawn_timer = tktimer.Timer(10)


            self.player_physics()

            self.bullet_physics()

            for enemy in self.enemies:
                self.enemy_ai(enemy)
            
            for big_helicopter in self.big_helicopters.keys():
                self.big_helicopter_ai(big_helicopter)
            
            for bullet in self.enemy_bullets.keys():
                direction = [self.enemy_bullets[bullet][0]*self.ENEMY_BULLET_SPEED, self.enemy_bullets[bullet][1]*self.ENEMY_BULLET_SPEED]

                self.canvas.move(bullet, *direction)

            self.window.update()
            self.window.after(self.game_speed)
        
        
        self.window.bind('<space>', lambda event: self.restart())

        self.window.wait_window()
        self.window.destroy()

    def move(self, x, y):
        if x != 0:
            self.velocity[0] = x*self.SPEED

        if y != 0:
            self.velocity[1] = y*self.SPEED

    def key_pressed(self, event):
        self.keyboard[event.keysym] = True
    def key_released(self, event):
        self.keyboard[event.keysym] = False

    def is_pressed(self, key):
        if key in self.keyboard:
            return self.keyboard[key]
        else: return False

    def bullet_physics(self):
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, -self.BULLET_SPEED)
            
            for enemy in self.enemies:
                enemy_box = self.canvas.coords(enemy)
                bullet_box = self.canvas.coords(bullet)

                if self.is_colliding(enemy_box, bullet_box) == True:
                    self.canvas.delete(enemy)
                    self.enemies.remove(enemy)

                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    
                    break

        for bullet in self.bullets:    
            for big_heli in list(self.big_helicopters.keys()):
                enemy_box = self.canvas.coords(big_heli)
                bullet_box = self.canvas.coords(bullet)

                if self.is_colliding(enemy_box, bullet_box) == True:
                    self.big_helicopters[big_heli][2] -= 1

                    if self.big_helicopters[big_heli][2] <= 0:
                        self.canvas.delete(big_heli)
                        self.big_helicopters.pop(big_heli)

                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    
                    break
                if self.is_colliding(self.canvas.coords(big_heli), (0, 0, self.WIDTH, self.HEIGHT)) == False:
                    self.canvas.delete(big_heli)
                    self.big_helicopters.pop(big_heli)


    def is_colliding(self, a, b):
        (ax1, ay1, ax2, ay2) = a
        (bx1, by1, bx2, by2) = b

        if ax2 < bx1 or bx2 < ax1:
            return False
    
        if ay2 < by1 or by2 < ay1:
            return False
    
        return True

    def player_input(self):
        velocity = [0, 0]
        if self.is_pressed('Up'):
            velocity[1] += -1
        if self.is_pressed('Down'):
            velocity[1] += 1
        if self.is_pressed('Left'):
            velocity[0] += -1
        if self.is_pressed('Right'):
            velocity[0] += 1

        if velocity != [0, 0]:
            magnitude = math.sqrt(velocity[0]**2 + velocity[1]**2)
            velocity[0] /= magnitude
            velocity[1] /= magnitude

        self.move(*velocity)
        return velocity
        

    def player_physics(self):
        if self.player_input()[0] == 0:
            self.velocity[0] *= 1-self.FRICTION
        if self.player_input()[1] == 0:
            self.velocity[1] *= 1-self.FRICTION

        self.canvas.move(self.player, self.velocity[0], self.velocity[1])

        player_box = self.canvas.coords(self.player)

        if self.is_colliding(player_box, (25, 25, self.WIDTH-25, self.HEIGHT-25)) == False:
            if player_box[0] < 25 or player_box[2] > self.WIDTH:
                self.canvas.move(self.player, -self.velocity[0], 0)
            if player_box[1] < 25 or player_box[3] > self.HEIGHT:
                self.canvas.move(self.player, 0, -self.velocity[1])

        for enemy in self.enemies:
            enemy_box = self.canvas.coords(enemy)
            player_box = self.canvas.coords(self.player)

            if self.is_colliding(player_box, enemy_box) == True:
                self.quit = True

        for bullet in self.enemy_bullets.keys():
            bullet_box = self.canvas.coords(bullet)
            player_box = self.canvas.coords(self.player)

            if self.is_colliding(player_box, bullet_box) == True:
                self.quit = True

        for big_helicopter in self.big_helicopters.keys():
            heli_box = self.canvas.coords(big_helicopter)
            player_box = self.canvas.coords(self.player)

            if self.is_colliding(player_box, heli_box) == True:
                self.quit = True
        
    def shoot(self, event):
        (x1, y1, x2, y2) = self.canvas.coords(self.player)

        center = [(x1+x2)/2, (y1+y2)/2]

        bullet = self.canvas.create_rectangle(center[0]-2, center[1]-10, center[0]+2, center[1]+10, fill="#000000", outline="#000000")

        self.bullets.append(bullet)

    def enemy_ai(self, enemy):
        if enemy in self.lost_enemy_directions:
            self.canvas.move(enemy, *self.lost_enemy_directions[enemy])
            return

        (x1, y1, x2, y2) = self.canvas.coords(self.player)
        player_coords = [(x1+x2)/2, (y1+y2)/2]

        (x1, y1, x2, y2) = self.canvas.coords(enemy)
        enemy_coords = [(x1+x2)/2, (y1+y2)/2]

        direction = [0, 0]

        direction[0] = player_coords[0]-enemy_coords[0]
        direction[1] = player_coords[1]-enemy_coords[1]
        
        length = math.sqrt(direction[0]**2 + direction[1]**2)*self.ENEMY_SPEED**-1
        if length == 0:
            direction = [0, 0]
        else:
            direction = [direction[0]/length, direction[1]/length]

        if direction[1] < 0:
            direction[1] = 0

            self.lost_enemy_directions[enemy] = direction
        self.canvas.move(enemy, *direction)

    def big_helicopter_ai(self, big_helicopter):
        (x1, y1, x2, y2) = self.canvas.coords(big_helicopter)
        (x, y) = [(x1+x2)/2, (y1+y2)/2]

        goal = self.big_helicopters[big_helicopter][1]

        direction = [0, 0]

        direction[0] = goal[0]-x
        direction[1] = goal[1]-y

        length = math.sqrt(direction[0]**2 + direction[1]**2)*self.BIG_HELI_SPEED**-1
        if length == 0:
            direction = [0, 0]
        else:
            direction = [direction[0]/length, direction[1]/length]

        self.canvas.move(big_helicopter, *direction)

        self.canvas.move(big_helicopter, 0, 1.25)

        if self.big_helicopters[big_helicopter][0].finished() == True:
            self.big_helicopters[big_helicopter][0] = tktimer.Timer(self.BIG_HELI_SHOOT_RATE)
                 
            (x1, y1, x2, y2) = self.canvas.coords(big_helicopter)
            (x, y) = [(x1+x2)/2, (y1+y2)/2]

            (x1, y1, x2, y2) = self.canvas.coords(self.player)
            (px, py) = [(x1+x2)/2, (y1+y2)/2]

            if random.randint(1, 3) == 1:
                direction = [0, 0]
                if random.randint(1, 2) == 1:
                    direction[0] = random.randint(100, self.WIDTH-100)
                if random.randint(1, 2) == 2:
                    direction[1] = random.randint(100, self.WIDTH-100)
                
                self.big_helicopters[big_helicopter][1] = direction

            direction = [0, 0]

            direction[0] = px - x
            direction[1] = py - y

            if abs(direction[0]) > abs(direction[1]):
                if direction[0] > 0:
                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (1, -1)

                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (1, 0)

                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (1, 1)
                else:
                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (-1, 1)

                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (-1, 0)

                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (-1, -1)
            else:
                if direction[1] > 0:
                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (-1, 1)

                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (0, 1)

                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (1, 1)
                else:
                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (-1, -1)

                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (0, -1)

                    enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
                    self.enemy_bullets[enemy_bullet] = (1, -1)

            self.canvas.tag_raise(big_helicopter)

    def restart(self):
        old_window = self.window
        self.__init__(self.root)
        old_window.destroy()
        self.game()
        

if __name__ == "__main__":
    Game().game()