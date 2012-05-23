import pygame

class InfoBox:
    """ the dialogue box at the bottom of the screen """
    screenRect = None   # rectangle of game sreen
    textRendered = False
    
    def __init__(self, screen=None, color=(0,0,200), width=532, height=108, bottom_padding=10):

        # create a rectangle for it
        self.box = pygame.Surface([width, height])
        self.rect = self.box.get_rect()
        self.color = color
        self.box.fill(color)
        self.box.set_alpha(255*.5)

        global screenRect

        # position it
        if screen:
            screenRect = screen.get_rect()
            self.rect.bottom = screenRect.height - bottom_padding
            self.rect.centerx = screenRect.centerx

        # add text properties 
        self.text = []
        self.messageLines = 0 # num of lines in the message
        fontSize = 12
        lineSpace = 5 # space in between two lines
        verdana = pygame.font.match_font('Verdana')
        self.font = pygame.font.Font(verdana, fontSize)

        # divide the text into pages
        self.pages = []
        self.numPages = 0
        self._currPage = 0

        # verify how many lines can be in one page
        self.numLines = 1+(height - 2*10)/(fontSize + lineSpace)  # 2*10 = space at top and bottom
        
        
        # add image
        self.image = None
        self.imageRect = pygame.Rect(0,0, 72,72)
        self.imageRect.centery = self.rect.height/2
        self.imageRect.left = 18
        
        # set it as inactive
        self.active = False
        
    
    def _resetBox(self):
        self.box.fill(self.color)
        
    def draw(self, screen):
        " draws the current page in the info box onto the screen "

        global screenRect

        if not screenRect:
            screenRect = screen.get_rect()
            self.rect.bottom = screenRect.height - bottom_padding
            self.rect.centerx = screenRect.centerx

        self._resetBox()

        if self._currPage >= self.numPages:
            self._currPage = self.numPages -1 # keep printing the last page
        
        # get text
        text, textRect = self._getText(self._currPage)

        # blit txt to info box
        for i in range(len(text)):
            self.box.blit(text[i], textRect[i])

        # blit image onto info box
        self.box.blit(self.image, self.imageRect)
        
        # blit info box to screen 
        screen.blit(self.box, self.rect)

    def nextPage(self, screen):
        " draws the rest of the message onto the screen if it is longer than self.numlines "
        self._currPage = self._currPage + 1
        self.draw(screen)
        
    def hasNextPage(self):
        " returns True if the current page isnt the last page in the box "
        print self._currPage
        print self.numPages
        return self._currPage < self.numPages-1

    def close(self):
        " close the info box "
        self._currPage = 0 # start with the first page the next time 
        
    def _getText(self, pageNum):
        " returns the text for the specified page number " 
        text = []
        textRect = []

        if pageNum < self.numPages:            
            for i in range(len(self.pages[pageNum])):
                # render text
                text.append(self.font.render(self.pages[pageNum][i], False, (255,255,255)))

                # position it 
                tmp = text[i].get_rect()
                tmp.left = 110
                tmp.top = i*12 +10
                textRect.append(tmp)

        return text, textRect
        
    def setText(self, text):
        " sets the input text as the text for this info box " 
        # parse input text so that each line is an individual element in the list
        # split long lines into two-- allow only ~60 chars per line
        # don't cut off words at line ends. Pass the word that could be cut off to the
        # next line 
        self.text = []
        LINE_SIZE = 60
        for line in text.split("\n"):
            if len(line) <= LINE_SIZE :
                self.text.append(line)
            else:
                start = 0 # start index ( to avoid cutting off words )
                end = LINE_SIZE 
                while start < len(line):
                    substr = line[start:end]
                    # if the last character is not an empty space,
                    # find the last end of word token and split the
                    # line at that point
                    if substr[-1] != ' ' and len(substr) == LINE_SIZE:
                        end = start+substr.rfind(' ')

                    # if we couldn't find a space in this line , revert
                    # to our old end point
                    if end == 0:
                        end = start+LINE_SIZE 

                    # add the substring to our growing list
                    self.text.append(line[start:end].strip())
                    start = end
                    end = start + LINE_SIZE 
        
        
        self.messageLines = len(self.text)

        # divide text up into pages
        self.numPages = self.messageLines/self.numLines
        if self.messageLines % self.numLines > 0:   # there are more lines
            self.numPages = self.numPages + 1

        for i in range(self.numPages-1):
            self.pages.append(self.text[i*self.numLines : (i+1)*self.numLines])

        self.pages.append(self.text[(self.numPages -1)*self.numLines:])

        # set the active page to 0
        self._currPage = 0
        

    def setImage(self, image):
        self.image = pygame.transform.scale(image, (self.imageRect.width, self.imageRect.height))
        
