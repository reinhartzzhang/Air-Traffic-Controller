import numpy as np
import time
import pygame,sys
from pygame.locals import *

plane_data=[[0,0]]
back_g="bg.jpg"
plane_img=['plane1.png']

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

def update(id_no,new_x,new_y):

    if(id_no>len(plane_data)):
        plane_data.append([new_x,new_y])        
    else:
        plane_data[id_no]=[new_x,new_y]

        
################################################################################

    
screen,background,plane_img=frame_initialize(back_g,plane_img,600)   
x_c,y_c=get_center(plane_img[0],600)
theta=0
while True:
    time.sleep(0.01)
    theta=theta+0.05
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame. quit()
            sys.exit()
            
    screen.blit(background,(0,0))

    update(0,100*np.cos(theta),100*np.sin(theta))

    screen.blit(plane_img[0],(x_c+plane_data[0][0],y_c+plane_data[0][1]))

    pygame.display.update()
