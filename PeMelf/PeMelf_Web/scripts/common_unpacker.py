#!/usr/bin/env python3
#from scripts.r2c import rbin
from r2c import *
import hashlib
import os

def find_refs(data):
    i = 1
    j = 5
    length = len(data)
    refs = {}
    while i < length and j <length:
        refs[data[i]]=data[j]
        i+=7
        j+=7
    return refs

def find_function_refs(data,r2):
    ref_use = r2.cmd("pd ".format(data))

    return ref_use

def proc_f(refs,r2):
    key = next(iter(refs))
    breakpoint()
    dumps=[]

#dumping packed bytes
    for i in refs[key]:
        addr=refs[key][i]['adress'][0]
        value=refs[key][i]['values'][0]
        path_to_dump=os.path.join("dumps","{}_{}".format((r2.cmd("i~:1[1]")\
                                        .split("/")[-1].strip("\n")),addr))
        bin = r2.cmd("wtf {} {} @ {}".format(path_to_dump,value,addr))
        name_of_file=''
        with open(path_to_dump,"rb") as f:
            file = f.read()
            hash_of_file = hashlib.md5(file).hexdigest()
            name_of_file = os.path.join("dumps","{}".format(hash_of_file))
            os.rename(path_to_dump,name_of_file)
            dumps.append(name_of_file)

#trying to figure out decrypt function

    

    return True



def find_bin(r2):

    r_obj=r2.get_obj()
    r_obj.cmd("aaa")
    data_sections = r_obj.cmd("ax~section..data").strip(" ").split(" ")
    data_serialized = [f for f in data_sections if f!='']
    refs = find_refs(data_serialized)
    for i in refs:
        f_refs = r2.find_function(i)
        proc_f(f_refs,r_obj)

        #here we treat the function and try to export everything from
        #data section



def main(filename=None):
    if filename == None:
        return 0
    r2 = rbin(filename)
    data = r2.get_info()

    bin_data = find_bin(r2)
    return data


if __name__=='__main__':
    main("../files/pe3packed.exe")
