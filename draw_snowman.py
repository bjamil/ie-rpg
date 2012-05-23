import pygame

white = (255, 255, 255)

# Define a function that will draw a snowman at a certain location
def draw_snowman(screen,x,y):
    pygame.draw.ellipse(screen,white,[35+x,0+y,25,25])
    pygame.draw.ellipse(screen,white,[23+x,20+y,50,50])
    pygame.draw.ellipse(screen,white,[0+x,65+y,100,100])
     
