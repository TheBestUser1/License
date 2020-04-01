#!/usr/bin/env python3
import r2pipe
import os



registers = {'eax':'','ebx':'','ecx':'','edx':'','ebp':'','esp':'','edi':'','esi':'','eip':''}


def proc_lines(col,ref,ops):
    if ref[0] in col:
        if 'mov' in col[0] :
            if  ('dword' in col[2])
                ref[0] = col[1]
                ref[1] = 1
            elif ('byte' in col[2]) :
                ref[0] = col[1]
                ref[1] = 0
            elif ('byte' in col[1]):
                ref[0] = col[2]

#you have to treat casses like this and go on ... 
        elif 'add' in col[0]:
            if col[1]==ref[0]:
                if ref[1]==0:
                    ops[ref[2]]+='+ '
        elif 'sub' in col[0]:
            if col[1]==ref[0]:
                if ref[1]==0:
                    ops[ref[2]]+='- '
    return ref


def find_logic(r2,f):
    
    
    r2.cmd("s {}".format(f))    
    
    args = r2.cmd('afvb~arg[2]').split("\n")
    del(args[-1])
    operations = dict.fromkeys(args,'')

    for i in args:
        addr_of_read = r2.cmd("afvR {}~[1]".format(i)).strip("\n")
        read_inst = ''
        j =1
        ref = [i,1,i]

        while read_inst !='ret':
            breakpoint()
            read_inst = r2.cmd("pd {} @ {}~:{}[3-6]".format(j,addr_of_read,j-1)).strip("\n")
            line = read_inst.split(" ")
            
            ref = proc_lines(line,ref,operations)
            j+=1
            

    


    return 0





def main():
    r2 = r2pipe.open("../files/pe3packed.exe")
    function="fcn.00404520"
    r2.cmd('aaa')
    find_logic(r2,function)


if __name__=='__main__':
    main()
