# collect the stars
# get all the red stars

import pygame, sys, random, time
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
winRect = windowSurface.get_rect()
pygame.display.set_caption('Stars mania')


# set up the colors
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
WHITE   = (255, 255, 255)
YELLOW	= (255, 255, 0)
SILVER  = (192, 192, 192)

# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6

# set up player
PLAYERWIDTH = 40
PLAYERHEIGHT = 40 
player = pygame.Rect(300, 100, PLAYERWIDTH, PLAYERHEIGHT)
playerImage = pygame.image.load('playerStar.png')
playerStretchedImage = pygame.transform.scale(playerImage, (PLAYERWIDTH, PLAYERHEIGHT))

# set up red stars
NUMREDSTARS = 20
REDSTARWIDTH = 20
REDSTARHEIGHT = 20

redstarImage = pygame.image.load('redStar.png')
redstarStretchedImage = pygame.transform.scale(redstarImage, (REDSTARWIDTH, REDSTARHEIGHT))
redstars = []
for i in range(NUMREDSTARS):
    redstars.append(pygame.Rect(random.randint(0, WINDOWWIDTH - REDSTARWIDTH), random.randint(0, WINDOWHEIGHT - REDSTARHEIGHT), REDSTARWIDTH, REDSTARHEIGHT))

# set up music
pickUpSound = pygame.mixer.Sound('pickup.wav')
pygame.mixer.music.load('background.mid')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

gameOver = False

while not gameOver:
    # get events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # figure out which key actions were made
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moveRight = False
                moveLeft = True                
            if event.key == K_RIGHT:
                moveLeft = False
                moveRight = True                
            if event.key == K_UP:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN:
                moveUp = False
                moveDown = True

        if event.type == KEYUP:
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False

            if event.key == ord('m'):
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying

    # move the player
    if moveLeft and player.left  > 0:
        player.left -= MOVESPEED        
            
    if moveRight and player.right < WINDOWWIDTH:
        player.left += MOVESPEED
        
    if moveUp and player.top  > 0 :
        player.top -= MOVESPEED
        
    if moveDown and player.bottom  < WINDOWHEIGHT:
        player.top += MOVESPEED
        
    # draw the black background onto the surface
    windowSurface.fill(BLACK)
    
    # draw the player onto the surface
    windowSurface.blit(playerStretchedImage, player)

    # check if the player has intersected any redstars
    for star in redstars[:]:
        if player.colliderect(star):
            redstars.remove(star)
            player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
            playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
            if musicPlaying:
                pickUpSound.play()
        

    # draw the environment
    for star in redstars:
        windowSurface.blit(redstarStretchedImage, star)

    if len(redstars)==0:
        gameOver = True
        
    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(40)

# box is in goal, you win!
basicFont = pygame.font.SysFont(None, 48)
text = basicFont.render('You Win!!' , True, YELLOW, None)
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery


# draw the text onto the surface
windowSurface.blit(text, textRect)

# draw the window onto the screen
pygame.display.update()

time.sleep(1)

pygame.quit()
sys.exit()
                    
