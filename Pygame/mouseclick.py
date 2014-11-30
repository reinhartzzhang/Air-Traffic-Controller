from socket import *
import math
import pygame,sys
from pygame.locals import *
import wx
import wx.lib.buttons
import threading as thrd
import time

HOST='localhost'
PORT=21546
ADDR=(HOST,PORT)
lock = thrd.Lock()

univ_plane_id=0


bif="bg.jpg"
plimg=['plane2.png','plane1.png','plane3.png']
pygame.init()
screen=pygame.display.set_mode((600,600),0,32)
background=pygame.image.load(bif).convert()
plconv=[pygame.image.load(i).convert_alpha() for i in plimg]


BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
FLIGHTS=[]
x_c=600/2-plconv[0].get_width()/2
y_c=600/2-plconv[0].get_width()/2
c=''
d=[]
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
def func_call(x,y,clisocket,univ_plane_id):
    

    l=int(((x-300)**2+(y-300)**2)**0.5)
    clisocket.send(str(univ_plane_id).zfill(4))
    theta=int(100*(math.atan((300-y)/(x-300))))
    clisocket.send(str(l).zfill(4))
    clisocket.send(str(theta).zfill(4))
    #radius(plane_data[0],plane_data[1])
    while (l>100):
        #lock.acquire()
        l=l-5
        #update(0,l*np.cos(theta),l*np.sin(theta))
        x=str(l).zfill(4)
        y=str(theta).zfill(4)
        print x
        print y
        clisocket.send(x)
        clisocket.send(y)
                #lock.release()
                
        
    while (theta<600):
                #time.sleep(0.1)
                theta=theta+5
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
    

        
while True:
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==6:
            (alpha,beta)= pygame.mouse.get_pos()
            app = wx.PySimpleApp()
            frame = create(None)
            frame.Show()
            app.MainLoop()
            clisocket=socket(AF_INET, SOCK_STREAM)
            clisocket.connect(ADDR)
            print 'chintu'
            t=thrd.Thread(target=func_call,args=(alpha,beta,clisocket,univ_plane_id))
            univ_plane_id=univ_plane_id+1
            t.start()

            
            
            
    screen.blit(background,(0,0))
    pygame.draw.line(screen, GREEN, (300, 300), (400,300), 4)
    pygame.draw.circle(screen, GREEN, (300,300), 100, 4)
    pygame.draw.circle(screen, GREEN, (300,300), 97, 4)
    pygame.draw.circle(screen, GREEN, (300,300), 95, 4)
    pygame.display.update()


        
