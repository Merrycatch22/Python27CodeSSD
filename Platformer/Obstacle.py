import pygame,sys,time,math
import pygame.gfxdraw, pygame.mixer
from pygame.locals import *

class Obstacle (object):
    
    def __init__(self,color,x,y,dx,dy):
        
        self.x, self.y, self.dx, self.dy = x,y,dx,dy
        self.jumper_rect=Rect((self.x,self.y),(self.dx,self.dy))
        self.color=color
        
    def redraw(self,screen):
        
        self.jumper_rect=Rect((self.x,self.y),(self.dx,self.dy))
        pygame.draw.rect(screen,self.color,self.jumper_rect)
    