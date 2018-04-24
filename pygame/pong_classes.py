import pygame
from pygame import Rect
from random import randint as rand
#from math import abs

class Puck:
    def __init__(self, pos, screenDims):
        self.rect = Rect(pos, (20, 150))
        self.screenRect = Rect((0,0), screenDims)
        self.goingUp, self.goingDown = False, False
        
    def canGoUp(self):
        return self.rect.top > 0
    
    def canGoDown(self):
        return self.rect.bottom < self.screenRect.bottom
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect)
        
    def move(self, num):
        self.rect.centery += num
        
    def update(self):
        if self.goingUp:
            self.rect.x
    
class Ball:
    def __init__(self, center, screenDims):
        self.rect = Rect((0,0), (20,20))
        self.rect.center = center
        self.screenRect = Rect((0,0), screenDims)
        self.dx = rand(4,10)
        self.dy = rand(4,10)
        if rand(0,1):
            self.dx = -self.dx
        if rand(0,1):
            self.dy = -self.dy
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), self.rect.center, self.rect.width)
        
    def update(self, lefty, righty):
        if self.rect.colliderect(lefty.rect):
            self.dx = abs(self.dx)
        
        if self.rect.colliderect(righty.rect):
            self.dx = -abs(self.dx)
        
        if self.rect.top <= 0:
            self.dy = abs(self.dy)
            
        if self.rect.bottom >= self.screenRect.bottom:
            self.dy = -abs(self.dy)
        
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
        return not self.rect.colliderect(self.screenRect)