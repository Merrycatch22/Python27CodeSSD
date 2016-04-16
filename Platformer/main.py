'''
Created on Feb 13, 2015

@author: Nicky
'''

import pygame, sys, time, math, random
from pygame.locals import *
import pygame.mixer

from Jumper import Jumper
from KeyInput import KeyInput
from Obstacle import Obstacle


size = width, height= 640, 480
screen = pygame.display.set_mode(size)
pygame.mixer.init()
background=pygame.Surface(screen.get_size())
background=background.convert()
pygame.display.set_caption("")
color_back=(255,255,255)    
background.fill(color_back)  
KI=KeyInput()
J=Jumper((0,255,255))
ObsArr=[Obstacle((255,0,0),0,height-10,width,10),
        Obstacle((255,0,0),0,0,width,10),
        Obstacle((255,0,0),0,0,10,height),
        Obstacle((255,0,0),630,0,10,height),
        Obstacle((255,0,0),width/4,150,width/2,30),
        Obstacle((255,0,0),0,300,width/3,30),
        Obstacle((255,0,0),width*2/3,300,width/3,30)
        ]

def main():
    
    while 1:
        for i in ObsArr:
            i.redraw(screen)
            
        KI.get_input()
        if KI.ret("escape"):
            sys.exit()
        if KI.ret("a"):
            J.accelx(False)
        if KI.ret("d"):
            J.accelx(True)
        if KI.ret("w"):
            J.jump()
        if not KI.ret("w"):
            J.canjump=False
        
        J.gravdown()
        
        for i in ObsArr:
            i.redraw(screen)
            J.collide(i)
        J.jumputil()
        J.move()
        J.redraw(screen)
        
        pygame.display.update()
        screen.blit(background,(0,0))
        time.sleep(0.01)  
        print (J.canjump) 
        
if __name__ == '__main__':
    main()
    