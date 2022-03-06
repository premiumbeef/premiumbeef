# Follow The Breadcrumbs

- Type  : Forensics
- Points: 200

## Description
I've acquired a USB from the K9's. Luckily for us, those mongrels fail at basic operational security. Attached to the USB is a note that reads, "secret key in picture". The file inside doesn't appear to be a picture, though. Why don't you take a look and let me know what you can extract?

## Hints
You found this file on a flash drive with a sticky note on it which says "Secret key in picture." It doesn't seem to be a picture, though...this might take a while...

## Solutions
The general approach to solving this is to recursively decompress the file and convert all the "bytes" into a binary file. Once we decompress the final archive, we are given a few files. The flag is hidden in the image file using the `stego_ctf.py` script and it is a one-way steganography. We need to reverse the script and extract the flag ourselves.

1. Since we are given a "breadcrumbs.tar.bz2" file, we will extract it with `bzip2 -d breadcrumbs.tar.bz2`
2. After decompressing the bz2 file, we obtained the "breadcrumbs.tar" file. Extracting this TAR file, you will noticed that it extracted into a "data.tar" and a "4" file. 
3. If you continue to extract the "data.tar" you will realised that it is a giant tarball except that you will get a different byte along with the extracted "data.tar".
4. If you observe the order of the file extracted, you will see that the first 6 files extracted form "\x42\x5A\x68" which is conincidentally (or not) the magic header for a bzip2 file. 
5. Assuming that the recursive extracting of file will give us a bzip2 file, i wrote a script to append all the extracted bytes into a binary file. (Note! It will take some time to run)
6. Running `file output.bin` indeed shows us that it is a bzip2 compressed file. 
7. We now change the file extension of `output.bin` to `output.tar.bz2` and extract it. We should see a folder called "inner" with 3 files: `stego_ctf.py`, `new_cat.png` and `commit_message.tmp`
8. The `commit_message.tmp` says that the secret is embedded in the image, but the user doesnt remember what parameters were used. Luckily, they provided the stego python script, so we can reverse the logic of it!
9. After looking at the code, i wrote another script to extract the embedded secret inside the image. However, the user could have embedded the message in any of the bit position (0 to 7), so we will need to do a trial and error. 
10. Running the script, you should see the flag when the POS is at 6!

**FLAG: ATR[Say hello to my little friend]**

## After Thoughts
Intially when i ran the decompression script, i was not sure if that was the correct approach to it since it was taking quite a bit of time. When the first `output.bin` was extracted, i was also not able to decompress it due to some corrupted bytes when i was saving it into a file. So after taking a short break, i modified the script again and i managed to decompress the final archive! (Sadly, that was not the end of it)
Luckily, the `stego_ctf.py` script was rather easy to reverse. 

## Scripts

**Decompression Script**
```python
#!/usr/bin/python3
import os
import subprocess

def save(strings):                                                              # save to binary file if completed
    print(strings)
    try:
        output = bytes.fromhex(strings)                                             # convert to hex value
    except:
        output = strings
    print("Writing to file")
    f = open("output.bin", "wb")
    f.write(output)
    f.close()

def main():
    strings = ""
    count = 0
    zero_count = 0
    try:
        if "breadcrumbs.tar" in os.listdir("."):                                # check if breadcrumbs.tar is in folder
            file = 'breadcrumbs.tar'
            output = os.popen('tar -xvf {}'.format(file)).read()                # extract it and save output in "output"
            strings += output[0]                                                # append the file as string
            while True:
                count += 1
                if zero_count > 30:                                             # might not terminate until user ctrl+c
                    print("More than 30 bytes of \\x00 has been written!")
                    f.close()
                    save(strings)
                    break
                #if count == 20:
                #    print(strings)
                #    count = 0
                file = "data.tar"
                if os.path.isfile(file):                                        # if "data.tar" exist
                    output = os.popen('tar -xvf {}'.format(file)).read()        # extract it and save output in "output"
                    if output[0] == 0:                                          # take note if the output is 0
                        zero_count += 1
                    strings += output[0]                                        # append the file as string
                else:
                    f.close()
                    save(strings)
                    break
    except KeyboardInterrupt:
        save(strings)

if __name__ == "__main__":
    main()
```

**Reverse Stego Script**
```python
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
```
