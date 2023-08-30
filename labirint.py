from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self,picture,x,y,w,h):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        okno.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self,picture,x,y,w,h,x_speed,y_speed):
        GameSprite.__init__(self,picture,x,y,w,h)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        platform_toched = sprite.spritecollide(self,barriers,False)
        if self.x_speed > 0:
            for p in platform_toched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed<0:
            for p in platform_toched:
                self.rect.left= max(self.rect.left, p.rect.right)
        if hero.rect.y <= win_h-80 and hero.y_speed >0 or hero.rect.y >= 0 and hero.y_speed<0:
            self.rect.y += self.y_speed
        platform_toched = sprite.spritecollide(self,barriers,False)
        if self.y_speed > 0:
            for p in platform_toched:
                self.y_speed = 0

                if p.rect.top <self.rect.bottom:
                    self.rect.bottom = p.rect.top 
        elif self.y_speed<0:
            for p in platform_toched:    
                self.y_speed = 0
                self.rect.top = max(self.rect.top,p.rect.bottom)   
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.right,self.rect.centery,15,20,15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def __init__(self,picture,x,y,w,h,player_speed):
        GameSprite.__init__(self,picture,x,y,w,h)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed    
        if self.rect.x > win_w+10:
            self.kill()

class Enemy(GameSprite):
    side = "left"
    def __init__(self,picture,x,y,w,h,player_speed):
        GameSprite.__init__(self,picture,x,y,w,h)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_w - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

win_w = 700
win_h = 500
okno = display.set_mode((win_w, win_h))
display.set_caption('АF')
barriers = sprite.Group()
bullets = sprite.Group()
enemis = sprite.Group()
wall1 = GameSprite('walll.png',win_w / 2 - win_w / 3 ,win_h / 2,300,50)
wall2 = GameSprite('walll.png',370,100,50,400)
barriers.add(wall1)
barriers.add(wall2)

hero = Player('hero.png',5,win_h - 80 ,80,80,0,0)
enemy = Enemy('enemy.png',600,190,80,80,5)
enemis.add(enemy)

final = GameSprite('finish.jpg',600, 430,80,80)
run = True
finish = False
while run:
    time.delay(50)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                hero.x_speed = -5
            elif e.key == K_RIGHT:
                hero.x_speed = 5
            elif e.key == K_DOWN:
                hero.y_speed = 5
            elif e.key == K_UP:
                hero.y_speed = -5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                hero.x_speed = 0
            elif e.key == K_RIGHT:
                hero.x_speed = 0
            elif e.key == K_DOWN:
                hero.y_speed = 0
            elif e.key == K_UP:
                hero.y_speed = 0
            if e.key ==K_SPACE:
                hero.fire()
    if not finish:
        okno.fill((219,210,223))
        hero.update()
        bullets.update()
        barriers.draw(okno)
        bullets.draw(okno)
        hero.reset()
        enemis.draw(okno)
        final.reset()
        sprite.groupcollide(enemis,bullets,True,True)
        enemis.update()
        enemis.draw(okno)
        sprite.groupcollide(bullets,barriers,True,False)
        if  sprite.spritecollide(hero,enemis,False):
            finish = True
            img = image.load('thumb1.jpg')
            d = img.get_width() // img.get_height()
            okno.fill((255,255,255))
            okno.blit(transform.scale(img,(win_h*d,win_h)),(90,0))
        if  sprite.collide_rect(hero,final):
            finish = True
            img = image.load('thumb.jpg')
            d = img.get_width() // img.get_height()
            okno.fill((255,255,255))
            okno.blit(transform.scale(img,(win_h*d,win_h)),(90,0))
    display.update()