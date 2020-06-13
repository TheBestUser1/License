from scripts.vmc import vm
from scripts.r2c import rbin
import os,hashlib
import time,json
import scripts.db_updater as db
import scripts.yara_simple_scan as yr
#from vmc import vm

CSRFtoken,root_path=None,None


def hash_file(filename):
    with open(filename,"rb") as f:
        file = f.read()
        hash_of_file = hashlib.md5(file).hexdigest()
        return hash_of_file

def debug_binary(data,r2,filename,conex):
    allocated_p=[]

    r2.auto_analyze()
    entry = r2.get_entry()
    r2.set_breakpoint(entry)
    current = r2.get_current()

    while int(current,16) != int(entry,16):
        r2.con()
        current = r2.get_current()


    VirtualAlloc = r2.get_addres_of_api("KERNELBASE.dll","VirtualAlloc")
    VirtualProtect = r2.get_addres_of_api("KERNELBASE.dll","VirtualProtect")

    ret_virtual_alloc = r2.get_ret_addres_from_api(VirtualAlloc)
    r2.set_breakpoint(ret_virtual_alloc)
    r2.set_breakpoint(VirtualProtect)

    always = 1
    while always:

        r2.con()
        current = r2.get_current()
        if current == ret_virtual_alloc:
            allocated_p.append(r2.get_ax())


        if current == VirtualProtect:
            if allocated_p !=[]:
                for addr in allocated_p:
                    dump = r2.examine_addr(addr,200)
                    if "DOS" in dump:
                        size_to_dump = r2.get_size_m_map(addr)
                        win_path_to_dump = f"Desktop/malwares/dumps/{addr[2:]}_{filename}"
                        r2.get_obj().cmd(f"wtf {win_path_to_dump} {size_to_dump} @ {addr}")
                        conex.get_file(win_path_to_dump,root_path)
                        time.sleep(2)
                        db.update_db_file(f"{addr[2:]}_{filename}",root_path,CSRFtoken)

                        r3=rbin(os.path.join(root_path,f"{addr[2:]}_{filename}"))
                        r3.auto_analyze()
                        r3=yr.read_rules(r3)

                        data_s = json.loads(r3.cmd("ij"))
                        item_l = {'file_arch':data_s['bin']['arch'],'file_class':data_s['bin']['class']}
                        item_l = yr.scan(r3,item_l)
                        
                        data['info_dumps'].append(item_l)

            always = 0


    return data
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
    data['info_dumps'] = []
    data = debug_binary(data,r2,hash,a)
    return data

if __name__=='__main__':
    main()
