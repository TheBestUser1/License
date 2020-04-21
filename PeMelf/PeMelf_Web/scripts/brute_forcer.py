#!/usr/bin/env python3
import os, logging
from queue import Queue
from threading import Thread

continue_threads=1
root_path=''
def brute_f(buffer,lims):

    for brute_v in range(lims[0],lims[1]):


        global continue_threads
        if continue_threads is 0:
            break
        decrypted=''

        for i in range(len(buffer)): # the down line is written dynamically
            decrypted+=chr(0xff&buffer[i] - brute_v - i)
        if 'This'in decrypted:
            print(brute_v)
            with open(os.path.join(root_path,lims[2]),"w") as d:
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

def main(byte=None,name_of_file=None):
    if  byte ==None:
        return 0
    global root_path
    root_path=os.path.join(os.path.abspath("."),"scripts/dumps")

    queue = Queue()
    for x in range(8):
        worker =Brute(queue)
        worker.daemon=True
        worker.start()
    #breakpoint()
    for i in range(8):
        queue.put((byte,[i*32,(i+1)*32,name_of_file]))
    queue.join()

if __name__=='__main__':
    main()
