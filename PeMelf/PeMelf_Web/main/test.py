#!/usr/bin/env python3

def write_file():

    with open("write.txt","w") as f:
        f.write("The test worked")


if __name__ == "__main__":
    print(__name__)
    write_file()
