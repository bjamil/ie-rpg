import pygame

RED     = (255, 0, 0)

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

    def shootLaser(self, screen, clock):
        """ shoots a laser beam until the end of the screen is reached """
        self.beamRect.x = self.rect.centerx-3
        self.beamRect.y = self.rect.top - 24
        self.beam.set_alpha(255*.8)
        screen.blit(self.beam, self.beamRect)
        print "pew"
        print 'y',  self.beamRect.y
        print 'top ' , self.beamRect.top
        
        while self.beamRect.top > 0:
            self.beamRect.y -= 20
            screen.blit(self.beam, self.beamRect)
            clock.tick(10)


    def moveLeft(self, amount, collidable):
        " move left by the given amount, avoiding collisions with the given rects  " 
        if self.rect.left > 0:# and self.rect.collidelist(collidable) == -1:
            self.rect.left -= amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.left += amount
        
    def moveRight(self, amount, collidable):
        " move right by the given amount, avoiding collisions with the given rects "
        if self.rect.right < self.area.width: #and self.rect.collidelist(collidable) == -1:
            self.rect.left += amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.left -= amount

    def moveUp(self, amount, collidable):
        " move up by the given amount, avoiding collisions with the given rects "
        if self.rect.top > 0:# and self.rect.collidelist(collidable) == -1:
            self.rect.top -= amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.top += amount

    def moveDown(self, amount, collidable ):
        " move down by the given amount, avoiding collisions with the given rects " 
        if self.rect.bottom < self.area.height:# and self.rect.collidelist(collidable) == -1:
            self.rect.top += amount
            if self.rect.collidelist(collidable) >= 0:
                self.rect.top -= amount
        


    
    
