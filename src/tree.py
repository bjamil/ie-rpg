import pygame


# this class represents a tree
class Tree:
    """ This class represents a tree """

    # constructor. pass in the tree image and dimensions 
    def __init__(self, image, tree_width, tree_height, stump_width, stump_height):

        # create a scaled image of the tree
        self.image = pygame.transform.scale(image, (tree_width, tree_height))
        
        # create a rectangle for the tree
        self.treeRect = self.image.get_rect()

        # create a rectangle for the stump (default rectangle for collision detection)
        self.stump = pygame.Rect(0,0, stump_width, stump_height)
        self.stump.bottom = self.treeRect.bottom
        self.stump.centerx = self.treeRect.centerx


    def draw(self, screen):
        " draws the tree to the given screen " 
        screen.blit(self.image, self.treeRect)

    
    def setPos(self, x, y):
        "set the x,y position of the tree"

        # compute displacement
        xDisplacement = x - self.treeRect.x 
        yDisplacement = y - self.treeRect.y 

        # move the rectangles
        self.treeRect.x = x
        self.treeRect.y = y

        self.stump.x += xDisplacement
        self.stump.y += yDisplacement 
