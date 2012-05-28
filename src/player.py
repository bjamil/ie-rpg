import pygame
from constants import * 


class Player:
    """ the player """

    def __init__(self, screen, image, width, height, posx=0, posy=0):

        # set up the screen dimensions
        self.area = screen.get_rect()
        
        # create a rectangle for the player
        self.rect = pygame.Rect(posx, posy, width, height)

        # create an image for the player
        self.image = pygame.transform.scale(image, (width, height))

        # create a laser beam for the player
        self.beam = pygame.Surface([4, 20])
        self.beamRect =self.beam.get_rect()
        self.beam.fill(RED)
        self.beam.set_alpha(0)

        # define the direction he is facing
        self.face = UP 
        


    def draw(self, screen):
        " draws the player to the given screen "
        screen.blit(self.image, self.rect)
        
    def setPos(self, x, y):
        " set the x,y position of the player " 
        self.rect.x = x
        self.rect.y = y

    def hasCollided(self, collidable):
        " returns the indexes of the rectangles it has collided with "
        radius = 6
        self.rect.inflate_ip(radius, radius)
        collision = self.rect.collidelist(collidable)
        self.rect.inflate_ip(-radius, -radius)
        
        return collision



    def moveLeft(self, amount, collidable):
        " move left by the given amount, avoiding collisions with the given rects  "
        # always change the direction he is facing
        self.face = LEFT

        # move
        if self.rect.left > 0:# and self.rect.collidelist(collidable) == -1:
            self.rect.left -= amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.left += amount
        
    def moveRight(self, amount, collidable):
        " move right by the given amount, avoiding collisions with the given rects "
        # always change the direction he is facing
        self.face = RIGHT

        # move
        if self.rect.right < self.area.width: #and self.rect.collidelist(collidable) == -1:
            self.rect.left += amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.left -= amount

    def moveUp(self, amount, collidable):
        " move up by the given amount, avoiding collisions with the given rects "
        # always change the direction he is facing
        self.face = UP

        # move
        if self.rect.top > 0:# and self.rect.collidelist(collidable) == -1:
            self.rect.top -= amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.top += amount

    def moveDown(self, amount, collidable ):
        " move down by the given amount, avoiding collisions with the given rects " 
        # always change the direction he is facing
        self.face = DOWN

        # move
        if self.rect.bottom < self.area.height:# and self.rect.collidelist(collidable) == -1:
            self.rect.top += amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.top -= amount
        


    
    
