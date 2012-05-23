import Tkinter

class mapMaker(Tkinter.Tk):
    """ a class used to build maps """ 

    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent

        # initialize the gui
        self.initialize()

    def initialize(self):
        self.grid()

        # text field: 
        # create the widget
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)

        # add the widget to the gui at row=0, column=0
        self.entry.grid(column=0, row=0, sticky='EW')

        # bind an action to the entry form when enter is pressed 
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")


        # button:
        button = Tkinter.Button(self, text=u"Click me!",
                                        command=self.OnButtonClick) # action command
        button.grid(column=1, row=0)

        # label:
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.labelVariable.set(u"Hello !")

        # allow resizing columns
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)

    def OnButtonClick(self):
        self.labelVariable.set("You clicked the button !")
        
    def OnPressEnter(self,event):
        self.labelVariable.set("You pressed enter !")

        

if __name__ == "__main__":
    app = mapMaker(None)
    app.title('Map Maker')
    app.mainloop()
