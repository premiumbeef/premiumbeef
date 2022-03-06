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
