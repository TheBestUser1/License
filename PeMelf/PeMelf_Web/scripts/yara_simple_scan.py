#!/usr/bin/env python3
import os
import json
import r2pipe



def main(filename=None):
    if filename == None:
        return 0
    r2 = r2pipe.open(filename)
    data = json.loads(r2.cmd('iaj'))
    return data['info']


if __name__=="__main__":
    main()
