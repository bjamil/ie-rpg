import pygame, removable
from constants import * 

class Boulders(removable.Removable):
    """ the boulders """

    def __init__(self, images, width, height, posx = 0, posy = 0):

        # call the parent constructor
        removable.Removable.__init__(self, images, width, height)

        # set position
        self.rect.x = posx
        self.rect.y = posy
 
