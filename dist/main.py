from pygame import * # modules
from random import *

mixer.init() # inits
init()

lost = 0

bulletsy = sprite.Group()

class GameSprite(sprite.Sprite): # Game Sprite Class
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__() # loading sprite init
        self.image = transform.scale(image.load(player_image), (65, 65)) # loading sprite
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

class LeftRight(GameSprite): # basic dumb Sprite
    direction = "left" # setting directions
    def __init__(self, Yv, player_image, player_x, player_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, player_speed) # loading sprite init
        self.Yspeed = Yv
    def update(self):
        global lost
        self.rect.y += self.Yspeed
        if self.rect.x <= 0: # changing directions
            self.direction = "right"
        if self.rect.x >= w - 65:
            self.direction = "left"
 
        if self.direction == "left": # moving
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        if self.rect.y >= h:
            lost += 1
            self.rect.y = 0
            print(lost)
            self.speed = randint(1,15)
            self.Yspeed = randint(1,15)

        mw.blit(self.image, (self.rect.x, self.rect.y)) # adding sprite to the screen

class Bullet(GameSprite): # basic-est dumbass Sprite
    def update(self):
        self.rect.y += self.speed # self-exlainatory
        if self.rect.y < h:
            self.kill()

class Player(GameSprite): # sigma gigachad smart Sprite class
    def update(self):
        keys = key.get_pressed() # key presses reaction
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            dire = 'l'
        if keys[K_RIGHT] and self.rect.x < w - 65:
            self.rect.x += self.speed
            dire = 'r'
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
            dire = 'u'
        if keys[K_DOWN] and self.rect.y < h - 65:
            self.rect.y += self.speed
            dire = 'd'

        mw.blit(self.image, (self.rect.x, self.rect.y)) # adding sprite to the screen
    def fire(self):
        print("fire in the hole ☺")
        bullety = Bullet(bullet, self.rect.centerx, self.rect.top, 5)
        bulletsy.add(bullety)

bg = 'bg.jpg' # characters
hero = 'загружено.png'
enemy = 'загружено.jfif'
platform = ''
bullet = 'загружено (1).png'

run = True # variables
w = 800
h = 600
dire = 'l'

clock = time.Clock() # clock
FPS=60 # FPS
mw = display.set_mode((w, h)) # creating window
display.set_caption("Story of Undertale: the game") # setting caption

bg = transform.scale(image.load("bg.jpg"),(w, h)) # creating characters
char = Player(hero, 0, 0, 5)
enemee = LeftRight(randint(1,9), enemy, 0, 0, randint(1,9))
enemee1 = LeftRight(randint(1,9), enemy, 0, 65, randint(1,9))
enemee2 = LeftRight(randint(1,9), enemy, 0, 130, randint(1,9))
enemee3 = LeftRight(randint(1,9), enemy, 0, 195, randint(1,9))
enemee4 = LeftRight(randint(1,9), enemy, 0, 260, randint(1,9))
enemee5 = LeftRight(randint(1,9), enemy, 0, 260, randint(1,9))
enemee6 = LeftRight(randint(1,9), enemy, 0, 260, randint(1,9))
enemee7 = LeftRight(randint(1,9), enemy, 0, 260, randint(1,9))

while run: # main loop
    for e in event.get(): # event check
        if e.type == QUIT: # quitting system
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_LSHIFT:
                char.fire()
    bulletsy.update()
    sl = font.Font("dos2000-ru-en.ttf", 16).render("lost: " + str(lost),True,[0,0,0])
    slo = font.Font("dos2000-ru-en.ttf", 16).render("lost: " + str(lost),True,[255,255,255])
    sl2 = font.Font("dos2000-ru-en.ttf", 16).render("Score: ",True,[0,0,0])
    sl2o = font.Font("dos2000-ru-en.ttf", 16).render("Score: ",True,[255,255,255])
    mw.blit(bg, (0, 0)) # adding characters to the screen
    char.update()
    enemee.update()
    enemee1.update()
    enemee2.update()
    enemee3.update()
    enemee4.update()
    enemee5.update()
    enemee6.update()
    enemee7.update()
    mw.blit(slo, (16, 256))
    mw.blit(slo, (16, 254))
    mw.blit(slo, (15, 255))
    mw.blit(slo, (17, 255))
    mw.blit(sl, (16, 255))
    mw.blit(sl2o, (16, 256+16))
    mw.blit(sl2o, (16, 254+16))
    mw.blit(sl2o, (15, 255+16))
    mw.blit(sl2o, (17, 255+16))
    mw.blit(sl2, (16, 255+16))
    display.update() # updating display
    clock.tick(FPS) # clock ticks