import pylab as pl
import matplotlib.pyplot as plt 
import threading as thrd
import numpy as np
import signal
import time
import pygame,sys
from pygame.locals import *
from socket import *
import math


 
# Reocrd start time for calculating frame rate
tstart = time.time()
CHECK=4
HOST=''
PORT=21532
BUFSIZ=1024
ADDR = (HOST,PORT)
threads=[]
serversocket=socket(AF_INET, SOCK_STREAM)
#serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversocket.bind(ADDR)
serversocket.listen(5)
lock = thrd.Lock()

back_g="bg.jpg"
plane_img=['plane1.png','plane2.png','plane3.png','plane1.png','plane2.png','plane3.png']
plane_data=[[-1,-1],[-1,-1]]

def accept_thread():
    while 1:
        clisocket, addr=serversocket.accept()
        print '...connected from:',addr
        t=thrd.Thread(target=plane,args=(clisocket,))
        threads.append(clisocket)
        t.start()

        


def frame_initialize(back_g,plane_img,dim):
    pygame.init()
    screen=pygame.display.set_mode((dim,dim),0,32)
    background=pygame.image.load(back_g).convert()
    planes=[pygame.image.load(i).convert_alpha() for i in plane_img]
    return screen,background,planes

def get_center(plane_img,dim):
    x_c=plane_img.get_width()/2
    y_c=plane_img.get_width()/2
    return x_c,y_c

def update(id_no,new_x,new_y):
    #print 'updating'
    if(id_no>len(plane_data)-1):
        plane_data.append([new_x,new_y])
        
    else:
        plane_data[id_no]=[new_x,new_y]
    print new_x,'  ',new_y
def plane(clisocket):
        d=[0,0]
        c=clisocket.recv(CHECK)
        i=int(c)
        x=clisocket.recv(CHECK)
        y=clisocket.recv(CHECK)
        l=int(x)
        t=int(y)
        
        
        x_c,y_c=get_center(plane_img[i],600)
        #pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame. quit()
                sys.exit()

        time.sleep(0.5)

        lock.acquire()
        #pygame.time.wait(10)

        
        theta=math.radians(t)
        update(i,x_c+l*np.cos(theta),y_c-l*np.sin(theta))
        #print x_c+l*np.cos(theta),y_c+l*np.sin(theta)
        lock.release()
        while True:
                for event in pygame.event.get():
                        if event.type==QUIT:
                                pygame. quit()
                                sys.exit()
                #lock.acquire()
                x=clisocket.recv(CHECK)
                y=clisocket.recv(CHECK)
                l=int(x)
                print l
                t=int(y)
                
                
                #print y
                if (l==-1 and t==-1):
                        #lock.release()
                        break
                #pygame.time.wait(10)
                time.sleep(0.3)
                lock.acquire()
                theta=math.radians(t)
                #print theta
                update(i,300+l*np.cos(theta),300-l*np.sin(theta))
                lock.release()
            


screen,background,plane_img=frame_initialize(back_g,plane_img,600)

t1=thrd.Thread(target=accept_thread)
t1.start()

while True:
    for event in pygame.event.get():
            if event.type==QUIT:
                pygame. quit()
                sys.exit()
                
    screen.blit(background,(0,0))
    for i in range(0,len(plane_data)):
        #print plane_data[i][0],plane_data[i][1]
        screen.blit(plane_img[i],(plane_data[i][0],plane_data[i][1]))
    #print 'updated'
    #print plane_data[0]
    pygame.display.update()
