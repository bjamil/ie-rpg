# src: http://www.pyedpypers.org/forum/viewtopic.php?f=11&t=1494
# author: Keeyai
# description:
#       I was helping someone today in IRC and thought the code might end up
#       being helpful for others as well. He was trying to get a 'game board'
#       with tiles and gaps between them, then calculate which tile was being
#       clicked on with the mouse. He wanted to make each tile an object and
#       iterate through them all checking for collisions; I suggested this
#       was extreme overkill and wrote this as an example.
#
#       It's built directly on the shell of the pong tutorial at muagames,
#       so if something is unclear, go read those for a thorough explanation
#
#
#


try:
    import pygame
    from pygame.locals import *

except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    sys.exit(1)

class Game(object):

    def __init__(self):
        self.width = 600
        self.height = 600
        self.boardsize = 8
        self.tilegap = 5
        self.tilecolor = (100, 120, 200)


        self.tilewidth = (self.width / self.boardsize) - self.tilegap
        self.tileheight = (self.height / self.boardsize) - self.tilegap

        # load and set up pygame
        pygame.init()

        # create our window
        self.window = pygame.display.set_mode((self.width, self.height))

        # clock for ticking
        self.clock = pygame.time.Clock()

        pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])

        # make background
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((255,255,255))

        self.drawGrid()
        # flip the display so the background is on there
        pygame.display.flip()

        # a sprite rendering group
        self.sprites = pygame.sprite.RenderUpdates()

        # make a simple sprite to represent a 'piece' on the board
        self.piece = pygame.sprite.Sprite()
        self.piece.rect = pygame.Rect(-50, -50, 50, 50)
        self.piece.image = pygame.Surface((self.piece.rect.width, self.piece.rect.height))
        self.piece.image.fill((0,0,0))
        self.sprites.add(self.piece)

    def drawGrid(self):
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                # draw a box
                left = i*(self.tilewidth+self.tilegap)
                top = j*(self.tileheight+self.tilegap)
                pygame.draw.rect(self.background, self.tilecolor, pygame.Rect( left, top, self.tilewidth, self.tileheight))

        self.window.blit(self.background, (0,0))

    def run(self):
        """Runs the game. Contains the game loop that computes and renders
        each frame."""

        print 'Starting Event Loop'

        running = True
        # run until something tells us to stop
        while running:

            # tick pygame clock
            # you can limit the fps by passing the desired frames per seccond to tick()
            self.clock.tick(60)

            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()

            # update the title bar with our frames per second
            pygame.display.set_caption('A LarsHelo Example - %d fps' % self.clock.get_fps())

            # update our sprites
            for sprite in self.sprites:
                sprite.update()

            # render our sprites
            self.sprites.clear(self.window, self.background)    # clears the window where the sprites currently are, using the background
            dirty = self.sprites.draw(self.window)              # calculates the 'dirty' rectangles that need to be redrawn

            # blit the dirty areas of the screen
            pygame.display.update(dirty)                        # updates just the 'dirty' areas

        print 'Quitting. Thanks for playing'

    def handleEvents(self):
        """Poll for PyGame events and behave accordingly. Return false to stop
        the event loop and end the game."""

        # poll for pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            # handle user input
            elif event.type == KEYDOWN:
                # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    return False

            elif event.type == MOUSEBUTTONDOWN:
                self.handleMouseClick(event)

        return True

    def handleMouseClick(self, event):
        mousex, mousey = event.pos

        # calculate the square this is on
        tilex = int(mousex / (self.tilewidth + self.tilegap))
        tiley = int(mousey / (self.tileheight + self.tilegap))

        # move piece to the center of this tile
        self.piece.rect.center = ( (tilex * (self.tilewidth+self.tilegap)) + (self.tilewidth/2), (tiley * (self.tileheight+self.tilegap)) + (self.tileheight/2))

# create a game and run it
if __name__ == '__main__':
    game = Game()
    game.run()
