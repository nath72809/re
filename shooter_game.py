from pygame import *
from random import randint
from time import time as timer
image_b = 'bullet.png'
lost = 0
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, y, x, player_image, player_x, player_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (x, y))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   def dead(self):
       if ship.rect.x == monster.rect.x and ship.rect.y == monster.rect.y:
            global lost 
            lost += 1
   def fire(self):
        bullet = Bullet(30, 40, image_b, self.rect.centerx - 20, self.rect.top, randint(10,25))
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Enemy(GameSprite):
   def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.speed = randint(1,5)
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 5
            global lost
            lost += 1
   def kik(self):
       self.speed = randint(1,5)
       self.rect.x = randint(80, win_width - 80)
       self.rect.y = 5
       global lost
       lost += 2
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
ship = Player(60, 60, 'rocket.png', 5, win_height - 80, 4)

game = True
finish = False
clock = time.Clock()
FPS = 60

score = 0
i = 1
font.init()
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN!', True, (255, 255, 255))
lose = font.render('YOU LOSE!', True, (255, 255, 255))
monsters = sprite.Group()
bullets = sprite.Group()
piys = sprite.Group()
piys.add()
for i in range(5):
            
            monster = Enemy(60, 60,'ufo.png', randint(1, 495), 5, randint(1,4))
            monsters.add(monster)
            time.delay(50)
            i += 1
#музыка
relod = font.render('relode', True, (255, 255, 255))
relode = False
bull = 0
last_timer = 1
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
tim = True
kick = mixer.Sound('fire.ogg')
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
  
    if finish != True:
        
        keys = key.get_pressed()
        if keys[K_SPACE] and bull != 20:
            kick.play()
            ship.fire()
            bull += 1
        if bull >= 20 and relode == False:
            relode = True
            last_timer = timer()
            tim = True
        window.blit(background,(0, 0))
        ship.update()
        monsters.update()
        bullets.update()
        bullets.draw(window)
        ship.dead()

        ship.reset()
        monster.reset()
        monsters.draw(window)
        
        if tim == True:
            timee = timer()
            if last_timer < 180:
                win.blit(relod, (250, 10))

            else:
                bull = 0
                tim = False
                relode = False
        if sprite.spritecollide(ship, monsters, True):
            finish = True
        for i in monsters:
            if sprite.spritecollide(i, bullets, True):
                score += 1
                i.kill()
                monster = Enemy(60, 60, 'ufo.png', randint(1, 495), 5, randint(1,4))
                monsters.add(monster)
        if finish == True:
            finish = False
            for i in monsters:
                i.kill()
            for i in bullets:
                i.kill()
            bull = 0
            score = 0
            lost = 0
            for i in range(5):
            
                monster = Enemy(60, 60,'ufo.png', randint(1, 495), 5, randint(1,4))
                monsters.add(monster)
                time.delay(50)
                i += 1


    los = font.render('пропущено:' + str(lost), True, (255, 255, 255))
    scoress = font.render('счёт:' + str(score), True, (255, 255, 255))
       #Ситуация "Проигрыш"
    window.blit(los, (10, 40))
    window.blit(scoress, (10, 10))

    
    if lost == 10:
        finish = True
        window.blit(lose, (ship.rect.x, ship.rect.y))
        
        #Ситуация "Выигрыш"
    if score >= 100:
        finish = True
        window.blit(win, (ship.rect.x, ship.rect.y))
        
 
    display.update()
    clock.tick(FPS)