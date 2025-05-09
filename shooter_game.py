from pygame import *
from random import randint


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
text1 = font.Font(None, 72)
text2= font.Font(None, 36)

win_game = text1.render('YOU WIN!', True, (0, 180, 0))
lose_game = text1.render('YOU LOSE!', True, (180, 0, 0))


img_back = "galaxy.jpg" 
img_hero = "rocket.png" 
img_alien1 = "ufo.png"
img_bullet = "bullet.png"



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
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
    def fire(self): 
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500

lost = 0
fired = 0
max_lost = 3
goal = 5

display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

aliens = sprite.Group()
for i in range(1, 6):
    alien1 = Enemy(img_alien1, randint(80, win_height - 80), -40, 80, 50, randint(4, 8))
    aliens.add(alien1)

bullets = sprite.Group()

finish = False
run = True


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    
    if not finish:
        window.blit(background,(0,0))

        lose = text2.render('Пропущенно: ' + str(lost), 1, (255, 255, 255))
        win = text2.render('Счёт:' + str(fired), 1, (255, 255, 255))
        window.blit(lose, (10, 20))
        window.blit(win, (600, 20))

        ship.update()
        ship.reset()
        aliens.update()
        bullets.update()
        aliens.draw(window)
        bullets.draw(window)    
        if sprite.spritecollide(ship, aliens, False) or lost >= max_lost:
            finish = True
            window.blit(lose_game, (200, 250))
        
        if fired >= goal:
            finish = True
            window.blit(win_game, (200, 250))
        collide = sprite.groupcollide(aliens, bullets, True, True)

        for i in collide:
            fired += 1
            alien1 = Enemy(img_alien1, randint(80, win_height - 80), -40, 80, 50, randint(4, 8))
            aliens.add(alien1)
        display.update()

    else:
        finish = False
        fired = 0
        lost = 0
        for i in bullets:
            i.kill()
        for i in aliens:
            i.kill()
        
        time.delay(3000)

        for i in range(1, 6):
            alien1 = Enemy(img_alien1, randint(80, win_height - 80), -40, 80, 50, randint(4, 8))
            aliens.add(alien1)

    time.delay(50)