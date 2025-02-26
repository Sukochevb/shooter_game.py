from random import randint
from pygame import *
import time as f

life = 3
window = display.set_mode((700, 500))
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
clock = time.Clock()
font.init()
f1 = font.SysFont(None, 40)
lifes = f1.render('Кол-во жизней:', True, (255, 255, 255))
lost = f1.render('Пропущено:', True, (255, 255, 255))
won = f1.render('Сбито:', True, (255, 255, 255))

sb = 0
pr = 0

class GameSprite(sprite.Sprite):
    def __init__(self, width, height, x, y, speed, im_name):
        super().__init__()
        
        self.image = transform.scale(image.load(im_name), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 25:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x < 615:
            self.rect.x += self.speed
    def fire(self):
        bul1 = Bullet(10, 20, self.rect.centerx - 5, self.rect.top, 15, 'bullet.png')
        bullets.add(bul1)

asteroids = sprite.Group()
k = 0
num_fires = 25

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 650)

class Enemy(GameSprite):
    def update(self):
        global pr
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 650)
            pr += 1
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(70, 50, randint(0,650), 0, randint(1, 5), 'ufo.png')
    monsters.add(monster)
    
for i in range(2):
    asteroid = Asteroid(70, 50, randint(0,650), 0, randint(1, 5), 'asteroid.png')
    asteroids.add(asteroid)
        

game = True
spr1 = Player(50, 70, 350, 400, 10, 'rocket.png')
p_n = False
while game:
    lost = f1.render('Пропущено:' + str(pr), True, (255, 255, 255))
    won = f1.render('Сбито:' + str(sb), True, (255, 255, 255))
    lifes = f1.render('Кол-во жизней:' + str(life), True, (255, 255, 255))
    window.blit(bg, (0, 0))
    window.blit(lost, (0, 0))
    window.blit(won, (0, 40))
    window.blit(lifes, (0, 80))

    spr1.reset()
    spr1.move()
    monsters.draw(window)
    monsters.update()
    asteroids.draw(window)
    asteroids.update()
    bullets.draw(window)
    bullets.update()
    if sprite.spritecollide(spr1, monsters, True) or sprite.spritecollide(spr1, asteroids, True) :
        life -= 1
    if life < 1 or pr > sb:
        losing = f1.render('You lose!', True, (216, 28, 92))
        window.blit(losing, (300, 300))
        display.update()
        f.sleep(2)
        break
    gb = sprite.groupcollide(bullets, asteroids, True, False)
    gc = sprite.groupcollide(bullets, monsters, True, True)

    for a in gc:
        sb += 1
        monster = Enemy(70, 50, randint(0,650), 0, randint(1, 3), 'ufo.png')
        monsters.add(monster)
    if sb == 15:
        winning = f1.render('You win!', True, (216, 28, 92))
        window.blit(winning, (300, 300))
        display.update()
        f.sleep(2)
        break
    if p_n == True:
        t1 = f1.render('Перезарядка:', True, (255, 255, 255))
        window.blit(t1, (0, 400))
        if f.time() - k > 3:
            p_n = False
            num_fires = 1 

    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fires < 15:
                    spr1.fire()
                    num_fires += 1
                    k = f.time()
                else:
                    p_n = True
                
    display.update()
    clock.tick(60)


