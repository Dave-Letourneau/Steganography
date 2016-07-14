
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

# def callback():
#     name = askopenfilename()
#     print(name)
#
# # For the actual object, add this method as a "ENCODE NOW" type button method
# def getInput():
#     input = text.get("1.0", "end-1c") # end is the end of the text box, -1 is 1 character less, to remove new line
#     print(input)
#
# errmsg = 'Error!'
# Button(text='File Open', command=getInput).pack(fill=X)
#
# text = Text(height=6, width=75, wrap=WORD)
# text.pack()



# This seems to be needed to get it to perform.
#mainloop()


# Try to make it in class format below

class startMenu:
    """A class containing GUI functons for use
    in my steganography program. The start
    menu calls the other menus depending on
    the user's request."""
    def __init__(self, master):
        # Variables for this menu
        self.mode = IntVar()                # Encode or Decode mode
        # self.saveName = "dummy save path"   # file name of new image
        self.master = master                # name of the tk instance
        self.frame = Frame(self.master)     # frame of this window
        self.child = None                   # Initially there is no child
        # Button variables - File explorer and mode boxes respectively
        #self.fileButton = Button(self.frame, text='Class button', command=self.call).pack(fill=X)
        self.EncodeBox = Radiobutton(self.frame, text='Encode', variable=self.mode, value=0).pack(anchor=W)
        self.DecodeBox = Radiobutton(self.frame, text='Decode', variable=self.mode, value=1).pack(anchor=W)
        #self.saveButton = Button(self.frame, text='Save filename', command=self.save).pack(fill=X)
        self.proceedButton = Button(self.frame, text='Next', command=self.openMenu).pack(fill=X)
        # personal use button
        self.test = Button(self.frame, text='Print mode', command=self.pmode).pack(fill=X)
        self.frame.pack()

    def openMenu(self):
        """This method is called
        when the user clicks the PROCEED
        button, and creates a child window
        of either the Encode or Decode
        menus depending on the user's
        selection."""
        self.child = Toplevel(self.master)
        # Create a child window depending on the mode
        if self.mode.get() == 0:
            self.app = EncodeMenu(self.child)
        else:
            self.app = DecodeMenu(self.child)

    def pmode(self):
        print(self.mode.get())
        print(self.saveName)

    def save(self):
        self.saveName = asksaveasfilename()

class EncodeMenu:
    """ The encode menu is the menu
    that appears when the user request
    the ability to encode a message into
    an image.
    """
    def __init__(self, master):
        # Set up the Tk box
        self.master = master
        master.title("Image Encoder")
        self.frame = Frame(self.master)
        # Variables required for this menu
        self.filepath = None
        self.userInput = Text(self.frame, height=8, width=45, wrap=WORD, borderwidth=3).pack()
        self.userPath = Text(self.frame, height=1, width=45, borderwidth=3, state=DISABLED)
        self.label = Label(master, text="Insert Message Below").pack()
        self.userPath.pack()
        # Buttons
        self.quit = Button(self.frame, text="Cancel", command=self.close)
        self.quit.pack(side=RIGHT, ipadx=10, padx=7, expand=0)
        self.getFile = Button(self.frame, text="Select Image", command=self.getFilePath)
        self.getFile.pack(side=LEFT, ipadx=10, padx=7, expand=0)
        self.encode = Button(self.frame, text="Encode", command=self.enc)
        self.encode.pack(side=LEFT, ipadx=10, expand=0)
        self.frame.pack()

    def getFilePath(self):
        """This method allows the user
        to select an image through
        use of the filebrowser, then
        displays the file path in the
        text box."""
        self.filepath = askopenfilename()

        # Change the text box to be editable
        self.userPath.configure(state=NORMAL)
        # Clear out the text box
        self.userPath.delete("1.0", END)
        # Insert the file path to the text box
        self.userPath.insert(INSERT, self.filepath)
        # Set the textbox to be un-editable
        self.userPath.configure(state=DISABLED)

    def close(self):
        self.master.destroy()

    def testF(self):
        print(self.filepath)


    def enc(self):
        """Method for encoding the
        user's message into an image."""
        print("wow. Wink")


class DecodeMenu:
    """ The decode menu appears
    when the user requests the
    ability to decode a message
    from a previously encoded image.
    """
    def __init__(self, master):
        self.master = master
        master.title("Image Decoder")
        self.frame = Frame(self.master)
        self.quit = Button(self.frame, text="Cancel", command=self.close).pack()
        self.frame.pack()

    def close(self):
        self.master.destroy()
# Object will likely need to be instantiated from Steg
root = Tk()
root.title("Steganographer")
g = startMenu(root)

mainloop()
