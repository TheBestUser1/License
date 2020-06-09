from scripts.vmc import vm
from scripts.r2c import rbin
import os,hashlib
import time
#from vmc import vm

CSRFtoken,root_path=None,None


def hash_file(filename):
    with open(filename,"rb") as f:
        file = f.read()
        hash_of_file = hashlib.md5(file).hexdigest()
        return hash_of_file

def debug_binary(data,r2,filename):
    allocated_p=[]

    r2.auto_analyze()
    entry = r2.get_entry()
    r2.set_breakpoint(entry)
    current = r2.get_current()
    while current != entry:
        r2.con()
        current = r2.get_current()


    VirtualAlloc = r2.get_addres_of_api("KERNELBASE.dll","VirtualAlloc")
    VirtualProtect = r2.get_addres_of_api("KERNELBASE.dll","VirtualProtect")
    breakpoint()
    ret_virtual_alloc = r2.get_ret_addres_from_api(VirtualAlloc)
    r2.set_breakpoint(ret_virtual_alloc)
    r2.set_breakpoint(VirtualProtect)

    while True:
        if allocated_p !=[]:
            for addr in allocated_p:
                dump = r2.examine_addr(addr,200)
                if "This" in dump:
                    size_to_dump = r2.get_size_m_map(addr)
                    path_to_dump = os.path.join(root_path,f"{addr}_{filename}")
                    r2.get_obj().cmd(f"wtf {path_to_dump} {size_to_dump} @ 0x{addr}")

        r2.con()
        current = r2.get_current()
        if current == ret_virtual_alloc:
            allocated_p.append(r2.get_eax())


def main(request=None,filename=None):
    global CSRFtoken,root_path
    CSRFtoken = request.COOKIES['csrftoken']
    root_path = os.path.join(os.path.abspath("."),"scripts/dumps")
    hash =hash_file(filename)


    a = vm("cata","192.168.142.131","scripts/keys/windows")
    a.upload_file(filename,hash)
    a.start_r_debug(f".\\Desktop\\malwares\\{hash}")
    time.sleep(2)

    r2 = rbin("http://192.168.142.131:1337")
    data = r2.get_info()
    debug_binary(data,r2,filename)
    return data

if __name__=='__main__':
    main()
