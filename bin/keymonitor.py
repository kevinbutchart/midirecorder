#!/usr/bin/python3
import struct 
import subprocess 
import select
import signal
import os

def kill(proc_pid):
    os.killpg(os.getpgid(proc_pid), signal.SIGTERM) 

def readmouse(dev):
    data = f.read(3)  # Reads the 3 bytes 
    message = struct.unpack('3b',data)  #Unpacks the bytes to integers
    return message

def waitleftdown(dev, process):
    leftdown=False
    while True:
        r, w, e = select.select([ dev ], [], [], 0)
        if dev in r:
            message = readmouse(dev) 
            if message[0] == 9:
                leftdown = True
            if message[0] == 8:
                if leftdown:
                    break 
        if process is not None:
           retcode = process.poll()
           if retcode is not None:
              break     


f = open( "/dev/input/mice", "rb" ); 
# Open the file in the read-binary mode
while 1:
    waitleftdown(f, None) 
    process = subprocess.Popen("playlast.sh", shell=True, preexec_fn=os.setsid)
    waitleftdown(f, process)
    retcode = process.poll()
    if retcode is None:
        kill(process.pid)
        os.system("allnotesoff.sh")
        print("force stopped")
    else:
        print("stopped on own")
