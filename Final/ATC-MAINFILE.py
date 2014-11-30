import os
import threading
import time
def kk():
    os.system('atc_changed.py')
def jj():
    os.system('mouseclick_changed.py')


t0=threading.Thread(target=kk,args=())
t0.start()
time.sleep(0.5)
t1=threading.Thread(target=jj,args=())
t1.start()

while (True):
    pass


