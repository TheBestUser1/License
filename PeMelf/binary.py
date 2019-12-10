#!/usr/bin/env python3

import r2pipe


class Binar:
    def __init__(self,name):
            
        self.r = r2pipe.open(name)
        self.r.cmd("aaa")

    def find_main(self):
        print(self.r.cmd("pdf @ main"))

        

