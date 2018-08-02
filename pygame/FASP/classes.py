import pygame
from random import randint as rand

def makelist(*arg):
    if isinstance(arg, tuple):
        return list(arg)
    else:
        return [arg]

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getPoint(self):
        return (self.x,self.y)

class RenderGroup(pygame.sprite.RenderPlain):
    
    def __init__(self):
        self.list = []
        pygame.sprite.RenderPlain.__init__(self)
    
    def add(self, *sprites):
        pygame.sprite.RenderPlain.add(self, *sprites)
        self.list.extend(makelist(*sprites))
        
    def remove(self, *sprites):
        pygame.sprite.RenderPlain.remove(self, *sprites)
        for item in makelist(*sprites):
            if self.list.__contains__(item):
                self.list.remove(item)
        return True
        
    def draw(self):
        count = 0
        for item in self.list:
            if item.OOB():
                if self.remove(item):
                    count += 1
            else:
                item.update()
                item.draw()
        return count
        
class PlanetGroup(RenderGroup):

    def __init__(self):
        RenderGroup.__init__(self)

    def remove(self, *sprites):
        flag = False
        for planet in makelist(*sprites):
            if planet.safe():
                flag = True
        RenderGroup.remove(self, *sprites)
        return flag


class StarField:
    
    def __init__(self, starSize, speed, numStars, dims, screen):
        self.starSize = starSize
        self.speed = speed
        self.numStars = numStars
        self.dims = dims
        self.stars = []
        for i in range(numStars):
            x = rand(0,dims[0]-1)
            y = rand(0,dims[1]-1)
            self.stars.append(Point(x,y))
        self.screen = screen
    
    def update(self):
        for i in range(len(self.stars)):
            star = self.stars[i]
            star.y += self.speed
            if star.y > self.dims[1]:
                star.y %= self.dims[1]
                star.x = rand(0,self.dims[0]-1)
            
    def draw(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, (255,255,255), star.getPoint(), self.starSize)
            
