#!/usr/bin/env python3
from scripts.r2c import rbin

#import r2pipe


def main(filename=None):
    if filename == None:
        return 0
    r2 = rbin(filename)
    data=r2.get_info()
    return data


if __name__=="__main__":
    main()
