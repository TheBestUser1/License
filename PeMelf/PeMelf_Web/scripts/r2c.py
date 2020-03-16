#!/usr/bin/env python3
import os
import json
import r2pipe

class rbin:

    def __init__(self,file):
        self.r2=r2pipe.open(file)
        self.file = file

    def get_info(self):
        data = json.loads(self.r2.cmd("ij"))
        data_f={"info":{}}
        data_f['info']['file']=self.file.split("/")[-1]
        data_f['info']['bintype']=data['bin']['bintype']
        data_f['info']['arch']=data['bin']['arch']
        data_f['info']['bits']=data['bin']['bits']
        data_f['info']['canary']=data['bin']['canary']
        data_f['info']['nx']=data['bin']['nx']
        data_f['info']['machine']=data['bin']['machine']
        data_f['info']['os']=data['bin']['os']
        data_f['info']['pic']=data['bin']['pic']
        data_f['info']['relocs']=data['bin']['relocs']
        data_f['info']['stripped']=data['bin']['stripped']
        

        data_f["imports"]=[]
        imports = json.loads(self.r2.cmd("iij"))
        for i in imports:
            data_f["imports"].append(i['name'])

        return data_f





def main(filename=None):
    r2 = rbin(filename)
    return r2.get_info()

if __name__=='__main__':
    main("../files/pe2.exe")
