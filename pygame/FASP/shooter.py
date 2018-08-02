import pygame
from pygame.locals import *
from classes import *
from time import sleep
from random import randint as rand

pygame.font.init()
frameRate = 30

dims = (1080,1920)
screen = pygame.display.set_mode(dims, FULLSCREEN)
smallfont = pygame.font.SysFont("consolas", 30)
bigfont = pygame.font.SysFont("consolas", 60)
clock = pygame.time.Clock()

def play():
    starFields = [StarField(1,5,120,dims,screen), StarField(3,7,30,dims,screen), StarField(4,20,5,dims,screen)]
    ship = Ship("ship.png", dims, screen)
    blueBullets = RenderGroup()
    redBullets = RenderGroup()
    asteroids = RenderGroup()
    planets = PlanetGroup()
    score, asteroidCounter, planetCounter = 0, 0, 0
    lives, randomFrameGap = 3, 90
    reverse = False
    ms1, ms2, ms3 = False, False, False

    crashFlag = False

    while lives > 0:
        clock.tick(frameRate)

        #Process Input
        for event in pygame.event.get():
            if hasattr(event, "key"):
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_LALT:
                        blueBullets.add(ship.shoot("bluebullet.png"))
                        score -= 1
                    elif event.key == K_SPACE:
                        redBullets.add(ship.shoot("redbullet.png"))
                        if reverse:
                            redBullets.add(ship.shootBackwards("redbullet.png"))
                        score -= 1
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                    elif event.key == K_q:
                        crashFlag = True
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            ship.moveY(-15)
        if pressed[K_DOWN]:
            ship.moveY(15)
        if pressed[K_LEFT]:
            ship.moveX(-20)
        if pressed[K_RIGHT]:
            ship.moveX(20)

        #Check for milestones
        
        if score >= 500 and not reverse:
            reverse = True
            lives += 1
            
        if score >= 250 and not ms1:
            ms1 = True
            lives += 1
        
        elif score >= 1000 and not ms2:
            ms2 = True
            lives += 1
        
        elif score >= 1500 and not ms2:
            ms2 = True
            lives += 1
        
        #Randomly add asteroid and planets
        
        

        if rand(1, int(randomFrameGap) + 10) == 1:
            asteroids.add(Asteroid("a1.png",dims[0],rand(5,10), rand(5,10), screen))
        
        if reverse and rand(1, int(randomFrameGap) + 10) == 1:
            asteroids.add(ReverseAsteroid("a1.png",dims[0],rand(5,10), rand(5,10), screen))
        
        if rand(1, int(randomFrameGap) * 6 + 30) == 1:
            planets.add(Planet(screen, dims))

        randomFrameGap *= .9984608586


        #Collision Checks

        for asteroid in pygame.sprite.spritecollide(ship, asteroids, True):
            print("boom!")
            asteroids.remove(asteroid)
            lives -= 1

        for asteroid, bullet in pygame.sprite.groupcollide(asteroids, redBullets, False, False).items():
            bullet = bullet[0]
            asteroids.remove(asteroid)
            if bullet.hasShield:
                bullet.hasShield = False
            else:
                redBullets.remove(bullet)
            score += 5

        for planet, bullet in pygame.sprite.groupcollide(planets, redBullets, False, False).items():
            bullet = bullet[0]
            planets.remove(planet)
            if bullet.hasShield:
                bullet.hasShield = False
            else:
                redBullets.remove(bullet)
            score -= 5

        for planet, bullet in pygame.sprite.groupcollide(planets, blueBullets, False, False).items():
            if planet.shrinking:
                planet.shrinking = False
                blueBullets.remove(bullet)

        #Draw output to screen

        if not crashFlag:
            screen.fill((0, 0, 0))

        for field in starFields:
            field.update()
            field.draw()

        score += planets.draw() * 40

        blueBullets.draw()

        redBullets.draw()

        lives -= asteroids.draw()

        ship.draw()

        scoreText = bigfont.render("SCORE: " + str(score), True, (255,255,255))
        textRect = scoreText.get_rect()
        textRect.topright = (dims[0], 0)
        screen.blit(scoreText, textRect)

        livesDesc = smallfont.render("Lives:", True, (255,255,255))
        livesText = bigfont.render(str(lives), True, (71,218,255))
        livesDescRect = livesDesc.get_rect()
        livesTextRect = livesText.get_rect()
        livesTextRect.topleft = (0, livesDescRect.bottom + 5)
        screen.blit(livesDesc, (0,0))
        screen.blit(livesText, livesTextRect)

        pygame.display.flip()

        #rect = ship.rect
        #print(str(rect.top) + " " + str(rect.right) + " " + str(rect.bottom) + " " + str(rect.left))


play()

#Display game-over instructions
gameOverText = bigfont.render("GAME OVER", True, (255,255,255), (0,0,0))
gameOverRect = gameOverText.get_rect()
gameOverRect.center = (dims[0] // 2, dims[1] // 2)
screen.blit(gameOverText, gameOverRect)
pygame.display.flip()
sleep(2)

endText1 = bigfont.render("Press SPACE to Play Again", True, (255,255,255), (0,0,0))
endText2 = bigfont.render("Press ESC to Exit", True, (255,255,255), (0,0,0))
endRect2 = endText2.get_rect()
endRect2.center = (dims[0] // 2, dims[1] // 2)
screen.blit(endText2, endRect2)
endRect1 = endText1.get_rect()
endRect1.center = (endRect2.centerx, endRect2.centery - endRect2.height)
screen.blit(endText1, endRect1)
pygame.display.flip()

while True:
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    if pressed[K_ESCAPE]:
        pygame.quit()
    elif pressed[K_SPACE]:
        play()




        