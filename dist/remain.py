from pygame import *
from random import randint
 
w = 700
h = 500

hp = 100

# фоновая музыка
# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()

#шрифты и надписи
font.init()
font2 = font.Font("dos2000-ru-en.ttf", 16)

#нам нужны такие картинки:
img_back = 'bg.jpg' #фон игры
img_hero = 'загружено.png' #герой
img_enemy = 'загружено.jfif' # враг
img_bullet = 'загружено (1).png' #пуля
img_bonus = 'erm.png' #Бонус

#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

score = 0 #сбито кораблей
lost = 0 #пропущено кораблей

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
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

 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        #bullet = Bullet(img_bullet, self.rect.x, self.rect.y , 15, 20, 15)
        bullets.add(bullet)


#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
    direction = "left" # setting directions
    def __init__(self, Yv, player_image, player_x, player_y, player_w, player_h, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, player_w, player_h, player_speed) # loading sprite init
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

        window.blit(self.image, (self.rect.x, self.rect.y)) # adding sprite to the screen

    def dong(self):
        self.rect.y = 0
        self.speed = randint(1,15)
        self.Yspeed = randint(1,15)

#класс спрайта-врага  
class left_right(GameSprite):
   #движение врага
    direction = "left" # setting directions
    def __init__(self, Yv, player_image, player_x, player_y, player_w, player_h, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, player_w, player_h, player_speed) # loading sprite init
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

        window.blit(self.image, (self.rect.x, self.rect.y)) # adding sprite to the screen


#класс спрайта-пули  
class Bullet(GameSprite):
   #движение врага
    def update(self):
        self.rect.y -= self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()

#lost=0

#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 60, 60, 10)
 
monsters = sprite.Group()
for i in range(1, 8):
    monster = Enemy(randint(1, 20), img_enemy, randint(80, win_width - 80), -40, 60, 60, randint(1, 20))
    monsters.add(monster)

bonuses = sprite.Group()
bonus = left_right(15, img_bonus, randint(80, win_width - 80), -40, 70, 70, randint(1, 20))
bonuses.add(bonus)

bullets = sprite.Group()

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна

clock = time.Clock() # clock
FPS=60 # FPS

while run:
   #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False 

           #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE or e.key == K_LSHIFT or e.key == K_RSHIFT:
                #fire_sound.play()
                ship.fire()
                
    if not finish:
        #обновляем фон
        window.blit(background,(0,0)) 

        #пишем текст на экране
        text_o = font2.render("Счет: " + str(score),  True, (255, 255, 255))
        window.blit(text_o, (9, 255))
        window.blit(text_o, (11, 255))
        window.blit(text_o, (10, 256))
        window.blit(text_o, (10, 254))
        text = font2.render("Счет: " + str(score),  True, (0, 0, 0))
        window.blit(text, (10, 255))
        text_lose_o = font2.render("Пропущено: " + str(lost), True, (255, 255, 255))
        window.blit(text_lose_o, (9, 255+16))
        window.blit(text_lose_o, (11, 255+16))
        window.blit(text_lose_o, (10, 256+16))
        window.blit(text_lose_o, (10, 254+16))
        text_lose = font2.render("Пропущено: " + str(lost), True, (0, 0, 0))
        window.blit(text_lose, (10, 255+16))
        text_lose_o = font2.render("Здоровье: " + str(hp), True, (255, 255, 255))
        window.blit(text_lose_o, (9, 255+32))
        window.blit(text_lose_o, (11, 255+32))
        window.blit(text_lose_o, (10, 256+32))
        window.blit(text_lose_o, (10, 254+32))
        text_lose = font2.render("Здоровье: " + str(hp), True, (0, 0, 0))
        window.blit(text_lose, (10, 255+32))

       #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        bonuses.update()
        
       #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        display.update()

        #шрифты и надписи
        font.init()
        win = font2.render('YOU WIN!', True, (255, 0, 255))
        lose = font2.render('YOU LOSE!', True, (255, 0, 0))

        if sprite.spritecollide(ship, monsters, False):
            hp -= 1
            if hp < 0:
                finish = True
                window.blit(lose, (255, 255))

        if sprite.spritecollide(ship, bonuses, False):
            hp += 1

        collides = sprite.groupcollide(bullets, monsters, True, False)
        for c in collides:
            score += 10
            monster.dong()
         
    #цикл срабатывает каждые 0.05 секунд
    clock.tick(FPS)