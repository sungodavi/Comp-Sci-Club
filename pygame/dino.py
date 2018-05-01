import pygame
from pygame import Rect
from pygame.locals import *
from pygame.sprite import Sprite
from time import sleep
import random
import sys

WHITE = 255, 255, 255
BLACK = 0, 0, 0
BACKGROUND = 0,0,0

class Dino(Sprite):
    def __init__(self, pos, screenDims, jump_velocity=15, gravity=1, width=40, height=80, color=WHITE):
        super().__init__()
        self.width = width
        self.height = height
        self.gravity = gravity
        self.screenDims = Rect((0, 0), screenDims)
        self.image = pygame.image.load('Dino.png')
        scale = self.height / self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (int(scale * self.image.get_rect().width), self.height))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
        self.jump_velocity = jump_velocity
        self.jumping = False
        self.t = 0
        
    def update(self):
        if self.jumping:
            self.rect.y -= self.jump_velocity - self.gravity * self.t
            if self.rect.bottom > self.screenDims.bottom:
                self.rect.y = self.screenDims.bottom - self.height
                self.jumping = False
        self.t += 1
                
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.t = 0
        
        
class Block(Sprite):
    def __init__(self, pos, velocity=10, size=40, color=WHITE):
        super().__init__()
        self.size = size
        self.velocity = velocity
        
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
    def update(self):
        self.rect.x -= self.velocity
        
        
if __name__ == '__main__':
    pygame.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    
    screen_width = 700
    screen_height = 400
    screen = pygame.display.set_mode([screen_width, screen_height])
    block_prob = 0.05
    
    dino = Dino((100, 320), (screen_width, screen_height))
    sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    sprites.add(dino)
    buffer_start = 0
    COOLDOWN = 25
    time = 0
    flag = True
    while flag:
        time += 1
        sleep(1/45)
        if time - buffer_start > COOLDOWN and random.random() < block_prob:
            block = Block((660,360))
            sprites.add(block)
            blocks.add(block)
            
            buffer_start = time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(pygame.quit())
        pressed = pygame.key.get_pressed()
        
        if pressed[K_UP] or pressed[K_SPACE]:
            dino.jump()
        if pressed[K_ESCAPE]:
            pygame.quit()
            sys.exit()
            
        if len(pygame.sprite.spritecollide(dino,blocks,False)) > 0:
            break
        
           
        sprites.update()
        screen.fill(BACKGROUND)
        text = font.render("Score: " + str(time), True, WHITE)
        screen.blit(text, (0,0))
        sprites.draw(screen)
        pygame.display.flip()
    
    
    while not pressed[K_ESCAPE]:
        pygame.display.flip()
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pressed[K_ESCAPE] = False        
    sys.exit(pygame.quit())
    
        
        