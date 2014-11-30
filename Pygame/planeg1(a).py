from socket import *
import threading
import wx
import wx.lib.buttons
import pygame,sys
from pygame.locals import *
import numpy as np
import signal
import time

HOST='localhost'
PORT=21541
ADDR=(HOST,PORT)
clisocket=socket(AF_INET, SOCK_STREAM)
clisocket.connect(ADDR)
lock = threading.Lock()

#Boa:Frame:Frame2
c=[]
color=[]
speed=[]
angle=[]
length=[]

def fun_call():
    print color
    #print c
    #l=int(length[len(length)-1])
    l=500
    clisocket.send(color[len(color)-1])
    #clisocket.send(length[len(length)-1])
    theta=int(angle[len(angle)-1])
    #update(0,l*np.cos(theta),l*np.sin(theta))
    #x=str(plane_data[0][0]).zfill(4)
    #y=str(plane_data[0][1]).zfill(4)
    #print x
    #print y
    clisocket.send(str(l).zfill(4))
    clisocket.send(str(theta).zfill(4))
    #radius(plane_data[0],plane_data[1])
    while (l>200):
        #lock.acquire()
        l=l-10
        #update(0,l*np.cos(theta),l*np.sin(theta))
        x=str(l).zfill(4)
        y=str(theta).zfill(4)
        print x
        print y
        clisocket.send(x)
        clisocket.send(y)
                #lock.release()
                
        
    while (theta<600):
                time.sleep(0.1)
                theta=theta+10
                #update(0,l*np.cos(theta),l*np.sin(theta))
                #lock.acquire()
                x=str(l).zfill(4)
                y=str(theta).zfill(4)
                clisocket.send(x)
                clisocket.send(y)
                #lock.release()
                
                
    while (l>=0):
                time.sleep(0.1)
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


def create(parent):
    return Frame2(parent)

[wxID_FRAME2, wxID_FRAME2PANEL1, wxID_FRAME2SUBMIT, wxID_FRAME2TEXTCTRL1, 
 wxID_FRAME2TEXTCTRL2, wxID_FRAME2TEXTCTRL3, wxID_FRAME2TEXTCTRL4, 
] = [wx.NewId() for _init_ctrls in range(7)]

class Frame2(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME2, name='', parent=prnt,
              pos=wx.Point(569, 160), size=wx.Size(400, 485),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame2')
        self.SetClientSize(wx.Size(384, 447))

        self.panel1 = wx.Panel(id=wxID_FRAME2PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(384, 447),
              style=wx.TAB_TRAVERSAL)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME2TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(8, 160), size=wx.Size(96, 24),
              style=0, value='textCtrl1')
        self.textCtrl1.Bind(wx.EVT_TEXT, self.OnTextCtrl1Text,
              id=wxID_FRAME2TEXTCTRL1)

        self.textCtrl2 = wx.TextCtrl(id=wxID_FRAME2TEXTCTRL2, name='textCtrl2',
              parent=self.panel1, pos=wx.Point(8, 208), size=wx.Size(100, 21),
              style=0, value='textCtrl2')
        self.textCtrl2.Bind(wx.EVT_TEXT, self.OnTextCtrl2Text,
              id=wxID_FRAME2TEXTCTRL2)

        self.textCtrl3 = wx.TextCtrl(id=wxID_FRAME2TEXTCTRL3, name='textCtrl3',
              parent=self.panel1, pos=wx.Point(8, 256), size=wx.Size(100, 21),
              style=0, value='textCtrl3')
        self.textCtrl3.Bind(wx.EVT_TEXT, self.OnTextCtrl3Text,
              id=wxID_FRAME2TEXTCTRL3)

        self.submit = wx.lib.buttons.GenButton(id=wxID_FRAME2SUBMIT,
              label=u'submit', name=u'submit', parent=self.panel1,
              pos=wx.Point(248, 200), size=wx.Size(88, 64), style=0)
        self.submit.Bind(wx.EVT_BUTTON, self.OnSubmitButton,
              id=wxID_FRAME2SUBMIT)

        self.textCtrl4 = wx.TextCtrl(id=wxID_FRAME2TEXTCTRL4, name='textCtrl4',
              parent=self.panel1, pos=wx.Point(8, 120), size=wx.Size(96, 21),
              style=0, value='textCtrl4')
        self.textCtrl4.Bind(wx.EVT_TEXT, self.OnTextCtrl4Text,
              id=wxID_FRAME2TEXTCTRL4)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnSubmitButton(self, event):
        #c=color[len(color)-1]
        fun_call()
        

    def OnTextCtrl1Text(self, event):
        angle.append(self.textCtrl1.GetValue())

    def OnTextCtrl2Text(self, event):
        length.append(self.textCtrl2.GetValue())

    def OnTextCtrl3Text(self, event):
        speed.append(self.textCtrl3.GetValue())

    def OnTextCtrl4Text(self, event):
        color.append(self.textCtrl4.GetValue())



app = wx.PySimpleApp()
frame = create(None)
frame.Show()

app.MainLoop()


def recieve(clisocket):
    while 1:
        data=clisocket.recv(1024)
        print(data)


        
        
    


#t0=threading.Thread(target=recieve,args=(clisocket,))
#t1=threading.Thread(target=senddata,args=(clisocket,))
#t0.start()
#t1.start()

while 1:
    pass
