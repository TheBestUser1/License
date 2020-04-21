#!/usr/bin/env python3
import os, logging
from queue import Queue
from threading import Thread

continue_threads=1
_locals = locals()
def brute_f(buffer,lims):

    for brute_v in range(lims[0],lims[1]):


        global continue_threads
        if continue_threads is 0:
            break
        decrypted=''

        for i in range(len(buffer)):
            decrypted+=chr(0xff&buffer[i] - brute_v - i)
        if 'This'in decrypted:
            print(brute_v)
            with open("out_file.bin","w") as d:
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

def main(expr=None):
    if expr == None:
        return 0
    path = os.path.join("dumps","32aecddc3d01f81d3f803501fc2a07ff")
    with open(path,"rb") as d:
        byte=d.read()

    queue = Queue()
    for x in range(8):
        worker =Brute(queue)
        worker.daemon=True
        worker.start()
    #breakpoint()
    for i in range(8):
        queue.put((byte,[i*32,(i+1)*32,expr]))
    queue.join()

if __name__=='__main__':
    main()
