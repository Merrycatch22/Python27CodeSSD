import pygame,os,sys
from pygame.locals import *

class KeyInput():
    
    def __init__(self):
        self.buttons={
                      "a":False,
                      "d":False,
                      "w":False,
                      "s":False,
                      "up":False,
                      "down":False,
                      "left":False,
                      "right":False,
                      "escape":False
                      #can put more here
                      }
    
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                self.buttons[pygame.key.name(event.key)]=True
            if event.type == KEYUP:
                self.buttons[pygame.key.name(event.key)]=False
    
    def ret(self,st):
        return self.buttons[st]
    
    def debugg(self):
        os.system('cls')
        for i in self.buttons:            
            print(i,self.buttons[i])