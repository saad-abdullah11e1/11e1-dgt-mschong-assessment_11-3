import tkinter as tk
import random
import time
import math
from . import tktimer
import PIL

class Game:
    # Width and height of the window
    WIDTH = 600
    HEIGHT = 600

    # ms / frame
    GAME_SPEED = 10

    # Player Constants
    SPEED = 3
    FRICTION = 0.1
    ACCELERATION = 0.1

    # Speed at which the bullet travels
    BULLET_SPEED = 10

    # Speed to enemy bullets
    ENEMY_BULLET_SPEED = 2

    # Speed of enemies
    ENEMY_SPEED = 1.5

    # seconds between each shot of the shooters
    SHOOTER_RATE = 3

    # Big Helicopter Constants
    BIG_HELI_SHOOT_RATE = 5
    BIG_HELI_SPEED = 1
    BIG_HELI_MAX_HEALTH = 25

    def __init__(self, root: tk.Tk, name):
        """Set up all the variables for the game."""

        self.quit = False

        self.root = root

        self.name = name

        self.game_speed = self.GAME_SPEED

        # Make new window
        self.window = tk.Toplevel(self.root)
        self.window.focus()

        self.window.title("Game")

        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background='white')

        self.canvas.pack()

        self.player_image = PIL.Image.open("snake.jpeg")
        self.player_image = self.player_image.resize((30, 30))
        self.player_image = PIL.ImageTk.PhotoImage(self.player_image)
        self.player = self.canvas.create_image(self.WIDTH/2, self.HEIGHT/2, image=self.player_image, anchor="nw")

        # self.player = self.canvas.create_rectangle(self.WIDTH/2, self.HEIGHT/2, self.WIDTH/2+25, self.HEIGHT/2+25, fill="#00FF00", outline='#00FF00')
        
        # List of enemies
        self.enemies = []

        self.enemy_image = PIL.Image.open("snake.jpeg")
        self.enemy_image = self.enemy_image.resize((30, 30))
        self.enemy_image = PIL.ImageTk.PhotoImage(self.enemy_image)

        # If an enemy is behind the player it gets "lost" and continues in the direction it was
        # travelling before till it exits the screen. 
        self.lost_enemy_directions = {}

        # Dictionary of all Big Helicopters contains their ID, timer and health
        self.big_helicopters = {}

        self.big_heli_image = PIL.Image.open("snake.jpeg")
        self.big_heli_image = self.big_heli_image.resize((50, 75))
        self.big_heli_image = PIL.ImageTk.PhotoImage(self.big_heli_image)

        # Dictionary of enemy bullets contains thier direction.
        self.enemy_bullets = {}

        # List of player bullets
        self.bullets = []

        # Players velocity [x, y]
        self.velocity = [0, 0]

        # Dictionary of shooters, contains ID, Timer
        self.shooters = {}

        self.shooter_image = PIL.Image.open("snake.jpeg")
        self.shooter_image = self.shooter_image.resize((30, 30))
        self.shooter_image = PIL.ImageTk.PhotoImage(self.shooter_image)

        self.score_label = self.canvas.create_text(self.WIDTH/2, 50, text="Score: 0", font=("Arial", 24), fill="black")

        # Since Tk is event based it doesn't support polling a key press (is_pressed("up"))
        # This means if the player holds the key the character will only move once
        # These functions will update each keys state on the self.keyboard dictionary
        self.window.bind("<KeyPress>", self.key_pressed)
        self.window.bind("<KeyRelease>", self.key_released)

        self.window.bind("<space>", self.shoot)

        self.keyboard = {}

    def game(self):
        # Timers for enemy spawning
        self.enemy_spawn_timer = tktimer.Timer(10)
        self.big_helicopter_spawn_timer = tktimer.Timer(60)
        self.shooter_spawn_timer = tktimer.Timer(30)

        # Score
        self.score = 0

        # The time it takes for each enemy to spawn
        self.enemy_spawn = 1
        self.big_helicopter_spawn = 25
        self.shooter_spawn = 5

        self.game_loop()

    def game_loop(self):
        # Score is tied to time survived in seconds
        self.score += self.game_speed/1000

        self.canvas.itemconfig(self.score_label, text=f"Score: {(self.score):.0f}")
        self.canvas.tag_raise(self.score_label)

        if self.quit == True:
            self.quit_game()
            return
        
        # Whenever the timer finsihes, spawn the respective enemy and restart the timer
        if self.enemy_spawn_timer.finished() == True:
            x = random.randint(0, self.WIDTH-50)

            self.enemies.append(self.canvas.create_image(x, -25, image=self.enemy_image, anchor="nw"))
            self.enemy_spawn_timer = tktimer.Timer(self.enemy_spawn)

        if self.big_helicopter_spawn_timer.finished() == True:
            x = random.randint(0, self.WIDTH-50)

            big_helicopter = self.canvas.create_image(x, -25, image=self.big_heli_image, anchor="nw")
            self.big_helicopters[big_helicopter] = [tktimer.Timer(self.BIG_HELI_SHOOT_RATE), [x, self.HEIGHT/4], self.BIG_HELI_MAX_HEALTH]

            self.big_helicopter_spawn_timer = tktimer.Timer(self.big_helicopter_spawn)

            # When the Big Helicopter spawns start making the enemies spawn faster to increase difficulty
            self.enemy_spawn = 0.75
            self.shooter_spawn -= 0.25

        if self.shooter_spawn_timer.finished() == True:
            x = random.randint(0, self.WIDTH-50)

            shooter = self.canvas.create_image(x, -25, image=self.shooter_image, anchor="nw")
            self.shooters[shooter] = tktimer.Timer(self.SHOOTER_RATE)

            self.shooter_spawn_timer = tktimer.Timer(self.shooter_spawn)


        self.player_physics()

        self.bullet_physics()

        for enemy in self.enemies:
            self.enemy_ai(enemy)
        
        for big_helicopter in list(self.big_helicopters.keys()):
            self.big_helicopter_ai(big_helicopter)
        
        for shooter in list(self.shooters.keys()):
            self.shooter_ai(shooter)
        
        for bullet in self.enemy_bullets.keys():
            # Move the enemy bullets
            direction = [self.enemy_bullets[bullet][0]*self.ENEMY_BULLET_SPEED, self.enemy_bullets[bullet][1]*self.ENEMY_BULLET_SPEED]

            self.canvas.move(bullet, *direction)

        # self.window.update()
        self.window.after(self.game_speed, self.game_loop)

    def quit_game(self):
        self.score = round(self.score)

        # Read Highscores and write new highscore if there is one
        with open("shooter_highscore.txt") as f:
            name, highscore = f.read().split(':')

        if int(highscore) < len(self.score):
            with open("shooter_highscore.txt", "w") as f:
                highscore = f"{len(self.score)}"
                name = self.name
                f.write(self.name+":"+highscore)

        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2, text=f"Game Over\nScore: {int(self.score)}\nHighscore: {highscore} by {name}", font=("Arial", 36), fill="Red")
        
        # Space to Restart
        self.window.bind('<space>', lambda event: self.restart())

    def move(self, x, y):
        """Add velocity to player."""
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
        """Handle Bullet Physics. For each bullet and each enemy, check if they collide if so delete them or reduce their health."""
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, -self.BULLET_SPEED)
            
            for enemy in self.enemies:
                enemy_box = self.canvas.bbox(enemy)
                bullet_box = self.canvas.bbox(bullet)

                if self.is_colliding(enemy_box, bullet_box) == True:
                    self.canvas.delete(enemy)
                    self.enemies.remove(enemy)

                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    
                    break

        for bullet in self.bullets:    
            for big_heli in list(self.big_helicopters.keys()):
                enemy_box = self.canvas.bbox(big_heli)
                bullet_box = self.canvas.bbox(bullet)

                if self.is_colliding(enemy_box, bullet_box) == True:
                    self.big_helicopters[big_heli][2] -= 1

                    if self.big_helicopters[big_heli][2] <= 0:
                        self.canvas.delete(big_heli)
                        self.big_helicopters.pop(big_heli)

                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    
                    break
                if self.is_colliding(self.canvas.bbox(big_heli), (0, 0, self.WIDTH, self.HEIGHT)) == False:
                    self.canvas.delete(big_heli)
                    self.big_helicopters.pop(big_heli)

        for bullet in self.bullets:    
            for shooter in list(self.shooters.keys()):
                enemy_box = self.canvas.bbox(shooter)
                bullet_box = self.canvas.bbox(bullet)

                if self.is_colliding(enemy_box, bullet_box) == True:
                    self.canvas.delete(shooter)
                    self.shooters.pop(shooter)

                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)

                    break

    def is_colliding(self, a, b):
        """Check if two boxes are colliding."""
        (ax1, ay1, ax2, ay2) = a
        (bx1, by1, bx2, by2) = b

        if ax2 < bx1 or bx2 < ax1:
            return False
    
        if ay2 < by1 or by2 < ay1:
            return False
    
        return True

    def player_input(self):
        """Handle player inpute."""
        velocity = [0, 0]
        if self.is_pressed('Up'):
            velocity[1] += -1
        if self.is_pressed('Down'):
            velocity[1] += 1
        if self.is_pressed('Left'):
            velocity[0] += -1
        if self.is_pressed('Right'):
            velocity[0] += 1

        # Normalise velocity. 
        # If velocity = (0, 1) then speed is 1
        # If velocity = (1, 1) then the player will be moving at a speed of sqrt(2)
        # Normalising ensures that the player moves at the saem speed in all directions
        if velocity != [0, 0]:
            magnitude = math.sqrt(velocity[0]**2 + velocity[1]**2)
            velocity[0] /= magnitude
            velocity[1] /= magnitude

        self.move(*velocity)
        return velocity
        

    def player_physics(self):
        """Handle player physics, collision with border, and death."""
        if self.player_input()[0] == 0:
            self.velocity[0] *= 1-self.FRICTION
        if self.player_input()[1] == 0:
            self.velocity[1] *= 1-self.FRICTION

        self.canvas.move(self.player, self.velocity[0], self.velocity[1])

        player_box = self.canvas.bbox(self.player)

        (x1, y1, x2, y2) = self.canvas.bbox(self.player)

        if x1 < 0:
            self.canvas.move(self.player, -x1, 0)
        if x2 > self.WIDTH:
            self.canvas.move(self.player, (self.WIDTH) - x2, 0)
        if y1 < 0:
            self.canvas.move(self.player, 0, -y1)
        if y2 > self.HEIGHT:
            self.canvas.move(self.player, 0, (self.HEIGHT) - y2)

        for enemy in self.enemies:
            enemy_box = self.canvas.bbox(enemy)
            player_box = self.canvas.bbox(self.player)

            if self.is_colliding(player_box, enemy_box) == True:
                self.quit = True

        for bullet in self.enemy_bullets.keys():
            bullet_box = self.canvas.bbox(bullet)
            player_box = self.canvas.bbox(self.player)

            if self.is_colliding(player_box, bullet_box) == True:
                self.quit = True

        for big_helicopter in self.big_helicopters.keys():
            heli_box = self.canvas.bbox(big_helicopter)
            player_box = self.canvas.bbox(self.player)

            if self.is_colliding(player_box, heli_box) == True:
                self.quit = True
        
    def shoot(self, event):
        """Spawn a bullet."""
        (x1, y1, x2, y2) = self.canvas.bbox(self.player)

        center = [(x1+x2)/2, (y1+y2)/2]

        bullet = self.canvas.create_rectangle(center[0]-2, center[1]-10, center[0]+2, center[1]+10, fill="#000000", outline="#000000")

        self.bullets.append(bullet)

    def enemy_ai(self, enemy):
        """Enemy AI. Move toward the player.""" 
        """If enemy falls behind player than it is lost and will continue moving in the same direction till it falls out of the screen"""
        if enemy in self.lost_enemy_directions:
            self.canvas.move(enemy, *self.lost_enemy_directions[enemy])
            return

        (x1, y1, x2, y2) = self.canvas.bbox(self.player)
        player_coords = [(x1+x2)/2, (y1+y2)/2]

        (x1, y1, x2, y2) = self.canvas.bbox(enemy)
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

        enemy_box = self.canvas.bbox(enemy)

        (x1, y1, x2, y2) = self.canvas.bbox(enemy)

        if x1 < 0 or x2 > self.WIDTH  or y2 > self.HEIGHT:
            self.canvas.delete(enemy)
            self.enemies.remove(enemy)

    def big_helicopter_ai(self, big_helicopter):
        """Big Helicopter AI. Every interval shoot out three bullets towards the player.
          1/3 chance of moving to a random position on the screen. Also slowly drifts down."""
        (x1, y1, x2, y2) = self.canvas.bbox(big_helicopter)
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
                 
            (x1, y1, x2, y2) = self.canvas.bbox(big_helicopter)
            (x, y) = [(x1+x2)/2, (y1+y2)/2]

            (x1, y1, x2, y2) = self.canvas.bbox(self.player)
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

            (x1, y1, x2, y2) = self.canvas.bbox(big_helicopter)

            if x1 < 0 or x2 > self.WIDTH or y2 > self.HEIGHT:
                    self.canvas.delete(big_helicopter)
                    self.big_helicopters.pop(big_helicopter)

    def shooter_ai(self, shooter):
        """Shooter AI. Shoot bullets towards the player. Slowly drift down."""
        self.canvas.move(shooter, 0, 0.25)

        if self.shooters[shooter].finished() == True:
            self.shooters[shooter] = tktimer.Timer(self.SHOOTER_RATE)

            (x1, y1, x2, y2) = self.canvas.bbox(shooter)
            (x, y) = [(x1+x2)/2, (y1+y2)/2]

            (x1, y1, x2, y2) = self.canvas.bbox(self.player)
            (px, py) = [(x1+x2)/2, (y1+y2)/2]

            direction = [px - x, py - y]

            if direction != [0, 0]:
                magnitude = math.sqrt(direction[0]**2 + direction[1]**2)
                direction[0] /= magnitude
                direction[1] /= magnitude

            enemy_bullet = self.canvas.create_rectangle(x-7.5, y-7.5, x+7.5, y+7.5, fill="#FF8000", outline="#FF0000")
            self.enemy_bullets[enemy_bullet] = direction   

            (x1, y1, x2, y2) = self.canvas.bbox(shooter)

            if x1 < 0 or x2 > self.WIDTH or y2 > self.HEIGHT:
                self.canvas.delete(shooter)
                self.shooters.pop(shooter)

    def restart(self):
        """Restart Game"""
        old_window = self.window
        self.__init__(self.root, self.name)
        old_window.destroy()
        self.game()
        

if __name__ == "__main__":
    Game().game()