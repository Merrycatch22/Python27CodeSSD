import pygame,sys,time,math
import pygame.gfxdraw, pygame.mixer
from pygame.locals import *

class Jumper(object):
    
    def __init__(self,color):
        
        self.alive=True
        self.x, self.y, self.dx, self.dy = 310,100,20,20
        self.jumper_rect=Rect((self.x,self.y),(self.dx,self.dy))
        self.color=color
        self.vx, self.vy=0,0
        self.vx_max=5
        self.accx,self.grav=0.5,0.3
        self.jumpheight=7
        self.canjump=False
        self.jumptimemax, self.jumptime=20,0
    def redraw(self,screen):
        
        self.jumper_rect=Rect((self.x,self.y),(self.dx,self.dy))
        pygame.draw.rect(screen,self.color,self.jumper_rect)
    
    #def movex (self):
        
    def gravdown (self):
        self.vy-=self.grav
    
    def move (self):
        
        if self.vx>=self.accx:
            self.vx-=self.accx
        if self.vx<=-self.accx:
            self.vx+=self.accx               
        if self.vx<self.accx and self.vx>-self.accx:
            self.vx=0   
        
        self.x+=self.vx
        self.y-=self.vy
        
    def accelx (self,boolo):
        
        if self.vx<self.vx_max and boolo:
            self.vx+=2*self.accx
        if self.vx>-self.vx_max and not boolo:
            self.vx-=2*self.accx
    def jumputil (self):
        self.jumptime-=1
        if self.jumptime<0:
            self.canjump=False
    def jump (self):
        if self.canjump:
            self.vy=self.jumpheight
        
    def collide(self,o):
        if self.x+self.dx>o.x and self.x<o.x+o.dx and self.y+self.dy-self.vy>o.y and self.y-self.vy<o.y+o.dy:
            self.vy=0
            if self.y+self.dy<=o.y:
                self.canjump=True
                self.jumptime=self.jumptimemax
        if self.x+self.dx+self.vx>o.x and self.x+self.vx<o.x+o.dx and self.y+self.dy>o.y and self.y<o.y+o.dy:
            self.vx=0