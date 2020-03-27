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

    def get_obj(self):
        return self.r2

    def check_addr(self,addr):
        if self.r2.cmd("pd 1 @ {}~invalid".format(addr))=='':
            return True
        return False

    def is_number(self,s):
        try:
            int(s,base=16)
            return True
        except ValueError:
            return False

    def find_occurence(self,addr):
        occurences = self.r2.cmd("axt @ {}~[1]".format(addr)).strip("\n").split("\n")
        return occurences

    def find_args(self,addr,blob):
        if self.check_addr(addr):
            block_function=self.r2.cmd("pd @ {}-32~push,call[4]".format(addr))
            function = block_function.strip('\n').split('\n')
            function.reverse()
            if bool(blob)==False:
                addr = self.find_occurence(function[0])[0]
                blob[function[0]]={addr:{}}
            else:
                blob[function[0]][addr]={}

            blob[function[0]][addr]['adress']=[]
            blob[function[0]][addr]['values']=[]

            for i in range(1,len(function)-1):

                if(self.check_addr(function[i])):
                    blob[function[0]][addr]['adress'].append(function[i])
                else:
                    if self.is_number(function[i]):
                        blob[function[0]][addr]['values'].append(function[i])
        return blob

    def find_function(self,addr):
        blob={}
        blob=self.find_args(addr,blob)
        occurences = self.find_occurence(next(iter(blob)))
        for i in range(1,len(occurences)):
            blob=self.find_args(occurences[i],blob)
        return blob



def main(filename=None):
    r2 = rbin(filename)
    return r2.get_info()

if __name__=='__main__':
    main("../files/pe2.exe")
