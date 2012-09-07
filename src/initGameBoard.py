# collect the stars
# get all the red stars

import pygame, sys, random, time, tree, player, infoBox, fairy, laser, boulders, player2
from pygame.locals import *
from constants import * 


# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
shootBeam = False
talk = -1

# set up info box switch
boxOn = False
moreInfo = False # i.e. go to next page

# lower numbers = faster ; it's more delay than speed 
MOVESPEED = 6
BEAMSPEED = 3
beams = [] # the active laser beams 

breakable = []
breakableRects = []

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
    global shootBeam
    
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
##                if event.key == K_SPACE:
##                    shootBeam = True

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False
                if event.key == K_SPACE:
                    shootBeam = True
        
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
        


def addBeam():
    """ adds a laser beam starting from link's current position """
    global beams, shootBeam

    # the beam direction is whatever direction link was facing when this fxn was called
    # if no direction was being faced, then the default direction is top
    
    if moveLeft:
        direction = LEFT
    elif moveRight:
        direction = RIGHT
    elif moveDown:
        direction = DOWN
    else:
        direction = UP
        
    beams.append(laser.Laser(screen,link.rect.centerx-2 ,link.rect.top+20, direction))
    shootBeam = False
    print len(beams) , 'beams'

def moveBeams():
    """ moves all active beams. deletes all inactive ones """
    global beams

    remove = []
    for i, beam in enumerate(beams):
        beam.moveBeam( MOVESPEED , collidable, breakable )
        if not beam.active:
            remove.append(i)
            print i 

    # remove all inactive beams
    beams = [beam for i, beam in enumerate(beams) if i not in remove]

def updateBreakable():
    """ removes broken/inactive obects from the breakable list """
    global breakable, collidable
    
    remove = []
    for i, item in enumerate(breakable):
        if item.removed:
            collidable.remove(item)
            remove.append(i)
    # remove all broken objects
    breakable = [item for i, item in enumerate(breakable) if i not in remove]
            

def drawBeams():
    """ draw all active beams """
    for beam in beams:
        beam.draw(screen)


def drawTrees():
    """ draw all trees """
    for tree in alltrees:
        tree.draw(screen)


def movelink():
    """ move the link """
    global link

    if moveLeft:
        link.moveLeft(BEAMSPEED, collidable)
    if moveRight:
        link.moveRight(BEAMSPEED, collidable)
    if moveUp:
        link.moveUp(BEAMSPEED, collidable)
    if moveDown:
        link.moveDown(BEAMSPEED, collidable)

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

#linkImage = pygame.image.load('tmp-Link.png')
#linkStretchedImage = pygame.transform.scale(linkImage, (PLAYERWIDTH, PLAYERHEIGHT))
linkImage = pygame.image.load('tmp-ML1.png')

#link = player.Player(screen, linkImage, PLAYERWIDTH, PLAYERHEIGHT, WINDOWWIDTH/2, WINDOWHEIGHT - PLAYERHEIGHT)

linkFW = 132/4
linkFH = 144/4
link = player2.Player2(screen, linkImage, PLAYERWIDTH, PLAYERHEIGHT, linkFW, linkFH, WINDOWWIDTH/2, WINDOWHEIGHT - PLAYERHEIGHT)


# set up environment
collidable = []
actionable = [] # actionable objects
actionableRects = [] # rects of actionable objects 

# Background image
bg = pygame.Rect(0,0, WINDOWWIDTH, WINDOWHEIGHT)
bgImage = pygame.image.load('tmp-BG.png')
bgStretchedImage = pygame.transform.scale(bgImage, (WINDOWWIDTH, WINDOWHEIGHT))

# create boulders
BOULDERWIDTH = 216
BOULDERHEIGHT = 40
BOULDERPOSX = WINDOWWIDTH/2 - BOULDERWIDTH/2 +16 # center it
BOULDERPOSY = WINDOWHEIGHT/2 - BOULDERHEIGHT +16

boulderImages = [pygame.image.load('tmp-boulders-00.png'), pygame.image.load('tmp-boulders-01.png'), pygame.image.load('tmp-boulders-02.png'), pygame.image.load('tmp-boulders-03.png')]
boulders = boulders.Boulders(boulderImages, BOULDERWIDTH, BOULDERHEIGHT, BOULDERPOSX, BOULDERPOSY)
collidable.append(boulders.rect)
breakable.append(boulders)

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
info.setText("Hello Traveler! \nPress the Space-bar button to shoot at the boulders and clear your path!\n\nOnce upon a time in a land far far away, there lived a prince who owned a dinosaur. Yes, that's right. A dinosaur. Not a nice herbivore either, but a big, huge, human-hungry T-Rex. Or so they say. Kind of makes you curious doesn't it? Why don't you go check it out? Just follow the leftward road -- If you're brave enough, of course.")
info.setImage(fairyImage)




# set up music
#pickUpSound = pygame.mixer.Sound('pickup.wav')
#pygame.mixer.music.load('background.mid')
#pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

gameOver = False

while not gameOver:

    # get all events
    getEvents(pygame.event.get())

    # add any beams that need to be added
    if shootBeam:
        addBeam()

    # animate all beams
    moveBeams()
    updateBreakable() # update the collidable list 

    # animate link 
    movelink()
    
    # draw the background onto the surface
    screen.blit(bgStretchedImage, bg)


    # draw  link onto the surface
 #   screen.blit(linkStretchedImage, link)
#    screen.blit(linkImage, link)
    link.draw(screen)

    
    # draw the trees onto the surface
    drawTrees()

    # draw the removable objects onto the surface
    boulders.draw(screen)
            

    # draw the fairy
    missy.draw(screen)

    # draw the beams 
    drawBeams()        


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
    mainClock.tick(60)


time.sleep(1)

pygame.quit()
sys.exit()
                    
