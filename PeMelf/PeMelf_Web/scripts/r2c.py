#!/usr/bin/env python3
import os,sys
import json
import r2pipe

#sys.stderr=object

class rbin:

    def __init__(self,file):
        self.r2=r2pipe.open(file,['-2'])
        self.file = file

    def get_info(self): #it builds a json with infos from a binary
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

    def check_addr(self,addr):#it checks if an value is an address or not
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


        occurences = self.r2.cmd("axt @ {}~[1]".format(addr)).strip("\n").split("\n")#it looks for occurences of a function in assembly or whatever address or hash is given


        return occurences

    def find_args(self,addr,blob):       #finds args of a function in assembly (it's just for x86 and cdecl , it searches for pushes)
        if self.check_addr(addr):

            block_function=self.r2.cmd("pd @ {}-32~push,call[4]".format(addr))
            function = block_function.strip('\n').split('\n')
            function.reverse()
            if bool(blob)==False:
                addr = self.find_occurence(function[0])[0]
 #               breakpoint()
                if addr == '':
                    return None

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

    def find_function(self,addr):#it goes in findding functions job
        blob={}
        blob=self.find_args(addr,blob)
        if blob is None:
            return None
        occurences = self.find_occurence(next(iter(blob)))
        for i in range(1,len(occurences)):
            blob=self.find_args(occurences[i],blob)
        return blob

    def con(self):
        self.r2.cmd("dc")

    def auto_analyze(self):
        self.r2.cmd("aaa")

    def set_breakpoint(self,breakpoint):
        self.r2.cmd(f"db {breakpoint}")

    def get_current(self):
        return self.r2.cmd("s").strip("\n")

    def get_entry(self):
        return self.r2.cmd("ie~:0[1]").strip("\r\n")

    def get_addres_of_api(self,dll,api):
        apis = self.r2.cmd(f"dmi {dll}~{api}").split("\r\n")
        addr = ''
        for i in apis:
            new_i = i.split(" ")
            new_i[-1] = new_i[-1].strip("\r")
            if new_i[-1] == api:
                addr= new_i[3]
                return addr
        return None

    def get_ret_addres_from_api(self,api):
        self.r2.cmd(f'db -{api}')
        addr_ret=self.r2.cmd(f"pd @ {api}~ret:0[1]").strip("\r\n") #maybe it prints another value insted of addres

        return addr_ret

    def get_ax(self):
        return self.r2.cmd("dr~ax[1]").strip("\r\n")

    def examine_addr(self,addr,size):
        return self.r2.cmd(f"pxw {size} @ {addr}")

    def get_size_m_map(self,addr):
        addr= addr[2:]
        search_v = '0x'+'0'*(16-len(addr))+addr
        v_range = self.r2.cmd(f"dm~^{search_v}[0,2]").strip("\r\n")
        v_range = v_range.split(" ")
        to_dump = int(v_range[1],16)-int(v_range[0],16)
        return to_dump


def main(filename=None):
    r2 = rbin(filename)
    return r2.get_info()

if __name__=='__main__':
    main("../files/pe2.exe")
