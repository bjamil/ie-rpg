import pygame, sys, random
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
winRect = windowSurface.get_rect()
pygame.display.set_caption('My Test')

# set up the colors
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
WHITE   = (255, 255, 255)
YELLOW	= (255, 255, 0)
SILVER  = (192, 192, 192)

# set up pillars
PILLARWIDTH = 25
PILLARHEIGHT = 25
pillar1 = pygame.Rect(0, 0, PILLARWIDTH, PILLARHEIGHT)
pillar1.centerx = winRect.centerx
pillar1.centery = winRect.centery
pillar1Color = GREEN

# set up player
PLAYERWIDTH = 50
PLAYERHEIGHT = 50 
player = pygame.Rect(300, 100, PLAYERWIDTH, PLAYERHEIGHT)

# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6

while True:
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

    # move the player
    if moveLeft and player.left  > 0:
        player.left -= MOVESPEED        
        # if there is a collision, make it flush to the pillar
        if player.colliderect(pillar1):
            player.left = pillar1.right
            pillar1Color = RED
            
    if moveRight and player.right < WINDOWWIDTH:
        player.left += MOVESPEED
        # if there is a collision, make it flush to the pillar
        if player.colliderect(pillar1):
            player.right = pillar1.left
            pillar1Color = BLUE

    if moveUp and player.top  > 0 :
        player.top -= MOVESPEED
        # if there is a collision, make it flush to the pillar
        if player.colliderect(pillar1):
            player.top = pillar1.bottom
            pillar1Color = YELLOW

    if moveDown and player.bottom  < WINDOWHEIGHT:
        player.top += MOVESPEED
        # if there is a collision, make it flush to the pillar
        if player.colliderect(pillar1):
            player.bottom = pillar1.top
            pillar1Color = SILVER
        
    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    # draw the environment
    pygame.draw.rect(windowSurface, pillar1Color, pillar1)
    
    # draw the player onto the surface
    pygame.draw.rect(windowSurface, WHITE, player)

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(40)
