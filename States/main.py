'''
Created on Feb 13, 2015

@author: Nicky
'''

import pygame, sys, time, math, random
from pygame.locals import *
import pygame.mixer

from KeyInput import KeyInput


size = width, height= 640, 640
screen = pygame.display.set_mode(size)
pygame.mixer.init()
background=pygame.Surface(screen.get_size())
background=background.convert()
pygame.display.set_caption("")
color_back=(255,255,255)    
background.fill(color_back)  
KI=KeyInput()
def main():
    
    while 1:
        KI.get_input()
        KI.debugg()
        pygame.display.update()
        screen.blit(background,(0,0))
        time.sleep(0.01)   
        
if __name__ == '__main__':
    main()
    