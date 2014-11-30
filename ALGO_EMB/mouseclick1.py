from socket import *
import math
import pygame,sys
from pygame.locals import *
import wx
import wx.lib.buttons
import threading as thrd
import time
import numpy as np

HOST='localhost'
PORT=2134
ADDR=(HOST,PORT)
lock = thrd.Lock()

univ_plane_id=0


bif="bg1.jpg"
#plimg=['plane2.png','plane1.png','plane3.png']
pygame.init()
screen=pygame.display.set_mode((700,700),0,32)
background=pygame.image.load(bif).convert()


BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
#FLIGHTS=[]
#x_c=700/2-plconv[0].get_width()/2
#y_c=700/2-plconv[0].get_width()/2
c=''
speed=[]
###########################################################3
def create(parent):
    return Frame2(parent)

[wxID_FRAME2, wxID_FRAME2BUTTON1, wxID_FRAME2PANEL1, wxID_FRAME2STATICTEXT1, 
 wxID_FRAME2TEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(5)]

class Frame2(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME2, name='', parent=prnt,
              pos=wx.Point(513, 311), size=wx.Size(353, 167),
              style=wx.DEFAULT_FRAME_STYLE, title='ENTER PLANE SPEED')
        self.SetClientSize(wx.Size(337, 128))
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.SetThemeEnabled(False)
        self.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,'Tahoma'))
        self.SetBackgroundStyle(wx.BG_STYLE_COLOUR)

        self.panel1 = wx.Panel(id=wxID_FRAME2PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(337, 128),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetBackgroundColour(wx.Colour(64, 0, 0))

        self.staticText1 = wx.StaticText(id=wxID_FRAME2STATICTEXT1,
              label='  SPEED : ', name='staticText1', parent=self.panel1,
              pos=wx.Point(56, 16), size=wx.Size(87, 23), style=0)
        self.staticText1.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        self.staticText1.SetAutoLayout(False)
        self.staticText1.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.staticText1.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.staticText1.SetForegroundColour(wx.Colour(0, 0, 0))

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME2TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(160, 16), size=wx.Size(108, 29),
              style=0, value='Enter Speed . . .')
        self.textCtrl1.Bind(wx.EVT_TEXT, self.OnTextCtrl1Text,
              id=wxID_FRAME2TEXTCTRL1)

        self.button1 = wx.Button(id=wxID_FRAME2BUTTON1, label='SUBMIT',
              name='button1', parent=self.panel1, pos=wx.Point(120, 72),
              size=wx.Size(96, 32), style=0)
        self.button1.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.button1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME2BUTTON1)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        self.Close(1)

    def OnTextCtrl1Text(self,event):
        speed.append(self.textCtrl1.GetValue())
        





        ######################
