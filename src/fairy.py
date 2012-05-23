import pygame, actionable, infoBox

class Fairy(actionable.Actionable):
    """ the fairy """

    def __init__(self, image, width, height, posx=0, posy=0):

        # call the parent constructor
        actionable.Actionable.__init__(self, image, width, height)

        # set position
        self.rect.x = posx
        self.rect.y = posy

        # create a dialogue box for it
        self.info = infoBox.InfoBox()

    
        
