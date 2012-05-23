import pygame

class Laser:
    """ the laser beam """

    def __init__(self, screen, posx, posy, direction, color=(255,0,0), width=4, height=20):

        # create a rectangle for it
        # if the direction is up or down, make the beam vertical ; else horizontal 
        if direction == "up" or direction == "down" : 
            self.beam = pygame.Surface([width, height])
        else:
            self.beam = pygame.Surface([height, width])
        
        self.rect = self.beam.get_rect()
        self.color = color
        self.beam.fill(color)
        self.beam.set_alpha(255*.8)

        # set its initial x,y positions
        self.rect.x = posx
        self.rect.y = posy
    
        # set it as inactive
        self.active = True

        # get the area of the screen ( for testing purposes ) 
        self.area = screen.get_rect()
        self.direction = direction 
    
    def draw(self, screen):
        " draws the current page in the info box onto the screen "
        # set this beam as active
        self.active = True
        
        # draw beam 
        screen.blit(self.beam, self.rect)


    def moveBeam(self, amount, collidable):
        if self.direction == "left":
            self.moveLeft(amount, collidable)
        elif self.direction == "right":
            self.moveRight(amount, collidable)
        elif self.direction == "up":
            self.moveUp(amount, collidable)
        elif self.direction == "down":
            self.moveDown(amount, collidable)

    def moveLeft(self, amount, collidable):
        " move left by the given amount, avoiding collisions with the given rects  " 
        if self.rect.left > 0:# and self.rect.collidelist(collidable) == -1:
            self.rect.left -= amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.left += amount
                self.active = False
        else:
            self.active = False
        
    def moveRight(self, amount, collidable):
        " move right by the given amount, avoiding collisions with the given rects "
        if self.rect.right < self.area.width: #and self.rect.collidelist(collidable) == -1:
            self.rect.left += amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.left -= amount
                self.active = False
        else:
            self.active = False

    def moveUp(self, amount, collidable):
        " move up by the given amount, avoiding collisions with the given rects "
        if self.rect.top > 0:# and self.rect.collidelist(collidable) == -1:
            self.rect.top -= amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.top += amount
                self.active = False
        else:
            self.active = False

    def moveDown(self, amount, collidable ):
        " move down by the given amount, avoiding collisions with the given rects " 
        if self.rect.bottom < self.area.height:# and self.rect.collidelist(collidable) == -1:
            self.rect.top += amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.top -= amount
                self.active = False
        else:
            self.active = False
        


    
    

    
