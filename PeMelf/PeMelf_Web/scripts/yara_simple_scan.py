#!/usr/bin/env python3
from scripts.r2c import rbin
#for debugg
#from r2c import rbin
import os
#import r2pipe

def read_rules(r2):
    r = r2.get_obj()
#    (r.cmd("yara add {}".format(os.path.join("./yara.r",f)) for f in os.listdir("./yara.r") if os.path.isfile(os.path.join("./yara.r",f)))
    for f in os.listdir("scripts/yara.r"):
        path = os.path.join("scripts/yara.r",f)
        if os.path.isfile(path)==True:
            r.cmd("yara add {}".format(path))
    return r


def scan(r2,data):

    data_yara=r2.cmd("yara scan").split("\n")
    del data_yara[-1]
    data['results']=data_yara
    return data






def main(request=None,filename=None):
    if filename == None:
        return 0
    r2 = rbin(filename)
    data=r2.get_info()

    r2=read_rules(r2)
    return scan(r2,data)

if __name__=="__main__":
    main("../files/pe2.exe")
