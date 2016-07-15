"""
This program takes an image file and a message from the user
and transcribes the message into a new version of the image
using the parity of the RGB values within the image. The user
can request to encode a message into an image given an
appropriate path, or decode a message that has already
been encoded into an existing image. Please note that
this program was written in a version of python 3, and
therefore requires the use of the Pillow library to work,
since the PIL library is not officially supported in python
3. Documentation and downloads for the community supported
pillow library can be found online.

Author: David Letourneau, 6/29/2016
"""

from PIL import Image

# Function definitions

def textToBinary(text):
    """Function for converting a
    text string into binary"""
    binary = ''.join(format(ord(x), 'b').zfill(8) for x in text)
    return binary


def encodeGUI(bitString, imagePath, savePath):
    """This function is used for
    encoding a message into an image
    and is used by the stegGui.py file
    to perform encoding through the GUI"""
    image = Image.open(imagePath)
    image = image.convert("RGB")
    width, height = image.size

    bitString = bitConversions(bitString, width, height)

    imageCpy = image                # create a copy of the image for modifying
    pixels = imageCpy.load()        # List of the pixels in the image
    b = 0                           # to iterate through bitString
    length = len(bitString)         # length of message

    for w in range(0, width):
        for h in range(0, height):
            # The following is performed for the R, G, B values per pixel
            for x in range(0, 3):
                # Check to see if we've finished encoding the message.
                if b == length:
                    # Save the image in the location specified(savePath)
                    imageCpy.save(savePath)
                    return

                # Since we haven't finished, we can begin encoding
                color = pixels[w, h]  # get a tuple of the RGB value at a given pixel.
                if bitString[b] == "1":
                    if color[x] % 2 == 0:
                        # our color has an even value, add one to make it odd
                        rgbList = list(color)
                        rgbList[x] += 1
                        pixels[w, h] = tuple(rgbList)  # set the new pixel values
                else:
                    if color[x] % 2 == 1:
                        rgbList = list(color)
                        rgbList[x] -= 1
                        pixels[w, h] = tuple(rgbList)  # set pixel values
                b += 1


def bitConversions(text, width, height):
    """This function takes a string in
    ASCII, and performs all the neccesary
    computation to convert it into a usable
    binary string, including appending the
    null termination byte so the decode
    function knows where to stop reading."""
    bitString = textToBinary(text)

    # Check if the message is too long to fit inside the image
    totalBits = len(bitString)          # total number of bits in the message
    totalPixels = width * height        # total numbers of pixels in the image
    bitMax = totalPixels * 3            # total number of bits that can fit in the image(3 per pixel)

    # The new bit string is a sub string that includes as many characters that can fit
    # in the image, plus the null termination bits used in decoding the message.
    if (totalBits + 9) > bitMax:
        print("Message is too long and will be truncated to fit")
        bitString = bitString[0:bitMax - 9]

    # append on the null termination byte to the end of the binString (00000000)
    bitString += "00000000"
    return bitString

def decodeGUI(imagePath):
    """This function is used for
    decoding the message hidden inside a
    previously encoded image. It is used by
    the GUI program."""
    image = Image.open(imagePath)
    image = image.convert("RGB")
    width, height = image.size

    message = ""
    zeroCounter = 0                 # This variable is used to detect the null termination byte
    pixels = image.load()
    for w in range(0, width):
        for h in range(0, height):
            color = pixels[w, h]    # get a tuple of the RGB values at a given pixel.
            for x in range(0, 3):
                bit = color[x]
                if zeroCounter == 8:
                    """
                    The decode function reads pixels in the image until it
                    encounters the null termination byte, which signifies that
                    it has read the entire message. First, check to make sure
                    the total length of the message is a multiple of 8. If it isn't,
                    some of the bits might have been cut off before reaching the null
                    termination character. In this case, we pad with 0's on the right
                    to reach a multiple of 8, and then convert the bit string back into
                    ASCII.
                    """
                    pad = len(message) % 8
                    if pad != 0:
                        zeros = 8 - pad     # number of zeros needed to pad message
                        message += '0' * zeros
                    message = convertFromBinary(message)
                    return message

                message += str(bit % 2)
                if bit % 2 == 0:
                    zeroCounter += 1
                else:
                    zeroCounter = 0

def convertFromBinary(string):
    """This is a helper function
    designed to convert a string from
    binary into the corresponding ASCII
    string"""

    # Convert the int into the corresponding ASCII symbols and return
    return ''.join(chr(int(string[i:i + 8], 2)) for i in range(0, len(string), 8))

# End of function definitions



