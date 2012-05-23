import Tkinter, tkMessageBox, ttk
from tkFileDialog import *
from PIL import Image, ImageTk

GRIDWIDTH = 18
GRIDHEIGHT = 18
BG_TAG = "bg"
GRID_TAG="grid"
HEADER = "# ieRPG Map v0.1 _-_ Beenish is awesome"

class simpleapp_tk(Tkinter.Tk):
    """ a class used to build maps """ 
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent

        # initialize the gui
        self.initialize()

    def initialize(self):
        self.initializeGUI()
        self.resetMap()
        
    def resetMap(self, event=None):
        self.title('Untitled Map')
        self.saveFilename=None
        self.objDict = {}
        self.bgFilename= ""
        self.bgImg=None

        self.objsY=30 # y coordinate of next image
        self.objsX=10 # x coordinate of next image
        self.objects.config(scrollregion = (0,0, 200, self.objsY))

        # canvas switches
        self.moving = "" # are you moving an object on the canvas? 
        self._resetOldCoords() # old coordinates of the object being moved

        # clear canvas
        objs = self.canvas.find_all()
        for obj in objs:
            self.canvas.delete(obj)

        # clear objs list
        objs = self.objects.find_all()
        for obj in objs:
            self.objects.delete(obj)
    

        # redraw grid
        self._createGrid()

        self.filemenu.entryconfigure('Save As', state='disabled')

        
    def initializeGUI(self):
        self.grid()
        
        # label:
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, columnspan=2, sticky='EWS')
        self.labelVariable.set(u"Press the 'Load BG Image' button to load a background image." +
                               "\nPress the 'Load Object' button to load a collidable object." +
                               "\nClick on any loaded object to place it on the top left corner of the map" +
                               " \n Drag objects on the map around to place them at the desired locations.")

        # canvas:
        self.CANVAS_WIDTH=600
        self.CANVAS_HEIGHT=500
        
        self.canvas = Tkinter.Canvas(self, bg = "white" ,
                                     height=self.CANVAS_HEIGHT, width=self.CANVAS_WIDTH)
        self.canvas.grid(column=0, row = 3, columnspan=2, sticky='W')

        # create grid
        self._createGrid()

        # possible objects 
        self.objects = Tkinter.Canvas(self, bg = "gray", width=200)
 

        # scrollbar
        yscroll = Tkinter.Scrollbar(self)
        yscroll.config(command=self.objects.yview)
        xscroll = Tkinter.Scrollbar(self, orient='horizontal')
        xscroll.config(command=self.objects.xview)
        
        self.objects.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        yscroll.grid(column=2,row=3, sticky="NS")
        xscroll.grid(column=1, row=4, sticky="EW")
        self.objects.grid(column=1, row=3, sticky="NSWE")


     #   self.objects.grid_propagate(False) # don't resize the grid 
        
        # load background button
        self.bgButton = Tkinter.Button(self, text="Load BG Image")
        self.bgButton.grid(column=0, row=5, sticky='W')

        # load objects button
        self.objButton = Tkinter.Button(self, text="Load an object")
        self.objButton.grid(column=1, row=5, sticky='W')


        # menu bar
        menubar=Tkinter.Menu(self)

        #file 
        self.filemenu=Tkinter.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="New", accelerator="<Ctr+n>", command=self.resetMap)
        self.filemenu.add_command(label="Open", accelerator="<Ctr+o>", command=self.load)
        self.filemenu.add_command(label="Save", accelerator="<Ctr+s>", command=self.save)
        self.filemenu.add_command(label="Save As", command=self.saveAs, state='disabled')
        menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.config(menu=menubar)

        
        # allow resizing columns
        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False)

        # fix window size
        self.update()
        self.geometry("825x625")

        # bind events
        self.canvas.bind('<Button-1>', self.OnIconPress)
        self.objButton.bind("<ButtonRelease-1>", self.OnButtonClick)
        self.bgButton.bind("<ButtonRelease-1>", self.OnButtonClick)
        self.objects.bind('<Button-1>', self.OnIconPress)
        self.canvas.bind('<ButtonRelease-1>', self.OnIconRelease)
        self.canvas.bind('<B1-Motion>', self.OnIconDrag)
        self.bind('<Control-s>', self.save)
        self.bind('<Control-o>', self.load)
        self.bind('<Control-n>', self.resetMap)


    def OnButtonClick(self, event):
        # it's the load background button 
        if event.widget == self.bgButton:
            fn  = askopenfilename() # get filename
            self._loadBG(fn)
            
        # it's the load object button
        elif event.widget == self.objButton:
            fn = askopenfilename() # get filename
            self._loadObject(fn)
            

        
    def OnIconPress(self, event):
        
        if event.widget == self.objects:
            item=self.objects.find_withtag("current")
            if len(item) > 0: # if an item is actually pressed
                # get all its tags
                tags=self.objects.gettags(item)

                # use the first tag
                self._placeImageOnCanvas(tags[0])

        elif event.widget == self.canvas:
            # user is moving an item. figure out what it is (its id)
            item = self.canvas.find_withtag("current")
            if len(item) > 0:
                tags = self.canvas.gettags(item)
                if tags[0] != BG_TAG and tags[0] != GRID_TAG: # don't move bg or grid
                    self.moving=item
                    #tags = self.canvas.gettags(self.moving)
                    box = self.canvas.bbox(item)
                    self.oldCoords=(self.canvas.canvasx(event.x),
                                    self.canvas.canvasy(event.y), box[0], box[1])


    def _placeImageOnCanvas(self, tag, pxlRow=0, pxlCol=0):
        " places the loaded image with the given tag on the canvas "
        self.canvas.create_image(pxlRow,pxlCol,image=self.objDict[tag][0], tags=tag, anchor='nw')

        
    def OnIconRelease(self, event):

        if len(self.moving) >0 :
            # snap to grid
            box = self.canvas.bbox(self.moving)
            newx = self.canvas.canvasx(box[0], gridspacing=GRIDWIDTH)
            newy = self.canvas.canvasy(box[1], gridspacing=GRIDHEIGHT)

            xdiff = newx - box[0]
            ydiff = newy - box[1]
            self.canvas.move(self.moving, xdiff, ydiff)
            
            # reset switches
            self.moving = ""
            self._resetOldCoords()

            

    def _resetOldCoords(self):
        self.oldCoords=(0,0,0,0)

    def OnIconDrag(self, event):

        # drag the icon around 
        if len(self.moving) >0:
            newx =self.canvas.canvasx(event.x)
            newy =self.canvas.canvasy(event.y)

            xdiff = newx - self.oldCoords[0]
            ydiff = newy - self.oldCoords[1]
            
            self.canvas.move(self.moving,xdiff, ydiff)

            box = self.canvas.bbox(self.moving)
            self.oldCoords=(newx, newy, box[0], box[1])


    def _loadBG(self, fn):        
        if len(fn) > 0: # a file was selected
            try:
                self.bgFilename=fn
                # load the new background
                self.bgImg = ImageTk.PhotoImage(Image.open(self.bgFilename))
                item = self.canvas.create_image(0,0,anchor='nw', image=self.bgImg)
                self.canvas.tag_lower(item)

                # delete the old background
                self.canvas.delete(BG_TAG)
                self.canvas.itemconfig(item, tags=BG_TAG)
                
            except(IOError):
                tkMessageBox.showerror("I said pictures, Jerry!" ,"Invalid background image file selected. \nFile: " + fn )


    def _loadObject(self, fn):
        
        if len(fn) > 0: # a file was selected
            objFilename = fn
            tag = self._getTag(objFilename)

            # if we've already loaded this image, don't reload it
            if tag in self.objDict:
                tkMessageBox.showinfo('You Fool!', 'This image has already been loaded.\n\nFilaneme: ' + objFilename)
                return


            # Load image 
            try:
                # load the object image, place it on the object menu,
                # and save a reference to it 
                img = ImageTk.PhotoImage(Image.open(objFilename))

                icon = self.objects.create_image(self.objsX, self.objsY,
                                          anchor = 'nw', image=img)

                # create a tag for the icon by removing all whitespace from the filename
                self.objects.itemconfig(icon, tags=tag)

                # draw a horizontal line
                self.objsY = self.objsY + img.height() + 15
                self.objects.create_line(0, self.objsY, 200, self.objsY)
                self.objsY = self.objsY + 15

                # update scroll region 
                self.objects.config(scrollregion=(0,0,200,self.objsY))

                # add it to the dictionary
                self.objDict[tag] = (img, objFilename)

            except(IOError):
                tkMessageBox.showerror("Error", "Could not open image file : " + fn +" Please make sure it exists and is an image file.") 
    
        
    def _getTag(self,string):
        " returns a tag constructed from the input string "
        # remove whitespace from input string 
        return ''.join(string.split(' '))


    def _createGrid(self):
        " creates a grid on the canvas "

        # create vertical lines
        for i in range(0, self.CANVAS_WIDTH, GRIDWIDTH):
            self.canvas.create_line(i, 0, i, self.CANVAS_HEIGHT, tags=GRID_TAG)
        
        # create horizontal lines
        for i in range(0, self.CANVAS_HEIGHT, GRIDHEIGHT):
            self.canvas.create_line(0, i, self.CANVAS_WIDTH, i, tags=GRID_TAG)
        

    def save(self, event=None):  # event argument added in case keyboard shortcut was used
        " write current state of map to file "
        
        # open the file that we will write to
        if self.saveFilename == None:   # we haven't saved this map before 
            fout = asksaveasfile(mode='w', defaultextension=".iemap") # ask for a file name
            if fout == None:    # no file selected
                return
            self.saveFilename=fout.name
        else:
            fout = open(self.saveFilename, mode="w")
        
        print " Saving, please wait. " + fout.name

        # header
        out = HEADER

        # BG image
        out +=  "\nBG|" + self.bgFilename + "|"

        # Objects
        for tag in self.objDict:
            out += "\nOBJ|" + self.objDict[tag][1] + "|" # filename

            # save all grid cell locations of that tag on the canvas
            loc = self.canvas.find_withtag(tag)
            cellLoc = []
            for oid in loc:
                box = self.canvas.bbox(oid)
                out += " " + str(box[0]/GRIDWIDTH) + "," + str(box[1]/GRIDHEIGHT)
                
        fout.write(out)
        fout.close()
        print "Saved!" 
        self.title(fout.name)
        self.filemenu.entryconfigure('Save As', state='normal')

                
    def saveAs(self, event=None):
        " use a diff filename to save this map "
        fn=asksaveasfile()
        if fn==None:
            return # no file selected

        # else
        self.saveFilename=fn.name # save to this filename
        fn.close()
        self.save()
        
    def load(self, event=None): # event argument added in case keyboard shortcut was used
        " load a saved map "
        
        # ask user which file to open 
        fin = askopenfile(mode="r")
        if fin==None:
            print "No file selected " 
            return # no file selected
        print "Loading map, please wait."
        text = fin.read().split("\n")
        fin.close()

        if text[0]!=HEADER: #ensure file opened was not corrupt
            tkMessageBox.showerror("Wth?!", "Corrupt or Old Map File Format!\nFile: " + fin.name)
            return

        # reset this map
        self.resetMap()
        
        # load bg
        self._loadBG(text[1].split("|")[1])

        # load the rest of the objects ..
        for i in range(2, len(text)):
            info = text[i].split("|")
            if info[0].strip() == "OBJ" :

                # load the object
                self._loadObject(info[1].strip())
                
                # place it on canvas
                tag = self._getTag(info[1])
                cellLoc = (info[2].strip()).split(" ") # get each cell location

                for loc in cellLoc:
                    components=loc.split(",")
                    if len(components )> 1:
                        row = int(components[0])
                        col = int(components[1])

                        self._placeImageOnCanvas(tag, pxlRow=row*GRIDHEIGHT, pxlCol=col*GRIDWIDTH)

        self.saveFilename=fin.name
        self.title(fin.name)
        self.filemenu.entryconfigure('Save As', state='normal')
                    
                
                             
if __name__ == "__main__":
    app = simpleapp_tk(None)
 #   app.title("Untitled Map")
    app.mainloop()