class JSprite(pygame.sprite.Sprite):
    
    def __init__(self, fileName, screen, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(fileName)
        self.rect = JRect(self.image.get_rect(), self.image)
        self.setPos(pos)
        self.screen = screen
        
    def setPos(self, pos):
        self.pos = pos
        self.rect.topleft = (pos.x, pos.y)
    
    def draw(self):
        self.screen.blit(self.image, self.pos.getPoint())
        #pygame.draw.rect(self.screen, (255,255,255), self.rect, 1)

    def getCenter(self):
        return Point(self.pos.x + self.rect.width // 2, self.pos.y + self.rect.height // 2)

    def setCenter(self, center):
        self.setPos(Point(center.x - self.rect.width // 2, center.y - self.rect.height // 2))
        
class JRect(pygame.Rect):
    
    def __init__(self, rect, image):
        pygame.Rect.__init__(self, rect)
        self.image = image
        
    def colliderect(self, other):
        rect = self.clip(other)
        if rect.width == 0:
            return False
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                if self.notTransparent(x,y) and other.notTransparent(x,y):
                    return True
        return False
             
    def notTransparent(self, x, y):
        return self.image.get_at((x-self.left, y-self.top))[3] != 0
                    
class Ship(JSprite):
    
    def __init__(self, fileName, screenDims, screen):
        JSprite.__init__(self, fileName, screen, Point(0,0))
        imageDims = (self.image.get_rect().size[0] // 2, self.image.get_rect().size[1] // 2)
        self.image = pygame.transform.scale(self.image, imageDims)
        self.rect = JRect(self.image.get_rect(), self.image)
        self.setPos(Point((screenDims[0] - imageDims[0]) // 2, (screenDims[1] - imageDims[1]) // 2))
                
    def shoot(self, fileName):
        x = self.pos.x + self.image.get_rect().size[0] // 2
        return Bullet(fileName, Point(x, self.pos.y), 20, self.screen)
        
    def shootBackwards(self, fileName):
        x = self.pos.x + self.image.get_rect().size[0] // 2
        return ReverseBullet(fileName, Point(x, self.pos.y), 20, self.screen)
    
    def moveX(self, dist):
        self.pos.x += dist
        self.rect.left += dist
        
    def moveY(self, dist):
        self.pos.y += dist
        self.rect.top += dist
        
class Bullet(JSprite):
    
    def __init__(self, fileName, pos, speed, screen):
        JSprite.__init__(self, fileName, screen, pos)
        self.speed = speed
        self.pos.x -= self.rect.width // 2
        self.hasShield = True
        
    def update(self):
        self.pos.y -= self.speed
        self.rect.top -= self.speed
            
    def OOB(self):
        return self.pos.y < -20
        
class ReverseBullet(Bullet):
    
    def __init__(self, fileName, pos, speed, screen):
        Bullet.__init__(self, fileName, pos, -speed, screen)
        self.image = pygame.transform.flip(self.image, False, True)

class Asteroid(JSprite):
    
    def __init__(self, fileName, xMax, speed, rotateSpeed, screen):
        JSprite.__init__(self, fileName, screen, Point(0,0))
        self.setPos(Point(rand(1,xMax-self.image.get_rect().size[0]), -self.image.get_rect().size[1]))
        self.speed= speed
        self.rotateSpeed = rotateSpeed
        self.backupImage = self.image
        self.angle = 0
        
    def update(self):
        self.pos.y += self.speed
        self.rect.top += self.speed
        self.rotate()
        
    def rotate(self):
        self.angle += self.rotateSpeed
        center = self.getCenter()
        self.image = pygame.transform.rotate(self.backupImage, self.angle)
        self.rect = JRect(self.image.get_rect(), self.image)
        self.setCenter(center)

                
    def OOB(self):
        return self.pos.y > self.screen.get_size()[1]

class ReverseAsteroid(Asteroid):

    def __init__(self, fileName, xMax, speed, rotateSpeed, screen):
        Asteroid.__init__(self, fileName, xMax, speed, rotateSpeed, screen)
        self.setPos(Point(self.pos.x, screen.get_size()[1]))
        self.speed = -self.speed

class Planet(JSprite):

    numPics = 3
    pics = []

    def __init__(self, screen, screenDims):
        JSprite.__init__(self, "p1.png", screen, Point(0,0))
        self.firstImage = Planet.pics[rand(0, Planet.numPics - 1)]
        self.image = self.firstImage
        self.rect = self.image.get_rect()
        self.setPos(Point(rand(0, screenDims[0]-self.rect.width), -self.rect.height))
        self.speed = rand(5,10)
        self.setNewShrinkSpeed(screenDims[1])
        self.shrinking = True

    def setNewShrinkSpeed(self, screenHeight):
        avgDist = screenHeight * 4 // 3
        dist = rand(avgDist - 100, avgDist + 100)
        frames = dist / self.speed
        self.shrinkSpeedX = int(self.rect.width / frames)
        self.shrinkSpeedY = int(self.rect.height / frames)

    def update(self):
        self.setPos(Point(self.pos.x, self.pos.y + self.speed))
        if self.shrinking:
            self.shrink()

    def shrink(self):
        center = self.getCenter()
        newWidth = self.rect.width - self.shrinkSpeedX
        newHeight = self.rect.height - self.shrinkSpeedY
        self.image = pygame.transform.scale(self.firstImage, (newWidth, newHeight))
        self.rect = self.image.get_rect()
        self.setCenter(center)

    def OOB(self):
        return ( self.safe() or
                self.rect.width < self.shrinkSpeedX or
                self.rect.height < self.shrinkSpeedY)

    def safe(self):
        return self.pos.y > self.screen.get_size()[1]



#Load pics
for x in range(Planet.numPics):
    Planet.pics.append(pygame.image.load("p" + str(x+1) + ".png"))
for pic in Planet.pics:
    if pic.get_rect().width > 256:
        newPic = pygame.transform.scale(pic, (256,256))
        Planet.pics.remove(pic)
        Planet.pics.append(newPic)
