'''
Created on Feb 13, 2015

@author: Nicholas Tarn
'''
import pygame,sys,time,math
import pygame.gfxdraw, pygame.mixer
from pygame.locals import *

size = width, height= 640, 640
screen = pygame.display.set_mode(size)
opness=0.04
gravityx, gravityy=width/2,height/2


pygame.mixer.init()
pew0=pygame.mixer.Sound("pew0.wav")
pew1=pygame.mixer.Sound("pew1.wav")
boom0=pygame.mixer.Sound("boom0.wav")
boom1=pygame.mixer.Sound("boom1.wav")
invin0=pygame.mixer.Sound("invin0.wav")
invin1=pygame.mixer.Sound("invin1.wav")

class Gun(object):
    
    def __init__(self,colorGun,x,y,theta):
        
        self.x, self.y = x,y
        self.velx,self.vely=0,0
        self.theta=theta
        self.gunrect=Rect((self.x,self.y),(20,20))
        self.alive=True
        self.colorGun=colorGun
        self.reload=0
        self.timetoreload=50
        self.invincible=False
        self.invinciblereload=0
        self.acc=0
        
    def redraw(self,width,height,timeCount):
        
        self.gunrect=Rect((self.x,self.y),(20,20))
        
        pygame.draw.rect(screen,self.colorGun,Rect((self.x,self.y+24),(20*(self.timetoreload-self.reload)/self.timetoreload,4)))
        pygame.draw.rect(screen,self.colorGun,self.gunrect)
        pygame.gfxdraw.line(screen,(int)(self.x+10),(int)(self.y+10),(int)(self.x+10+40*math.cos(self.theta)),(int)(self.y+10+40*math.sin(self.theta)), self.colorGun)
        #pygame.draw.rect(screen,self.colorGun,Rect((self.x,self.y-8),(19*(self.vel)/4+1,4)))
        
        if self.invincible:
            pygame.draw.rect(screen,(255,255,255),self.gunrect)
            
    def moveUp(self):
        
        self.acc=opness
        
            
    def move(self):
            
        self.velx+=self.acc*math.cos(self.theta)-0.2*opness*(self.x-gravityx)/math.sqrt((self.x-gravityx)**2+(self.y-gravityy)**2)
        self.vely+=self.acc*math.sin(self.theta)-0.2*opness*(self.y-gravityy)/math.sqrt((self.x-gravityx)**2+(self.y-gravityy)**2)
        self.x+=self.velx
        self.y+=self.vely
        
        if self.acc>=0.1*opness:
            self.acc-=0.1*opness           
        if self.acc<0.1*opness:
            self.acc=0
        
        
        if self.x>640:
            self.x=0
        if self.x<0:
            self.x=640
        if self.y>640:
            self.y=0
        if self.y<0:
            self.y=640
            
        if self.reload>0:  
            self.reload-=1
            
        if self.invinciblereload>0:  
            self.invinciblereload-=1
            
        if self.invinciblereload<1200:
            self.invincible=False
            
    def turn(self,boo):
        
        if boo:
            self.theta-=1*opness
        
        else:
            self.theta+=1*opness    
    
    def reloadGun(self):
        
        if self.reload<=0:
            self.reload=self.timetoreload
    
    def reloadInvincibility(self):
        
        if self.invinciblereload<=0:
            self.invinciblereload=1500 
            self.invincible=True                   
                 
class Bullet(object):
    
    def __init__(self,Gun):
        
        self.x, self.y = Gun.x+8, Gun.y+8
        self.theta=Gun.theta
        self.life=0
        self.bulletrect=Rect((self.x,self.y),(4,4))
        self.colorBullet=Gun.colorGun
        
    def move(self):
        
        self.bulletrect=Rect((self.x,self.y),(4,4))
        pygame.draw.rect(screen,self.colorBullet,Rect(self.bulletrect))
        
        if self.x>640:
            self.x=0
        if self.x<0:
            self.x=640
        if self.y>640:
            self.y=0
        if self.y<0:
            self.y=640
                
        self.x+=5*math.cos(self.theta)
        self.y+=5*math.sin(self.theta)
        
        self.life+=1
        
    def dead(self):
        
        if self.life>200:
            return True
    
        else:
            return False
                     
