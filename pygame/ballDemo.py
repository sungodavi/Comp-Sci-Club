import sys, pygame
import os
from time import sleep
from pygame.locals import *
from pygame import Rect

bullet = pygame.image.load("ball.png")
bullet = pygame.transform.scale(bullet, (50, 50))

class Bullet:
    def __init__(self, pos, speed, screenDims):
        self.speed = speed
        self.rect = Rect(pos, (20, 20))
        self.screenRect = Rect((0, 0), screenDims)
        
    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]
    
    def isValid(self):
        return self.rect.bottom < self.screenRect.bottom and self.rect.top > 0
        
    def draw(self, screen):
        screen.blit(bullet, self.rect)
        
pygame.init()

size = 1080, 720
speed = 15
black = 0, 0, 0
width, height = 300, 300

screen = pygame.display.set_mode(size)

ball = pygame.image.load("lilpump.png")
ballrect = ball.get_rect()
print(ballrect)
bullets = []
counter = 0
mod = 5

while True:
    counter += 1
    sleep(1/30)
    events = pygame.event.get()
    pressed = pygame.key.get_pressed()
    if pressed[K_ESCAPE]:
        pygame.quit()
        break
    if pressed[K_w]:
         ballrect = ballrect.move([0, -speed])
    if pressed[K_s]:
        ballrect = ballrect.move([0, speed])
    if pressed[K_a]:
        ballrect = ballrect.move([-speed, 0])
    if pressed[K_d]:
        ballrect = ballrect.move([speed, 0])
    if pressed[K_UP] and counter % mod == 0:
        bullets.append(Bullet((ballrect.centerx, ballrect.top), (0, -speed * 2), size))
    if pressed[K_DOWN] and counter % mod == 0:
        bullets.append(Bullet((ballrect.centerx, ballrect.bottom), (0, speed * 2), size))
    if pressed[K_LEFT] and counter % mod == 0:
        bullets.append(Bullet((ballrect.left, ballrect.centery), (-speed * 2, 0), size))
    if pressed[K_RIGHT] and counter % mod == 0:
        bullets.append(Bullet((ballrect.right, ballrect.centery), (speed * 2, 0), size))
    
    screen.fill(black)
    screen.blit(ball, ballrect)
    for data in bullets:
        data.move()
        if not data.isValid():
            del data
        else:
            data.draw(screen)
            pygame.display.flip()