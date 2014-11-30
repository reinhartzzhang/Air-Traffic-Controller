x = 0
y = 0
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
 
import pygame
pygame.init()
screen = pygame.display.set_mode((700,700))
 
# wait for a while to show the window.
import time
time.sleep(2)
