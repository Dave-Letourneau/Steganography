"""
The following is a GUI comprised of a
series of menus that enable to the user to
use my steganography program. With the addition
of this GUI, the previous version of the
steganography.py program has been changed to
no longer work on its own. Instead, the
functions that previously existed under the
older version have been changed to blend with
this GUI, which now serves as the main function
for running my program. For more information
on how the steganography process works, see
the steganography.py file.

Author: David Letourneau, 7/13/2016
"""

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from steganography import encodeGUI as encode, decodeGUI as decode

class startMenu:
    """A class containing GUI functons for use
    in my steganography program. The start
    menu calls the other menus depending on
    the user's request(Either encode or
    decode.)"""
    def __init__(self, master):
        # Variables for this menu
        self.mode = IntVar()                # Encode or Decode mode
        self.master = master                # name of the tk instance
        self.frame = Frame(self.master)     # frame of this window
        self.child = None                   # Child windows created

        # Button variables - File explorer and mode boxes respectively
        self.EncodeBox = Radiobutton(self.frame, text='Encode', variable=self.mode, value=0).pack()
        self.DecodeBox = Radiobutton(self.frame, text='Decode', variable=self.mode, value=1).pack()
        self.proceedButton = Button(self.frame, text='Next', command=self.openMenu)
        self.proceedButton.pack(side=LEFT, pady=5, padx=25, ipadx=25)
        self.quitButton = Button(self.frame, text='Quit', command=self.close)
        self.quitButton.pack(side=LEFT, pady=5, padx=25, ipadx=25)
        self.frame.pack()

    def close(self):
        # Closes the current window.
        self.master.destroy()

    def openMenu(self):
        """This method is called
        when the user clicks the PROCEED
        button, which creates a child window
        of either the Encode or Decode
        menus depending on the user's
        selection."""
        self.child = Toplevel(self.master)

        # Create a child window depending on the mode
        if self.mode.get() == 0:
            self.app = EncodeMenu(self.child)
        else:
            self.app = DecodeMenu(self.child)

class EncodeMenu:
    """ The encode menu is the menu
    that appears when the user request
    the ability to encode a message into
    an image. It makes use of the
    encodeGUI function from the file
    steganography.py"""
    def __init__(self, master):
        # Set up the Tkinter box
        self.master = master
        master.title("Image Encoder")
        self.frame = Frame(self.master)
        self.label = Label(master, text="Insert Message Below").pack()

        # Variables required for this menu
        self.filepath = ""
        self.userInput = Text(self.frame, height=8, width=45, wrap=WORD, borderwidth=3)
        self.userPath = Text(self.frame, height=1, width=45, borderwidth=3, state=DISABLED)
        self.savePath = "Initially save path is empty."
        self.userInput.pack()
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
        self.filepath = askopenfilename(filetypes=[
            ('JPG files', '*.jpg'),
            ('PNG files', '*.png'),
            ('BMP files', '*.bmp'),
            ('JPEG files', '*.jpeg')
        ])

        """The following changes the text
        box to allow insertion of text,
        places the filepath inside it, and
        resets it to disable editing so the
        user can't interfere with the filepath."""
        self.userPath.configure(state=NORMAL)
        self.userPath.delete("1.0", END)
        self.userPath.insert(INSERT, self.filepath)
        self.userPath.configure(state=DISABLED)

    def close(self):
        # Closes the current window.
        self.master.destroy()

    def enc(self):
        """Method for encoding the
        user's message into an image."""

        self.savePath = asksaveasfilename(filetypes=[
            ('BMP file', '*.bmp'),
            ('PNG file', '*.png')
        ], defaultextension='*.bmp')

        # Make sure the user entered a name. if not, do nothing
        if len(self.filepath) == 0 or len(self.savePath) == 0:
            return

        """The range 1.0 - end-1c starts at the beginning
        of the string and extends until the end, remove the
        new line character added by the Text widget.
        The encode function is imported from steganography.py"""
        encode(self.userInput.get("1.0",'end-1c'), self.filepath, self.savePath)


class DecodeMenu:
    """ The decode menu appears
    when the user requests the
    ability to decode a message
    from a previously encoded image."""
    def __init__(self, master):
        self.master = master
        master.title("Image Decoder")
        self.frame = Frame(self.master)
        self.label = Label(master, text="Decoded message will appear below")
        self.label.pack()
        self.frame.pack()

        # variables
        self.filepath = None
        self.message = Text(self.frame, height=8, width=45, wrap=WORD, borderwidth=3, state=DISABLED)
        self.userPath = Text(self.frame, height=1, width=45, borderwidth=3, state=DISABLED)
        self.message.pack()
        self.userPath.pack()

        # Buttons
        self.quit = Button(self.frame, text="Cancel", command=self.close)
        self.quit.pack(side=RIGHT, ipadx=10, padx=7, expand=0)
        self.getFile = Button(self.frame, text="Select Image", command=self.getFilePath)
        self.getFile.pack(side=LEFT, ipadx=10, padx=7, expand=0)
        self.encode = Button(self.frame, text="Decode", command=self.dec)
        self.encode.pack(side=LEFT, ipadx=10, expand=0)
        self.frame.pack()

    def getFilePath(self):
        """This method allows the user
        to select an image through
        use of the filebrowser, then
        displays the file path in the
        text box."""
        self.filepath = askopenfilename(filetypes=[
            ('PNG files', '*.png'),
            ('BMP files', '*.bmp'),
        ])

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

    def dec(self):
        """The dec method reads from an image
        previously encoded with a message and
        prints out the hidden text to the screen.
        As with the enc method, the decodeGUI
        function is imported from the file
        steganography.py, which contains more
        documentation for the function."""

        # Make sure the user entered a file to decode. if not, do nothing
        if self.filepath != None and self.filepath != "":
            message = decode(self.filepath)

            """The following changes the text
            box to allow insertion of text,
            places the filepath inside it, and
            resets it to disable editing so the
            user can't interfere with the filepath."""
            self.message.configure(state=NORMAL)
            self.message.delete("1.0", END)
            self.message.insert(INSERT, message)
            self.message.configure(state=DISABLED)


# Instantiate the GUI object and run the program
root = Tk()
root.geometry("235x100")
root.title("Steganographer")
g = startMenu(root)

mainloop()
