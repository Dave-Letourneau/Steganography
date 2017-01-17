
This program allows users to embed hidden messages inside images by making small adjustments to the pixels within the image.
https://en.wikipedia.org/wiki/Steganography

Installation:

1. Clone this repository: git clone https://github.com/Dave-Letourneau/Steganography.git
2. Install python 3.X. This project was built using version 3.5.0.
3. Install the required libraries using Pip. Pip install -r requirements.txt
4. Launch the program. python stegGui.py

Usage: 

When this program runs, it opens a GUI which allows you to place messages in an image or extract messages
from an image that has been used in a previous run of the program.

Steps to encode a message:
1. Select Encode, then click Next or Quit to exit
2. Add your message in the section labeled 'Insert Message Below'
3. Click 'Select Image' and find the picture you wish to use
4. Click 'Encode', then save the new image with a new name

Steps to decode a message:
1. Select Decode, then click Next or Quit to exit
2. Click 'Select Image' and find the picture with a hidden message
3. Click 'Decode' and the hidden message will appear

