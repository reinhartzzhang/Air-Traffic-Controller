import threading as thrd
import numpy as np
import signal
import time
import pygame,sys
from pygame.locals import *
from socket import *
import math
import os

####################################################################################
BLUE = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)

temp=[-50 for i in range(0,36)]
position=[[-50 for i in range(0,2)] for j in range(0,36)]
back_g="bg1.jpg"
plane_img=['plane1.png','plane2.png','plane3.png','plane4.png','plane5.png','plane6.png','plane7.png','plane8.png','plane9.png','plane10.png','plane11.png','plane12.png','plane13.png','plane14.png','plane15.png','plane16.png','plane17.png','plane18.png','plane19.png','plane20.png','plane21.png','plane22.png','plane23.png','plane24.png','plane25.png','plane26.png','plane27.png','plane28.png','plane29.png']
plane_data=[[900 for i in range(0,2)] for j in range(0,29)]


################################################################################
#returns the value of the free port
def get_port():
    a=open("temp.txt",'r')
    b=int(a.readline())
    a.close()
    a=open('temp.txt','wt')
    a.write(str(b+5))
    a.close
    return b+5



tstart = time.time()
CHECK=4
HOST=''
PORT=get_port()
BUFSIZ=1024
ADDR = (HOST,PORT)
threads=[]
serversocket=socket(AF_INET, SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(12)
lock = thrd.Lock()
############################################################################################
#following function gives the time for joining the circle at 'dest'
def compute(dest,l):
    
    check=0

    for j in range (0,36):
        temp[j]=-50
    for j in range (0,36):
        if(position[j][0]!=-50):
            for i in range (-3,4):
                if (position[j][1]==-1):
                    temp[(position[j][0]+i)%36]=-1
                else:
                    temp[(position[j][0]+i)%36]=1

    #print temp
    #print position
    
    initial=dest-l
    if initial<0:
        check=1
    delay=l
    dist=5
    
    while(temp[initial%36]!=-50 and check==0):
        if (initial%36==0):   
           check=1
        initial=initial-1
        delay=delay+1
     
    while((temp[initial%36]!=-50 or  temp[initial%36]==1) and check==1):
        if (initial%36==0):   
           check=2
        initial=initial-1
        delay=delay+1

    while((temp[initial%36]!=-50 or  temp[initial%36]==1 or temp[initial%36]==-1)   and check==1):
        initial=initial-1
        delay=delay+1
        

    return (initial%36),delay
        

#############################################################################################3
#accepts a new plane connection , computes the joining time and adds the new plane
#as a new thread
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
        position[i][0]=slot
        t=thrd.Thread(target=plane,args=(clisocket,i,slot,delay))
        lock.release()
        
        t.start()
        
        threads.append(clisocket)

        
########################################################################################3

def frame_initialize(back_g,plane_img,dim):
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (698,28)
    pygame.init()
    pygame.display.set_caption('Central ATC Server')
    screen=pygame.display.set_mode((dim,dim),0,32)
    background=pygame.image.load(back_g).convert()
    planes=[pygame.image.load(i).convert_alpha() for i in plane_img]
    return screen,background,planes
##############################################################################

def get_center(plane_img,dim):
    x_c=plane_img.get_width()/2
    y_c=plane_img.get_width()/2
    return x_c,y_c

#############################################################################

def update(id_no,new_x,new_y):
    
    if(id_no>len(plane_data)-1):
        plane_data.append([new_x,new_y])
        
    else:
        plane_data[id_no]=[new_x,new_y]
    

################################################################################
   
def plane(clisocket,i,dest,delay):

        verify=1
        clisocket.send(str(delay).zfill(4))
        
        d=[0,0]
        dest=dest+1
        position[i][0]=dest
        x=clisocket.recv(CHECK)
        y=clisocket.recv(CHECK)

        l=int(x)
        t=int(y)
        x_c,y_c=get_center(plane_img[i],700)
        
        
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame. quit()
                sys.exit()

        time.sleep(0.5)

        lock.acquire()
        theta=math.radians(t)
        update(i,350+l*np.cos(theta)-x_c,350-l*np.sin(theta)-y_c)
        lock.release()

        # following loop continuously recieves the position of plane and plots it
        while True:
                for event in pygame.event.get():
                        if event.type==QUIT:
                                pygame. quit()
                                sys.exit()
                x=clisocket.recv(CHECK)
                y=clisocket.recv(CHECK)
                dest=dest+1
                
                if(l>150):
                    position[i][0]=(dest%36)
                    position[i][1]=-1
                elif(l==150):
                    position[i][0]=(dest%36)
                    position[i][1]=1
                elif(l<150):
                    position[i][0]=-50

                l=int(x)
                t=int(y)

                # following if statement tells that the plane has landed                
                if (l==-1 and t==-1):
                        break

                time.sleep(0.3)

                lock.acquire()
                theta=math.radians(t)
                # update function plots the updated positions of the plane
                update(i,350+l*np.cos(theta)-x_c,350-l*np.sin(theta)-y_c)
                lock.release()
        # following statement terminates the thread of the landed plane
        update(i,900,900) 
        
            

#############################################################################
        
screen,background,plane_img=frame_initialize(back_g,plane_img,700)

t1=thrd.Thread(target=accept_thread)
t1.start()

while True:
    for event in pygame.event.get():
            if event.type==QUIT:
                pygame. quit()
                sys.exit()
                
    screen.blit(background,(0,0))
    pygame.draw.line(screen, BLUE, (335, 355), (492,355),20)
    #pygame.draw.circle(screen, BLUE, (350,350), 148, 20)
    pygame.draw.circle(screen, BLUE, (343,357), 150, 4)
    pygame.draw.circle(screen, BLUE, (343,357), 20,4)

    for i in range(0,len(plane_data)):
        screen.blit(plane_img[i],(plane_data[i][0],plane_data[i][1]))
    pygame.display.update()
