#from scripts.vmc import vm
#from scripts.r2c import rbin
from vmc import vm



def main():
    a = vm("cata","192.168.142.131","keys/windows")
    a.start_r_debug(".\\Desktop\\malwares\\redaman.exe")

if __name__=='__main__':
    main()
