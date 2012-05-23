# push the little green box into the big red box (goal) using the white box

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
pygame.display.set_caption('Goal it!')

# set up the colors
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
WHITE   = (255, 255, 255)
YELLOW	= (255, 255, 0)
SILVER  = (192, 192, 192)

# set up small box
SMALLBOXWIDTH = 25
SMALLBOXHEIGHT = 25
smallbox = pygame.Rect(0, 0, SMALLBOXWIDTH, SMALLBOXHEIGHT)
smallbox.centerx = winRect.centerx
smallbox.centery = winRect.centery
smallboxColor = GREEN

# set up player
PLAYERWIDTH = 50
PLAYERHEIGHT = 50 
player = pygame.Rect(300, 100, PLAYERWIDTH, PLAYERHEIGHT)


# set up the goal
GOALWIDTH = SMALLBOXWIDTH + 10
GOALHEIGHT = SMALLBOXHEIGHT + 10
goal = pygame.Rect(0,0, GOALWIDTH, GOALHEIGHT)
goalColor = RED

# place the goal in a random location inside the playing field 
goal.left = random.randint(0, WINDOWWIDTH - GOALWIDTH)
goal.top = random.randint(0, WINDOWHEIGHT - GOALHEIGHT)

# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

boxInGoal = False # game won? 

MOVESPEED = 6

while not boxInGoal:
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
        # if there is a collision with small box, move both
        if player.colliderect(smallbox) and smallbox.left > 0 :
            smallbox.right = player.left
            # if the box is in the goal, you won!
            if smallbox.colliderect(goal) and goal.contains(smallbox):
                boxInGoal = True
            
        # if there is a collision with the goal, make them flush
        if player.colliderect(goal):
            player.left = goal.right
            
    if moveRight and player.right < WINDOWWIDTH:
        player.left += MOVESPEED
        # if there is a collision with small box, move both
        if player.colliderect(smallbox) and smallbox.right < WINDOWHEIGHT:
            smallbox.left = player.right
            # if the box is in the goal, you won!
            if smallbox.colliderect(goal) and goal.contains(smallbox):
                boxInGoal = True
                
        # if there is a collision with the goal, make them flush
        if player.colliderect(goal):
            player.right = goal.left

    if moveUp and player.top  > 0 :
        player.top -= MOVESPEED
        # if there is a collision with small box, move both
        if player.colliderect(smallbox) and smallbox.top > 0 :
            smallbox.bottom=player.top
            # if the box is in the goal, you won!
            if smallbox.colliderect(goal) and goal.contains(smallbox):
                boxInGoal = True
                
        # if there is a collision with the goal, make them flush
        if player.colliderect(goal):
            player.top = goal.bottom

    if moveDown and player.bottom  < WINDOWHEIGHT:
        player.top += MOVESPEED
        # if there is a collision with small box, move both
        if player.colliderect(smallbox) and smallbox.bottom < WINDOWHEIGHT:
            smallbox.top=player.bottom
            # if the box is in the goal, you won!
            if smallbox.colliderect(goal) and goal.contains(smallbox):
                boxInGoal = True
                
        # if there is a collision with the goal, make them flush
        if player.colliderect(goal):
            player.bottom = goal.top
        
    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    # draw the environment
    pygame.draw.rect(windowSurface, goalColor, goal)
    pygame.draw.rect(windowSurface, smallboxColor, smallbox)
    
    # draw the player onto the surface
    pygame.draw.rect(windowSurface, WHITE, player)

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
