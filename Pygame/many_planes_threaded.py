import numpy as np
import time
import pygame,sys
from pygame.locals import *
import threading as thrd
import time

plane_data=[[0,0],[0,0],[0,0]]
back_g="bg.jpg"
plane_img=['plane1.png','plane2.png','plane3.png']

################################################################################
# Function definitions

def frame_initialize(back_g,plane_img,dim):
    pygame.init()
    screen=pygame.display.set_mode((dim,dim),0,32)
    background=pygame.image.load(back_g).convert()
    planes=[pygame.image.load(i).convert_alpha() for i in plane_img]
    return screen,background,planes



def get_center(plane_img,dim):
    x_c=dim/2-plane_img.get_width()/2
    y_c=dim/2-plane_img.get_width()/2
    return x_c,y_c

def update(i,new_x,new_y):

    if(i>len(plane_data)):
        plane_data.append([new_x,new_y])
        print new_x,'  ',new_y
    else:
        plane_data[i]=[new_x,new_y]
        print 'aa',new_x,' ',new_y

lock = thrd.Lock()      
################################################################################
screen,background,plane_img=frame_initialize(back_g,plane_img,600)

def plot(i,theta):   
    x_c,y_c=get_center(plane_img[i],600)
    while True:
        
        #pygame.time.wait(100)
        theta=theta+0.1

        lock.acquire()       
        update(i,x_c+100*np.cos(theta),y_c+100*np.sin(theta))
        lock.release()



t1 = thrd.Thread(target=plot,args=(0,1))
t0 = thrd.Thread(target=plot,args=(1,100))
t2 = thrd.Thread(target=plot,args=(2,200))

t1.start()
t0.start()
t2.start()

while True:
    time.sleep(0.1)
    for event in pygame.event.get():
            if event.type==QUIT:
                pygame. quit()
                sys.exit()
                
    screen.blit(background,(0,0))
    for i in range(0,len(plane_data)):
        screen.blit(plane_img[i],(plane_data[i][0],plane_data[i][1]))

    pygame.display.update()



# Main loop is necessary for exiting properly with keyboard
# interrupts
while True:
	pass
