#!/usr/bin/env python3
from scripts.r2c import rbin
#it's just in buillding stage :D
#from r2c import *
import hashlib
import os
import sys
#import f_analyzer as f_a #here I think I should say import scripts.f_analyzer
import scripts.f_analyzer as f_a
import scripts.db_updater as db
import json

root_path=''
CSRFtoken,logic=None,None
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
    function = next(iter(refs))

    #dumps=[]
#    breakpoint()
#dumping packed bytes
    global logic
    for i in refs[function]:
        addr=refs[function][i]['adress'][0]
        value=refs[function][i]['values'][0]
        path_to_dump=os.path.join(root_path,"{}_{}".format((r2.cmd("i~:1[1]")\
                                        .split("/")[-1].strip("\n")),addr))
        bin = r2.cmd("wtf {} {} @ {}".format(path_to_dump,value,addr))
        name_of_file=''

        with open(path_to_dump,"rb") as f:
            file = f.read()
            hash_of_file = hashlib.md5(file).hexdigest()
            name_of_file = os.path.join(root_path,"{}".format(hash_of_file))
            os.rename(path_to_dump,name_of_file)
     #       dumps.append(name_of_file)

            db.update_db_file(name_of_file,root_path,CSRFtoken)
            logic=f_a.main(function,r2,"unpacked_"+hash_of_file,file,CSRFtoken,logic)
#trying to figure out decrypt functioni

    data = json.loads(r2.cmd("pdgj"))['code']
    entry_dis_f = {'function_offset':function,'code':data}

    return entry_dis_f



def find_bin(r2,dissasembly_functions):

    r_obj=r2.get_obj()
    r_obj.cmd("aaa")
    data_sections = r_obj.cmd("ax~section..data").strip(" ").split(" ")
    data_serialized = [f for f in data_sections if f!='']
    refs = find_refs(data_serialized)



    for i in refs:
        try:
            f_refs = r2.find_function(i) #it finds occurences of a function and if an adress and and offset is
            #breakpoint()                        #passed to that function here I should check for that dictionary to do the magic
            if f_refs is None:
                continue
            breakpoint()
            dissasembly_functions['function'].append(proc_f(f_refs,r_obj))

        except:
            pass
        #here we treat the function and try to export everything from
        #data section
    return dissasembly_functions


def main(request=None,filename=None):
    global root_path,CSRFtoken
    CSRFtoken = request.COOKIES['csrftoken']
    root_path=os.path.join(os.path.abspath('.'),"scripts/dumps")
    if filename == None:
        return 0
    r2 = rbin(filename)

    data = r2.get_info() #it has just info of bin file
    data['function']=[]

    bin_data = find_bin(r2,data) #after processing the bin it has also some code of decompiled functions
    return bin_data



if __name__=='__main__':
    main("../../../Malware_samples/WinEXE/pe3packed.exe")
