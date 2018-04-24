import pygame
from pygame.locals import *
from pong_classes import *
from time import sleep

#initialize the window with given dimensions
pygame.init()
dims = (750,500)
screen = pygame.display.set_mode(dims)
pygame.display.set_caption("Pong")

#Initialize our three objects
lefty = Puck((50,175), dims)
righty = Puck((680, 175), dims)
ball = Ball((375,250), dims)

lScore = 0
rScore = 0

isPaused = False
font = pygame.font.Font(None, 100)

while True:
    sleep(1/30)
    
    #Get input from keyboard
    events = pygame.event.get()
    pressed = pygame.key.get_pressed()
    
    
    #Check for pausing
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                isPaused = not isPaused
    if isPaused:
        continue
    
    #Move pucks based on input
    if pressed[K_ESCAPE]:
        pygame.quit()
    if pressed[K_UP] and righty.canGoUp():
        righty.move(-3)
    if pressed[K_DOWN] and righty.canGoDown():
        righty.move(3)
    if pressed[K_w] and lefty.canGoUp():
        lefty.move(-3)
    if pressed[K_s] and lefty.canGoDown():
        lefty.move(3)
        
    #Move ball
    if ball.update(lefty, righty):
        sleep(1)
        if ball.rect.centerx > dims[0] // 2:
            rScore += 1
        else:
            lScore += 1
        
        ball = Ball((375,250), dims)
    
    
    #Draw everything to screen
    screen.fill((0,0,0))
    
    lefty.draw(screen)
    righty.draw(screen)
    ball.draw(screen)
    
    #Draw score
    lText = font.render(str(lScore), True, (0,0,255))
    rText = font.render(str(rScore), True, (255,0,0))
    
    lRect = lText.get_rect()
    rRect = rText.get_rect()
    
    lRect.left = 10
    lRect.top = 10
    rRect.right = dims[0] - 10
    rRect.top = 10
    
    screen.blit(lText, lRect)
    screen.blit(rText, rRect)
    
    pygame.display.flip()
    

