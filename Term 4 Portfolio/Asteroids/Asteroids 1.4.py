#Asteroids 1.4
#Parker Gowans

#Imports
from superwires import games
import random
import math


#Global Info
games.init(screen_width = 640, screen_height = 480, fps = 60)







#Classes
class Wrapper(games.Sprite):
    def update(self):
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width
            
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
            
    def die(self):
        self.destroy()

class Collider(Wrapper):
    def update(self):
        """Check for overlapping sprites."""
        super(Collider, self).update()
        
    #check if missile overlaps any other object
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()
    def die(self):
        #Create explosion
        new_explosion = Explosion(obj_x = self.x, obj_y = self.y)
        #Add to screen
        games.screen.add(new_explosion)
        self.destroy()

    
class Asteroid(Wrapper):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL : games.load_image("images/Asteroid_small.png"),
                      MEDIUM : games.load_image("images/Asteroid_med.png"),
                      LARGE : games.load_image("images/Asteroid_big.png")}
    SPEED = 2
    SPAWN = 2

    def __init__(self, x, y, size):
        super(Asteroid,self).__init__(image = Asteroid.images[size],
                                      x = x,
                                      y = y,
                                      dx = random.choice([1, -1]) * Asteroid.SPEED * random.random()/size,
                                      dy = random.choice([1, -1]) * Asteroid.SPEED * random.random()/size)
        self.size = size

       
    def die(self):
        # If asteroid isn't small, replace with two smaller asteroids
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(x = self.x,
                                        y = self.y,
                                        size = self.size - 1)
                games.screen.add(new_asteroid)
        self.destroy()


class Ship(Collider):
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

        super(Ship, self).update()
            


class Missile(Collider):
    image = games.load_image("images/missile.PNG", transparent = True)
    sound = games.load_sound("sounds/missileExplosion.wav")
    BUFFER = 60
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
        self.angle = ship_angle
        
    def update(self):
        super(Missile, self).update()
        #If lifetime is up, destroy the missile
        self.lifetime -= 1
        if self.lifetime ==0:
            self.destroy()
        
class Explosion(games.Animation):
    sound = games.load_sound("sounds/shipExplosion.wav")
    exp_images = ["images/explosion1.bmp",
                        "images/explosion2.bmp",
                        "images/explosion3.bmp",
                        "images/explosion4.bmp",
                        "images/explosion5.bmp"]

    def __init__(self, obj_x, obj_y):
        super(Explosion, self).__init__(images = Explosion.exp_images,
                                        x = obj_x, y = obj_y,
                                        repeat_interval = 4,
                                        n_repeats = 1,
                                        is_collideable = False)
        Explosion.sound.play()


#Main
def main():
    
    #Load Data
    bg_img = games.load_image("images/background.jpg")



    #Create Objects
    for i in range(5):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
        new_asteroid = Asteroid(x = x, y = y , size = size)
        games.screen.add(new_asteroid)

    #Create Ship
    player = Ship()
    shot = Missile(100, 100, 0)



    #Draw Objects
    games.screen.background = bg_img
    games.screen.add(player)
    games.screen.add(shot)



    #Game Setup





    #Start main loop
    games.screen.mainloop()


main()
        

