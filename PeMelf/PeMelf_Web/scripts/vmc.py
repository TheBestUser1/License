import os,time
import subprocess, shlex
nr_of_conection=0

class vm:

    def __init__(self,user,host,key):
        global nr_of_conection
        self.connection_id =nr_of_conection +1
        nr_of_conection = self.connection_id
        self.host = host
        self.key = key
        self.user = user

    def get_con_id(self):
        return self.connection_id

    def start_r_debug(self,file):
        #r2 -c ' e http.bind=0.0.0.0;e http.sandbox=0;e http.root="C:\Users\cata\Desktop\radare2\radare2-vs2017_64-4.3.1\share\www";=h& 1337'
        command = f"powershell Start-Process .\\Desktop\\server.bat {file} -Wait"
        command_f = f"ssh -i {self.key} {self.user}@{self.host} \"{command}\""
        command_f = shlex.split(command_f)
        pid = subprocess.Popen(command_f)

    def upload_file(self,file):
        return 0