#Asteroids 1.2.5
#Parker Gowans

#Imports
from superwires import games
import random
import math


#Global Info
games.init(screen_width = 640, screen_height = 480, fps = 60)







#Classes

class Asteroid(games.Sprite):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL : games.load_image("images/Asteroid_small.png"),
                      MEDIUM : games.load_image("images/Asteroid_med.png"),
                      LARGE : games.load_image("images/Asteroid_big.png")}
    SPEED = 2

    def __init__(self, x, y, size):
        super(Asteroid,self).__init__(image = Asteroid.images[size],
                                      x = x,
                                      y = y,
                                      dx = random.choice([1, -1]) * Asteroid.SPEED * random.random()/size,
                                      dy = random.choice([1, -1]) * Asteroid.SPEED * random.random()/size)
        self.size = size

    def update(self):
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width
            
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height


class Ship(games.Sprite):
    image = games.load_image("images/spaceship.png")
    sound = games.load_sound("sounds/thrusters.wav")
    ROTATION_STEP = 7
    VELOCITY_STEP = .03
    MISSILE_DELAY = 25

    def __init__(self):
        super(Ship, self).__init__(image = Ship.image,
                                   x = games.screen.width/2,
                                   y = games.screen.height/2)
        self.missile_wait = 0

    def update(self):
        if games.keyboard.is_pressed(games.K_a) or games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.ROTATION_STEP
            
        if games.keyboard.is_pressed(games.K_d) or games.keyboard.is_pressed(games.K_RIGHT):
            self.angle+= Ship.ROTATION_STEP
            
        if games.keyboard.is_pressed(games.K_w) or games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()
            angle = self.angle * math.pi/180
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)
            
        if self.missile_wait >0:
            self.missile_wait -= 1
            
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY
            
            # This is copied code look into to better ways of doing it
            #Wrap the ship around the screen
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width
            
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height


class Missile(games.Sprite):
    image = games.load_image("images/missile.PNG", transparent = True
                             )
    sound = games.load_sound("sounds/missileExplosion.wav")
    BUFFER = 20
    VELOCITY_FACTOR = 10
    LIFETIME = 40

    def __init__(self, ship_x, ship_y, ship_angle):
        Missile.sound.play()
        angle = ship_angle * math.pi / 180



        # Calculate missile's starting position
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)

        x = ship_x + buffer_x
        y = ship_y + buffer_y

        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)
        super(Missile, self).__init__(image = Missile.image,
                                                        x = x,
                                                        y = y,
                                                        dx = dx,
                                                        dy = dy)

        self.lifetime = Missile.LIFETIME
        self.angle = Missile.angle
        
    def update(self):
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width
            
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
        
        self.lifetime -= 1
        if self.lifetime ==0:
            self.destroy()
        






#Main
def main():
    
    #Load Data
    bg_img = games.load_image("images/background.jpg")



    #Create Objects
    for i in range(8):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
        new_asteroid = Asteroid(x = x, y = y , size = size)
        games.screen.add(new_asteroid)

    #Create Ship
    player = Ship()
    #shot = Missile(100, 100, 0)



    #Draw Objects
    games.screen.background = bg_img
    games.screen.add(player)
    #games.screen.add(shot)



    #Game Setup





    #Start main loop
    games.screen.mainloop()


main()
        

