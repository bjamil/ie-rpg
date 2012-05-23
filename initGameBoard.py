# collect the stars
# get all the red stars

import pygame, sys, random, time, tree, player, infoBox, fairy
from pygame.locals import *



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
talk = -1

# set up info box switch
boxOn = False
moreInfo = False # i.e. go to next page

MOVESPEED = 6


def getEvents(events):
    "get all user events"

    global moveLeft
    global moveRight
    global moveUp
    global moveDown 
    global talk
    global gameOver
    global musicPlaying
    global boxOn
    global moreInfo 
    
    for event in events:
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            gameOver = True

        # if you're not in a dialogue box sequence
        if not boxOn:
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
                if event.key == K_LSHIFT:
                    # check if there is a collision with an actionable item
                    talk = link.hasCollided(actionableRects)
                    if talk >= 0:
                        actionable[talk].active = True
                        boxOn = True
                if event.key == ord('i'):
                    boxOn = True

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False
        
        # finish the dialogue box sequence before moving on 
        else:
            if event.type == KEYDOWN:
                if event.key == ord('x'):
                    boxOn = False
                if event.key == K_SPACE or event.key == K_RIGHT:
                    moreInfo = True

        # you can turn the music on or off at any time 
        if event.type == KEYUP and event.key == ord('m'):
            if musicPlaying:
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play(-1, 0.0)
            musicPlaying = not musicPlaying
        


def movelink():
    " move the link "
    global link

    if moveLeft:
        link.moveLeft(MOVESPEED, collidable)
    if moveRight:
        link.moveRight(MOVESPEED, collidable)
    if moveUp:
        link.moveUp(MOVESPEED, collidable)
    if moveDown:
        link.moveDown(MOVESPEED, collidable)


# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 600
WINDOWHEIGHT = 500
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
winRect = screen.get_rect()
pygame.display.set_caption('Fairy Tales - Chapter 0')

# set up link
PLAYERWIDTH = 36
PLAYERHEIGHT = 44 
#link = pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT - linkHEIGHT, linkWIDTH, linkHEIGHT)
linkImage = pygame.image.load('tmp-Link.png')
linkStretchedImage = pygame.transform.scale(linkImage, (PLAYERWIDTH, PLAYERHEIGHT))

link = player.Player(screen, linkImage, PLAYERWIDTH, PLAYERHEIGHT, WINDOWWIDTH/2, WINDOWHEIGHT - PLAYERHEIGHT)

# set up environment
collidable = []
actionable = [] # actionable objects
actionableRects = [] # rects of actionable objects 

# Background image
bg = pygame.Rect(0,0, WINDOWWIDTH, WINDOWHEIGHT)
bgImage = pygame.image.load('tmp-BG.png')
bgStretchedImage = pygame.transform.scale(bgImage, (WINDOWWIDTH, WINDOWHEIGHT))

# Trees 
TREEWIDTH = 108
TREEHEIGHT = 108
TREESTUMPWIDTH = 54
TREESTUMPHEIGHT = 36

NUMTREES = 12

treeImage = pygame.image.load('tmp-tree.png')

alltrees = []
#render = pygame.sprite.OrderedUpdates()

for i in range((NUMTREES - 3 )/2):
    # append trees on one side of image
    t = tree.Tree(treeImage, TREEWIDTH, TREEHEIGHT, TREESTUMPWIDTH, TREESTUMPHEIGHT)
    t.setPos((TREEWIDTH/2)*i , (TREEHEIGHT/2)*i)
    alltrees.append(t)
    collidable.append(t.stump)
    #render.add(t)

    # append trees on the other side of the image
    t = tree.Tree(treeImage, TREEWIDTH, TREEHEIGHT, TREESTUMPWIDTH, TREESTUMPHEIGHT)
    t.setPos(WINDOWWIDTH - (TREEWIDTH/2)*(i+1) , (TREEHEIGHT/2)*i)
    alltrees.append(t)
    collidable.append(t.stump)
    #render.add(t)

# append tree in the middle 
t = tree.Tree(treeImage, TREEWIDTH, TREEHEIGHT, TREESTUMPWIDTH, TREESTUMPHEIGHT)
t.setPos(WINDOWWIDTH/2 -TREEWIDTH/4, 0)
alltrees.append(t)
collidable.append(t.stump)
#render.add(t)

#collidable.extend(alltrees)

# create fairy
FAIRYWIDTH = 36
FAIRYHEIGHT = 36
FAIRYPOSX = WINDOWWIDTH - FAIRYWIDTH*2
FAIRYPOSY = WINDOWHEIGHT/2

fairyImage = pygame.image.load('tmp-fairy.png')
missy = fairy.Fairy(fairyImage, FAIRYWIDTH, FAIRYHEIGHT, FAIRYPOSX, FAIRYPOSY)
collidable.append(missy)
actionable.append(missy)
actionableRects.append(missy.rect)



DIALOGUEBOXWIDTH = 532
DIALOGUEBOXHEIGHT = 108
DIALOGUEBOXOPACITY = 0.5
DIALOGUEBOXPICWIDTH = 72
DIALOGUEBOXPICHEIGHT = 72
DIALOGUEBOXTXTWIDTH = 406
DIALOGUEBOXTXTHEIGHT = 72
DIALOGUEBOXBOTTOMPADDING = 10

info = infoBox.InfoBox(screen, BLUE, DIALOGUEBOXWIDTH, DIALOGUEBOXHEIGHT, DIALOGUEBOXBOTTOMPADDING)
info.setText("1.once upon a time in a land far away \n2. there lived \n3.a \n4.girl\n5.\n6.\n7.\n8.")
info.setImage(fairyImage)




# set up music
#pickUpSound = pygame.mixer.Sound('pickup.wav')
#pygame.mixer.music.load('background.mid')
#pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

gameOver = False

while not gameOver:
    
    getEvents(pygame.event.get())
    movelink()
    
    # draw the background onto the surface
    screen.blit(bgStretchedImage, bg)

    # draw the link onto the surface
    screen.blit(linkStretchedImage, link)
            

    # draw the trees onto the surface
    for tree in alltrees:
        tree.draw(screen)

    # draw the fairy
    missy.draw(screen)

    # draw the info box
    if boxOn:
        if moreInfo:
            if info.hasNextPage():
                info.nextPage(screen)
                moreInfo = False # turn off switch so that page is only changed when user wants it to be
            else:
                # close the box if no more pages exist 
                info.close()
                moreInfo= False
                boxOn = False
        else:
            info.draw(screen)
        

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(50)


time.sleep(1)

pygame.quit()
sys.exit()
                    
