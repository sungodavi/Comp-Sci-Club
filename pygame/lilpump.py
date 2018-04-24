import pygame
from pygame.locals import *
from time import sleep

pygame.init()

dims = (500,500)
screen = pygame.display.set_mode(dims)


x = 250
y = 250

while True:
    sleep(1/30)
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    if pressed[K_UP]:
        x -= 5
    if pressed[K_DOWN]:
        x += 5
    if pressed[K_LEFT]:
        y -= 5
    if pressed[K_RIGHT]:
        y += 5
        
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255,255,255), (x,y), 100)
    pygame.display.flip()
    