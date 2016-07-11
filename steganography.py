"""
This program takes an image file and a message from the user
and transcribes the message into a new version of the image
using the parity of the RGB values within the image. The user
can request to encode a message into an image given an
appropriate path, or decode a message that has already
been encoded into an existing image.

Author: David Letourneau, 6/29/2016
"""

from PIL import Image

# Function definitions

# Function for converting a text string into binary
def textToBinary(text):
   binary = ''.join(format(ord(x), 'b').zfill(8) for x in text)
   return binary

# Function for encoding the message into the image
def encode(bitString, image, width, height):
    pixels = image.load()           # List of the pixels in the image
    b = 0                           # to iterate through bitString
    length = len(bitString)         # length of message

    for w in range(0, width):
        for h in range(0, height):

            # The following is performed for the R, G, B values per pixel
            for x in range(0, 3):
                # Check to see if we've finished encoding the message.
                if b == length:
                    badSaveRequest = True
                    output = input(
                        "Where would you like this image to be saved? Enter a path ending with the desired file "
                        "name and format(png or bmp): ")
                    while badSaveRequest:
                        try:
                            image.save(output)
                            print("Your image has been saved in the location ", output)
                            badSaveRequest = False
                        except FileNotFoundError:
                            output = input("The requested path does not exist. Please try again: ")
                    return

                color = pixels[w, h]  # get a tuple of the RGB value at a given pixel.
                if bitString[b] == "1":
                    if color[x] % 2 == 0:
                        # our color has an even value, add one to make it odd
                        rgbList = list(color)
                        rgbList[x] += 1 # + 1
                        pixels[w, h] = tuple(rgbList)  # set the new pixel values
                else:
                    if color[x] % 2 == 1:
                        rgbList = list(color)
                        rgbList[x] -= 1 # - 1
                        pixels[w, h] = tuple(rgbList)  # set pixel values
                b += 1


# Function for decoding messages out of an image that has been encoded
def decode(image, width, height):
    message = ""
    zeroCounter = 0              # This variable is used to detect the null termination byte
    pixels = image.load()
    for w in range(0, width):
        for h in range(0, height):
            color = pixels[w, h]  # get a tuple of the RGB values at a given pixel.
            for x in range(0, 3):
                bit = color[x]
                if zeroCounter == 8:
                    """
                    The decode function reads pixels in the image until it
                    encounters the null termination byte, which signifies that
                    it has read the entire message. First, check to make sure
                    the total length of the message is a multiple of 8. If it isn't,
                    some of the bits might have been cut off before reaching the null termination
                    character. In this case, we pad with 0's on the right to reach
                    a multiple of 8, and then convert the bit string back into ASCII.
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

# Function to convert a binary string into an ASCII string
def convertFromBinary(string):
    # Convert the bit string into an int format
    # number = int(string, 2)

    # Convert the int into the corresponding ASCII symbols and return
    # return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode()
    return ''.join(chr(int(string[i:i + 8], 2)) for i in range(0, len(string), 8))


# End of function definitions

version = "V_2.3"

print("Steganography creator version", version, "\n")

# Ask the user if they wish to Encode a message or Decode from an image
request = ""
while request.lower() != "q" and request.lower() != "e" and request.lower() != "d":
    request = input("Would you like to encode a message onto an image or decode from an existing file? Please enter "
                "E to encode, D to decode, or Q to quit: ")

# Ask the user for the path to the image requested
badRequest = True
image = None
while badRequest:
    imagePath = input("Please enter the path to the image you would like to use or Q to quit: ")
    if imagePath.lower() == "q":
        # User has request to quit the program
        exit()
    try:
        # Attempt to use the path suggested & break out of while loop
        image = Image.open(imagePath)
        image = image.convert("RGB")
        width, height = image.size  # size properties of the image
        badRequest = False
    except FileNotFoundError:
        # User has entered a request for a file that cannot be found
        print("The file requested could not be found or does not exist")

# if the user selected encode, there is initial set up required below
if request.lower() == 'e':
    # Get the text the user wishes to embed within the image
    text = input("Please enter the text you wish to place within the image: ")
    binString = textToBinary(text)  # convert user's string to binary
    imageCpy = image                # create a copy of the image for modifying

    # Check if the message is too long to fit inside the image
    totalBits = len(binString)      # total number of bits in the message
    totalPixels = width * height    # total numbers of pixels in the image
    bitMax = totalPixels * 3        # total number of bits that can fit in the image(3 per pixel)



    # The new bit string is a sub string that includes as many characters that can fit
    # in the image, plus the null termination bits used in decoding the message.
    if (totalBits + 9) > bitMax:
        print("Message is too long and will be truncated to fit")
        binString = binString[0:bitMax - 9]

    # append on the null termination byte to the end of the binString (00000000)
    binString += "00000000"

    encode(binString, imageCpy, width, height)
else:
    # this block is used when the user requests decode
    width, height = image.size
    image = Image.open(imagePath)
    message = decode(image, width, height)
    print("Message is:", message)







