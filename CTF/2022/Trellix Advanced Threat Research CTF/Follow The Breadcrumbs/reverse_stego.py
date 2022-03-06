#!/usr/bin/python3
import bitarray
from bitarray.util import int2ba, ba2int
import sys
from PIL import Image
import math

def extract(im, pixels, pos):
    bits = bitarray.bitarray()              # create an empty bitarray to store binary
    for i in range(len(pixels)):            # loop through each pixels
        r,g,b = pixels[i]                   # get the RGB values of each pixels
        br = int2ba(r, 8)                   # convert values to binary
        bg = int2ba(g, 8)                   # convert values to binary
        bb = int2ba(b, 8)                   # convert values to binary

        vr = br[pos]                        # get the specific binary bit at the position
        vg = bg[pos]                        # get the specific binary bit at the position
        vb = bb[pos]                        # get the specific binary bit at the position

        bits.append(vr)                     # append binary bit to bitarray
        bits.append(vg)                     # append binary bit to bitarray
        bits.append(vb)                     # append binary bit to bitarray

    print(bits.tobytes())                   # convert the binary to bytes

def main():
    im =  Image.open("new_cat.png")         # open image file
    pixels = im.getdata()                   # get image as pixel data
    for pos in range(7, -1, -1):            # loop through position from 7 to 0
        print("POS: {}\n".format(pos))
        extract(im, pixels, pos)
        print("\n")

if __name__ == "__main__":
    main()