def main():
   
    background=pygame.Surface(screen.get_size())
    background=background.convert()
    pygame.display.set_caption("Game Starts in one second")
    
    timeCount=0
    jdown, ldown, idown=False, False, False
    adown, ddown, wdown=False, False, False
    
    GunArray=[Gun((0,0,255),64*9,64*9,math.pi),Gun((0,255,0),64,64,0)]
    BulletArray0=[]
    BulletArray1=[] 
    
    time.sleep(1)
    pygame.display.set_caption("Space Wars Hard Physics version") 
    
    while 1:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: sys.exit()
            
            if event.type==KEYDOWN:
                
                if event.key ==K_g and (GunArray[0].alive==False or GunArray[1].alive==False):
                    
                    pygame.display.set_caption("Game Starts in one second.")
                    timeCount=0
                    jdown, ldown, idown=False, False, False
                    adown, ddown, wdown=False, False, False
                    GunArray=[Gun((0,0,255),540,540,math.pi),Gun((0,255,0),100,100,0)]
                    BulletArray0=[]
                    BulletArray1=[] 
                    time.sleep(1)
                    pygame.display.set_caption("Space Wars Hard Physics version") 
            
            if GunArray[0].alive:
                if event.type == KEYDOWN:
                    if event.key == K_PERIOD:
                        if GunArray[0].reload<=0 and GunArray[0].invincible==False:
                            BulletArray0.append(Bullet(GunArray[0]))
                            GunArray[0].reloadGun()
                            pew0.play() 
                    
                    if event.key == K_j:
                        jdown=True
                    if event.key == K_l:
                        ldown=True
                    if event.key == K_i:
                        idown=True
                            
                    if event.key == K_SLASH:
                        if GunArray[0].invinciblereload<=0:
                              
                            GunArray[0].reloadInvincibility()
                            invin0.play()      
                if event.type == KEYUP:
                    if event.key == K_j:
                        jdown=False
                    if event.key == K_l:
                        ldown=False
                    if event.key == K_i:
                        idown=False
            
            if GunArray[1].alive:
                
                
                            
                if event.type == KEYDOWN:
                    if event.key == K_c:
                        if GunArray[1].reload<=0 and GunArray[1].invincible==False:
                            BulletArray1.append(Bullet(GunArray[1]))
                            GunArray[1].reloadGun()
                            pew1.play()
                    if event.key == K_a:
                        adown=True
                    if event.key == K_d:
                        ddown=True
                    if event.key == K_w:
                        wdown=True
                     
                    
                    if event.key == K_v:
                        if GunArray[1].invinciblereload<=0:   
                            GunArray[1].reloadInvincibility()
                            invin1.play()
                                   
                if event.type == KEYUP:
                    if event.key == K_a:
                        adown=False
                    if event.key == K_d:
                        ddown=False
                    if event.key == K_w:
                        wdown=False            
        
        if GunArray[0].alive:
            GunArray[0].redraw(width,height,timeCount) 
            if jdown==True:
                GunArray[0].turn(True)
            if ldown==True:
                GunArray[0].turn(False)
            if idown==True:
                GunArray[0].moveUp()        
            
            GunArray[0].move()
            
        if GunArray[1].alive:
            GunArray[1].redraw(width,height,timeCount) 
            if adown==True:
                GunArray[1].turn(True)
            if ddown==True:
                GunArray[1].turn(False)
            if wdown==True:
                GunArray[1].moveUp()        
            
            GunArray[1].move()
        
        for i in BulletArray0:
            i.move()
            if i.bulletrect.colliderect(GunArray[1].gunrect) and GunArray[1].alive and GunArray[1].invincible==False:
                GunArray[1].alive=False
                BulletArray0.remove(i)
                boom1.play()
                BulletArray1=[]
                pygame.display.set_caption("Someone 1ost! What a 1oser! Restart by clicking g.")


            if i.dead():
                BulletArray0.remove(i)
                
        for i in BulletArray1:
            i.move()
            if i.bulletrect.colliderect(GunArray[0].gunrect) and GunArray[0].alive and GunArray[0].invincible==False:
                GunArray[0].alive=False
                BulletArray1.remove(i)
                boom0.play()
                BulletArray0=[]
                pygame.display.set_caption("S0me0ne l0st! What a l0ser! Restart by clicking g")

            if i.dead():
                BulletArray1.remove(i)
        
        if GunArray[0].gunrect.colliderect(GunArray[1].gunrect) and GunArray[1].alive and GunArray[0].alive:
                if GunArray[0].invincible==False and GunArray[1].invincible==False:
                    
                    GunArray[0].alive=False
                    boom0.play()
                    BulletArray0=[]
                    GunArray[1].alive=False
                    boom1.play()
                    BulletArray1=[]
                    pygame.display.set_caption("Y0u 10sers c011ided with each 0ther! Restart by clicking g")
                elif GunArray[0].invincible==False:
                    
                    GunArray[0].alive=False
                    boom0.play()
                    BulletArray0=[]
                    pygame.display.set_caption("S0me0ne l0st! What a l0ser! Restart by clicking g")
                elif GunArray[1].invincible==False:
                    
                    GunArray[1].alive=False
                    boom1.play()
                    BulletArray1=[]
                    pygame.display.set_caption("Someone 1ost! What a 1oser! Restart by clicking g.")    
        
        ColorBack=(255,255,255)    
        background.fill(ColorBack)
        
        pygame.display.update()
        screen.blit(background,(0,0))
        pygame.draw.rect(screen,(0,0,0),Rect(gravityx,gravityy,2,2))
        timeCount+=1
        time.sleep(0.01)
        
        #print (GunArray[0].acc,GunArray[1].acc)
     
if __name__ == '__main__':
    main()
    