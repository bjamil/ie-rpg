import pygame
from constants import *

class Removable:
    """ an object that can be removed from the game if the player hits
        him enough times """

    def __init__(self, images, width, height):
        # images = a list of images. The first indicates the base
        #           image for this object. The system cycles through each
        #           of the rest every time the player hits this object
        #           at the final hit, this object disappears

        # create a rectangle for it
        self.rect = pygame.Rect(0,0, width, height)

        # set its image
        self.images = images
        self.image = pygame.transform.scale(images[0], (width, height))

        # set active
        self.removed = False

        # define how many hits have been made & how many are needed
        self.hits = 0
        self.counter = -1
        self.totalHits = len(images)
        
    def hit(self):
        " perform a hit to this object "
        self.hits += 1
        if self.hits == self.totalHits:
            self.removed = True
        print "bam!"

    def draw(self, screen):
        " draws the object to the given screen if it is not removed "
        if not self.removed:
            screen.blit(self.images[self.hits], self.rect)
    
    def setPos(self, x, y):
        " sets the position of the object "
        self.rect.x = x
        self.rect.y = y
    


        