def func_call(x,y,clisocket,univ_plane_id,sp_val):
    
    #print 'coordinates',x,y

    
    q=0
    l=int(((x-350)**2+(y-350)**2)**0.5)
    init_l=l
    clisocket.send(str(univ_plane_id).zfill(4))
    if ((350-y)>=0 and (x-350)>=0):
        s=math.atan2((350-y),(x-350))
        y=math.degrees(s)
        q=1
        #print y
        
    if ((350-y)>0 and (x-350)<0):
        s=math.atan2((350-y),(350-x))
        #print "la",s
        y=180-math.degrees(s)
        q=2
        #print "ma",(y)
        #print math.radians(y)
        #theta=int(math.radians(y)*100)
        #print theta
                          
    if ((350-y)<0 and (x-350)<0):
        s=math.atan2((y-350),(350-x))
        y=180+math.degrees(s)
        q=3
        #print y
    if ((350-y)<0 and (x-350)>0):
        s=math.atan2((y-350),(x-350))
        y=360-math.degrees(s)
        q=4
        #print y
    theta=int(y)
    vel=int(sp_val)/100
    #print theta
    if ((theta%30)<=23):
        dest=theta-(theta%30)
    else:
        dest=theta+(30-(theta%30))


    clisocket.send(str(dest).zfill(4))
    clisocket.send(str(l).zfill(4))
    delay=clisocket.recv(4)
    delay=int(delay)
    clisocket.send(str(l).zfill(4))
    clisocket.send(str(theta).zfill(4))
    #radius(plane_data[0],plane_data[1])

    while (l>200):
        #lock.acquire()
        l=l-vel
        if (l<=200):
            l=200
            break
        if vel<10:
            vel=vel+1
        if vel>10:
            vel=vel-1
        #update(0,l*np.cos(theta),l*np.sin(theta))

        if (theta%30)<7 and (theta%30)>4:
            theta=theta-2
        elif (theta%30)>23 and (theta%30)<26:
            theta=theta+2
        elif(theta%30)<=4 and (theta%30)>0 :
            theta=theta-(theta%30)
        elif(theta%30)>=26:
            theta=theta+(30-(theta%30))
        elif (theta%30)!=0:
            theta=theta-2
        
        x=str(l).zfill(4)
        y=str(theta).zfill(4)
        #print x
        #print y
        delay=delay-1
        clisocket.send(x)
        clisocket.send(y)
                #lock.release()

    theta_inc=90-theta
    temp_vel=vel
    #l_p=152
    alpha=0
    beta=0
    temp_l=l
    
    while (temp_l>150 and delay>0):
            #lock.acquire()
            temp_l=temp_l-temp_vel
            if temp_vel<10:
                temp_vel=temp_vel+1
            if temp_vel>10:
                temp_vel=temp_vel-1
            delay=delay-1
    

    count=delay

    l=200
    l_p=50
    x_c=350+(l+25)*np.cos(math.radians(theta))
    y_c=350-(l+25)*np.sin(math.radians(theta))
    print "centre",x_c,y_c
    if(q==1):
            theta1=180+theta
    if(q==2):
        theta1=270+theta-90
    if(q==3):
        theta1=theta-180
    if(q==4):
        theta1=theta-270

   


    while(count>0):
        
        x=x_c+l_p*np.cos(theta1)
        y=y_c-l_p*np.sin(theta1)
        l1=int(((x-350)**2+(y-350)**2)**0.5)
    
        if ((350-y)>=0 and (x-350)>0):
            s=math.atan2((350-y),(x-350))
            y=math.degrees(s)
            print y
            
            
        if ((350-y)>0 and (x-350)<=0):
            s=math.atan2((350-y),(350-x))
            print "la",s
            y=180-math.degrees(s)
            print "ma",(y)
            print math.radians(y)
            #theta=int(math.radians(y)*100)
            #print theta
                              
        if ((350-y)<=0 and (x-350)<0):
            s=math.atan2((y-350),(350-x))
            y=180+math.degrees(s)
            print y
            
        if ((350-y)<0 and (x-350)>=0):
            s=math.atan2((y-350),(x-350))
            y=360-math.degrees(s)
            print y
            
        s=int(y)
        print theta1    
        theta1=theta1+1
        count=count-1       
        clisocket.send(str(l1).zfill(4))
        clisocket.send(str(s).zfill(4))




  


    while (l>150):
            #lock.acquire()
            l=l-vel
            if (l<=150):
                l=150
                break

            if vel<10:
                vel=vel+1
            if vel>10:
                vel=vel-1
            #update(0,l*np.cos(theta),l*np.sin(theta))

            if (theta%30)<7 and (theta%30)>4:
                theta=theta-2
            elif (theta%30)>23 and (theta%30)<26:
                theta=theta-2
            elif(theta%30)<=4 and (theta%30)>0 :
                theta=theta-(theta%30)
            elif(theta%30)>=26:
                theta=theta+(30-(theta%30))
            elif (theta%30)!=0:
                theta=theta-2
            
            x=str(l).zfill(4)
            y=str(theta).zfill(4)
            #print x
            #print y
            clisocket.send(x)
            clisocket.send(y)
            
    while (theta<360):
        
                #time.sleep(0.1)
                theta=theta+10
                #update(0,l*np.cos(theta),l*np.sin(theta))
                #lock.acquire()
                x=str(l).zfill(4)
                y=str(theta).zfill(4)
                clisocket.send(x)
                clisocket.send(y)
                #lock.release()
                
                
    while (l>=0):
                #time.sleep(0.1)
                l=l-10
                #lock.acquire()
                #update(0,l*np.cos(theta),l*np.sin(theta))
                #lock.acquire()
                x=str(l).zfill(4)
                y=str(theta).zfill(4)
                clisocket.send(x)
                clisocket.send(y)
                #lock.release()
                
    l=-1
    theta=-1
    clisocket.send(str(l).zfill(4))
    clisocket.send(str(theta).zfill(4))

    
    
    ##################################
    
app = wx.PySimpleApp()
        
while True:
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==6:
            (alpha,beta)= pygame.mouse.get_pos()
            frame = create(None)
            frame.Show()
            app.MainLoop()
            clisocket=socket(AF_INET, SOCK_STREAM)
            clisocket.connect(ADDR)
            #print 'chintu'
            t=thrd.Thread(target=func_call,args=(alpha,beta,clisocket,univ_plane_id,speed[len(speed)-1]))
            univ_plane_id=univ_plane_id+1
            t.start()

          
    screen.blit(background,(0,0))
    pygame.draw.line(screen, BLACK, (350, 350), (500,350),20)
    pygame.draw.circle(screen, BLACK, (350,350), 148, 20)
    pygame.draw.circle(screen, BLACK, (350,350), 150, 20)
    pygame.draw.circle(screen, BLACK, (350,350), 20,20)
    pygame.display.update()
##    pygame.draw.line(screen, GREEN, (300, 300), (400,300), 4)
##    pygame.draw.circle(screen, GREEN, (300,300), 100, 4)
##    pygame.draw.circle(screen, GREEN, (300,300), 97, 4)
##    pygame.draw.circle(screen, GREEN, (300,300), 95, 4)
##    pygame.display.update()


        
