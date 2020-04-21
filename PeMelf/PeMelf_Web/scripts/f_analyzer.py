#!/usr/bin/env python3
import r2pipe
import os
import re,sys
import importlib.util



regex_signs = '[\-+^*/]'

def signe_test(signe,line):
    if signe:
        signe = signe.group()
    else:
        line=line.replace(pointer.group(),'buffer')
    return signe,line

def proc_lines(char_lines,operations):

    for i in char_lines:
        still_line = 1
        while still_line:
            pointer=re.search("\*\(char \*\)\(.*?\) ",i)

           #check for pointer increment (in this way we find our interest var)
            if pointer is not None:

                values = re.sub("\*\(char \*\)\(",'',pointer.group()).strip(") ")

                signe = re.search(regex_signs,values)


                signe,i=signe_test(signe,i)

                if signe:
                    argv = values.split(signe)
                    argv=[i.strip(' ') for i in argv]
                    if operations.get('buffer') is None:
                        operations['buffer']={}
                        operations['buffer']['last_time']=argv[0]
                        operations['buffer']['type']='element_buffer'
                        operations['buffer']['index']=argv[1]
                        operations['buffer']['decrypt']='buffer[i]'
                        del operations[argv[0]]
                    i = i.replace(pointer.group(),'buffer')

            pointer=re.search("\(buffer.*?\).*?\) ",i)
            if pointer is not None:

                signe = re.search(regex_signs,pointer.group())
                signe,i = signe_test(signe,i)

                if signe:
                    argv = pointer.group().split(signe)
                    argv =[i.strip(' ') for i in argv]
                    argv_1 = re.sub("\(.*?\)",'',argv[1]).strip(") ")
                    if argv_1:
                        argv[1]=argv_1

                    #here we should see in future if argv[1] is modified not just a parameter
                    if argv[1] in operations:
                        operations['buffer']['decrypt']+=' {} {}'.format(signe,'brute_v')
                    elif argv[1]==operations['buffer']['index']:
                        operations['buffer']['decrypt']+=' {} {}'.format(signe,'i')
                    i=i.replace(pointer.group(),'buffer')

            pointer=re.search("buffer.*?$",i)
                    #here we parse the last thing from command
            if pointer is not None:

                signe = re.search(regex_signs,pointer.group())
                signe,i = signe_test(signe,i)

                if signe:
                    argv = pointer.group().split(signe)
                    argv = [i.strip(' ') for i in argv]
                    argv_1= re.sub("\(.*?\)",'',argv[1])
                    if argv_1:
                        argv[1]=argv_1
                    argv[1]=argv[1].strip(";")
                    if argv[1] in operations:
                        operations['buffer']['decrypt']+=' {} {}'.format(signe,'brute_v')
                    elif argv[1]==operations['buffer']['index']:
                        operations['buffer']['decrypt']+=' {} {}'.format(signe,'i')
                    i=i.replace(pointer.group(),'buffer')

            still_line=0
    return operations


def find_logic(r2,f):#find decrypt function logic

    r2.cmd("s {}".format(f))
    args = r2.cmd('afvb~arg[2]').split("\n")
    del(args[-1])
    operations = dict.fromkeys(args)
    decomp = r2.cmd('pdg').split('\n')
    char_lines = [ x.strip(" ") for x in decomp if 'char' in x]
    operations=proc_lines(char_lines,operations)

    return operations['buffer']['decrypt']




    return 0





def main(function,r2,name_of_file,byte,decrypt_logic=None): #it takes just a bin and a function adrees
    #r2 = r2pipe.open("../files/pe3packed.exe")
    #function="fcn.00404520"
    #r2.cmd('aaa')
    root_path=os.path.join(os.path.abspath("."),"scripts")
    if decrypt_logic is None:
        decrypt_logic=find_logic(r2,function)
    
    if 'brute_v' in decrypt_logic:
        with open(os.path.join(root_path,"brute_forcer.py"),"r") as br:
            lines = br.readlines()
            up_space = len(lines[17])-len(lines[17].lstrip(" "))
            lines[18]=(up_space+4)*" "+"decrypted+=chr(0xff&{})\n".format(decrypt_logic)
            br.close()
        with open(os.path.join(root_path,"brute_forcer.py"),"w") as br:
            br.writelines(lines)
            br.close()
        
        file_path=os.path.join(root_path,"brute_forcer.py")
        module_name ="brute_forcer"
        spec = importlib.util.spec_from_file_location(module_name,file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        module.main(byte,name_of_file)
    return decrypt_logic

if __name__=='__main__':
    #breakpoint()
    main()
