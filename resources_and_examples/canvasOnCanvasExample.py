import Tkinter, tkFileDialog, tkMessageBox, ttk
from PIL import Image, ImageTk

GRIDWIDTH = 18
GRIDHEIGHT = 18
BG_TAG = "bg"

class simpleapp_tk(Tkinter.Tk):
    """ a class used to build maps """ 
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent

        # initialize the gui
        self.initialize()

    def initialize(self):
        self.grid()

        self.root = Tkinter.Canvas(self, bg = "red", height=500, width = 800)
        self.root.grid(column=0,row=0, sticky='NSEW')
        
        
        # canvas:
        self.canvas = Tkinter.Canvas(self.root, bg = "white" , height=400, width=600)
        #self.canvas.grid(column=0, row = 0, columnspan=2, sticky='W')
        self.root.create_window(0,0,window=self.canvas)


        # objects
        self.objects = Tkinter.Canvas(self.root, bg="blue", height=400, width=200)
        #self.objects.grid(column=1, row=0, sticky='E')
        self.root.create_window(0,1000, window=self.objects)
        

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Canvas on Canvas')
    app.mainloop()
