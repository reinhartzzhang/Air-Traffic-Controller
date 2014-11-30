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

temp=[-1 for i in range(0,36)]
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)



position=[-1 for i in range(0,36)]

# Reocrd start time for calculating frame rate
tstart = time.time()
CHECK=4
HOST=''
PORT=2134
BUFSIZ=1024
ADDR = (HOST,PORT)
threads=[]
serversocket=socket(AF_INET, SOCK_STREAM)
#serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversocket.bind(ADDR)
serversocket.listen(5)
lock = thrd.Lock()

back_g="bg1.jpg"
plane_img=['plane1.png','plane2.png','plane3.png','plane4.png','plane5.png','plane6.png','plane7.png','plane8.png','plane9.png','plane10.png','plane11.png','plane12.png','plane13.png','plane14.png','plane15.png','plane16.png','plane17.png','plane18.png','plane19.png','plane20.png','plane21.png','plane22.png','plane23.png','plane24.png','plane25.png','plane26.png','plane27.png','plane28.png','plane29.png']
plane_data=[[0,0],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]


def compute(dest,l):
    for j in range (0,36):
        if(position[j]!=-1):
            for i in range (-4,5):
                temp[(position[j]+i)%36]=1
        else:
            temp[position[j]]=-1
    print temp
    print position
    initial=dest-15
    delay=60
    dist=5
    while(temp[initial%36]!=-1):
        initial=initial-1
        delay=delay+1
    return (initial%36),delay
        


    
def accept_thread():
    while 1:
        clisocket, addr=serversocket.accept()
        print '...connected from:',addr
        
        
        c=clisocket.recv(CHECK)
        i=int(c)
        dest_temp=clisocket.recv(CHECK)
        dest=int(dest_temp)
        dest=dest/10
        x=clisocket.recv(CHECK)
        l=int(x)

        lock.acquire()

        slot,delay=compute(dest,l)
        position[i]=slot
        lock.release()
        t=thrd.Thread(target=plane,args=(clisocket,i,slot,delay))

        
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
    #print new_x,'  ',new_y


    
def plane(clisocket,i,dest,delay):

        verify=1
        clisocket.send(str(delay).zfill(4))
        
        d=[0,0]
        dest=dest+1
        position[i]=dest
        x=clisocket.recv(CHECK)
        y=clisocket.recv(CHECK)

        l=int(x)
        t=int(y)
        x_c,y_c=get_center(plane_img[i],700)
        #pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame. quit()
                sys.exit()

        time.sleep(0.5)

        lock.acquire()
        #pygame.time.wait(10)

        
        theta=math.radians(t)
        update(i,350+l*np.cos(theta)-x_c,350-l*np.sin(theta)-y_c)
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
                
                dest=dest+1
                if(l>=150):
                    position[i]=(dest%36)    
                elif(l<150):
                    position[i]=-1

                l=int(x)
                #print l
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
                update(i,350+l*np.cos(theta)-x_c,350-l*np.sin(theta)-y_c)
                lock.release()
            


screen,background,plane_img=frame_initialize(back_g,plane_img,700)

t1=thrd.Thread(target=accept_thread)
t1.start()

while True:
    for event in pygame.event.get():
            if event.type==QUIT:
                pygame. quit()
                sys.exit()
                
    screen.blit(background,(0,0))
    pygame.draw.line(screen, BLACK, (350, 350), (500,350),20)
    pygame.draw.circle(screen, BLACK, (350,350), 148, 20)
    pygame.draw.circle(screen, BLACK, (350,350), 150, 20)
    pygame.draw.circle(screen, BLACK, (350,350), 20,20)

    for i in range(0,len(plane_data)):
        #print plane_data[i][0],plane_data[i][1]
        screen.blit(plane_img[i],(plane_data[i][0],plane_data[i][1]))
    #print 'updated'
    #print plane_data[0]
    pygame.display.update()
