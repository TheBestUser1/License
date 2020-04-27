#!/usr/bin/env python3
import os, logging
from queue import Queue
from threading import Thread
import scripts.db_updater as db
continue_threads=1
root_path,token='',''
def brute_f(buffer,lims):

    for brute_v in range(lims[0],lims[1]):


        global continue_threads
        if continue_threads is 0:
            break
        decrypted=''

        for i in range(len(buffer)): # the down line is written dynamically
            decrypted+=chr(0xff&buffer[i] - brute_v - i)
        if 'This'in decrypted:
            path_to_file = os.path.join(root_path,lims[2])
            db.update_db_file(lims[2],root_path,token)
            with open(path_to_file,"w") as d:
                d.write(decrypted)
            continue_threads=0


class Brute(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue=queue

    def run(self):

        while True:
            byte, lims = self.queue.get()
            try:
                brute_f(byte,lims)
            finally:
                self.queue.task_done()

def main(CSRFtoken=None,byte=None,name_of_file=None,threads=8):
    if  byte ==None:
        return 0
    global root_path,token
    root_path=os.path.join(os.path.abspath("."),"scripts/dumps")
    token=CSRFtoken
    queue = Queue()
    for x in range(threads):
        worker =Brute(queue)
        worker.daemon=True
        worker.start()
    #breakpoint()
    if threads==8:
        for i in range(threads):
            queue.put((byte,[i*32,(i+1)*32,name_of_file]))
    elif threads==1:
        queue.put((byte,[0,1,name_of_file]))
    queue.join()

if __name__=='__main__':
    main()
