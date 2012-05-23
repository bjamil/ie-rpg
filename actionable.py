import pygame

class Actionable:
    """ an object whose actions a player can trigger using the 'action' button """

    def __init__(self, image, width, height):

        # create a rectangle for it
        self.rect = pygame.Rect(0,0, width, height)

        # set its image
        self.image = pygame.transform.scale(image, (width, height))

        # set active
        self.active = False

    def action(self):
        " perform action "
        print "action!"

    def draw(self, screen):
        " draws the player to the given screen "
        screen.blit(self.image, self.rect)

    def setPos(self, x, y):
        " sets the position of the object "
        self.rect.x = x
        self.rect.y = y
    

    
