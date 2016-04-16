'''
Created on Feb 13, 2015

@author: Nicky
'''

import pygame,sys,time,math,random
import pygame.gfxdraw, pygame.mixer
from pygame.locals import *

size = width, height= 640, 640
screen = pygame.display.set_mode(size)
pygame.mixer.init()

class Enemy(object):
    
    def __init__(self):
        
        self.x_size, self.y_size = random.randint(20,40),random.randint(20,40)
        self.x, self.y =random.randint(0,width-self.x_size),random.randint(0,80)
        self.vel=6*random.random()-3
        self.enemy_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
        self.color_bullet=(255,0,0)
        self.reload_ready, self.reload_time=0,60
        self.firing_type=random.randint(0,1)
   
    def moveDraw(self):
        
        if random.randint(0,99)==0:
            self.vel=6*random.random()-3
        self.enemy_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
        pygame.draw.rect(screen,self.color_bullet,self.enemy_rect)
        self.x+=self.vel
        if self.x<0:   
            self.vel=-self.vel
        if self.x>width-self.x_size:
            self.vel=-self.vel
        

    def reloadEnemy(self):
        
            self.reload_ready=self.reload_time  
              
class Bullet(object):
    
    def __init__(self,Gun,theta):
        self.theta=theta
        self.x_size, self.y_size=4,4
        self.x, self.y = Gun.x+Gun.x_size/2-self.x_size/2, Gun.y
        self.bullet_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
        self.color_bullet=(0,0,0)
        
    def moveDraw(self):
        
        self.bullet_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
        pygame.draw.rect(screen,self.color_bullet,self.bullet_rect)
        self.y-=10*math.sin(self.theta)
        self.x+=10*math.cos(self.theta)
        
    def out_of_bounds(self):
        
        if self.y<-self.y_size:
            return True
        else:
            return False

class EnemyBullet(object):
    
    def __init__(self,Enemy,Gun):
        
        if Enemy.firing_type==0:
            self.x_size, self.y_size=10,10
            self.x, self.y = Enemy.x+Enemy.x_size/2-self.x_size/2, Enemy.y+Enemy.y_size
            self.velx=5*(Gun.x+Gun.x_size/2-self.x_size/2-self.x)/math.sqrt((Gun.x+Gun.x_size/2-self.x_size/2-self.x)**2+(Gun.y-self.y)**2)
            self.vely=5*(Gun.y-self.y)/math.sqrt((Gun.x+Gun.x_size/2-self.x_size/2-self.x)**2+(Gun.y-self.y)**2)
            self.enemy_bullet_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
            self.color_enemy_bullet=(0,128,64)
        else:
            self.x_size, self.y_size=20,20
            self.x, self.y = Enemy.x+Enemy.x_size/2-self.x_size/2, Enemy.y+Enemy.y_size
            #self.velx=5*(Gun.x+Gun.x_size/2-self.x_size/2-self.x)/math.sqrt((Gun.x+Gun.x_size/2-self.x_size/2-self.x)**2+(Gun.y-self.y)**2)
            #self.vely=5*(Gun.y-self.y)/math.sqrt((Gun.x+Gun.x_size/2-self.x_size/2-self.x)**2+(Gun.y-self.y)**2)
            self.velx=0
            self.vely=8
            self.enemy_bullet_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
            self.color_enemy_bullet=(0,64,128)
        
    def moveDraw(self):
        
        self.enemy_bullet_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
        pygame.draw.rect(screen,self.color_enemy_bullet,self.enemy_bullet_rect)
        self.y+=self.vely
        self.x+=self.velx
        
    def out_of_bounds(self):
        if self.y>height:
            return True
        else:
            return False


class Gun(object):
    
    def __init__(self,color_gun):
        
        self.alive=True
        self.x, self.y, self.x_size, self.y_size = 300,600,40,40
        self.gun_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
        self.color_gun=color_gun
        self.vel=0
        self.vel_max=10
        self.acc=0.5
        self.reload_ready, self.reload_time=0,12
    
    def redraw(self, gun_type):
        
        if self.alive:
            self.color_gun=(0,0,255/2**(gun_type-1))
            self.gun_rect=Rect((self.x,self.y),(self.x_size,self.y_size))
            pygame.draw.rect(screen,self.color_gun,self.gun_rect)
            
    def move(self):
        
        if self.x<0:   
            self.x=0
        if self.x>width-self.x_size:
            self.x=width-self.x_size
        
        if self.vel>=self.acc:
            self.vel-=self.acc
        if self.vel<=-self.acc:
            self.vel+=self.acc               
        if self.vel<self.acc and self.vel>-self.acc:
            self.vel=0   
        
        self.x+=self.vel
            
    def accelerate(self, boole):
        
        if self.vel<self.vel_max and boole:
            self.vel+=2*self.acc
        if self.vel>-self.vel_max and boole==False:
            self.vel-=2*self.acc
                
    def reloadGun(self):
        
            self.reload_ready=self.reload_time                     
            

def main():
   
    background=pygame.Surface(screen.get_size())
    background=background.convert()
    pygame.display.set_caption("0")
    color_back=(255,255,255)    
    background.fill(color_back)
    a_down,d_down,space_down=False,False,False
    GA=[Gun((0,0,255))]
    BulletArray=[]
    EnemyArray=[]
    EnemyBulletArray=[]
    time_count=0
    enemy_spawn_rate=100
    gun_type=1
    gun_points=1
    
    
    while 1:
        
        
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: sys.exit()
            
            if event.type==KEYDOWN:
                
                if event.key == K_g and not GA[0].alive:
                    
                    a_down,d_down,space_down=False,False,False
                    GA=[Gun((0,0,255))]
                    BulletArray=[]
                    EnemyArray=[]
                    EnemyBulletArray=[]
                    time_count=0
                    enemy_spawn_rate=100
                    gun_type=1
                    gun_points=1
                    
                    
                if event.key == K_a:
                    a_down=True
                if event.key == K_d:
                    d_down=True
                if event.key == K_SPACE:
                    space_down=True
                    
            if event.type==KEYUP:
                if event.key == K_a:
                    a_down=False
                if event.key == K_d:
                    d_down=False
                if event.key== K_SPACE:
                    space_down=False 
            
        if a_down:
            GA[0].accelerate(False)
        if d_down:
            GA[0].accelerate(True)
        if space_down and GA[0].reload_ready<=0 and GA[0].alive:
            GA[0].reloadGun()
            if gun_type==1:
                BulletArray.append(Bullet(GA[0],math.pi/2))
            elif gun_type==2:
                GA[0].reload_time=6
                BulletArray.append(Bullet(GA[0],math.pi*80/180+math.pi*20/180*random.random()))
            elif gun_type==3:
                GA[0].reload_time=12
                BulletArray.append(Bullet(GA[0],math.pi/2))
                BulletArray.append(Bullet(GA[0],math.pi*80/180))
                BulletArray.append(Bullet(GA[0],math.pi*100/180))
            elif gun_type>=4:
                GA[0].reload_time=3
                BulletArray.append(Bullet(GA[0],math.pi*75/180+math.pi*30/180*random.random()))
            
        GA[0].move()
        GA[0].redraw(gun_type)
        GA[0].reload_ready-=1
        
        for i in BulletArray:
            i.moveDraw()
            if i.out_of_bounds():
                BulletArray.remove(i)
                
            else:
                dead=False
                for j in EnemyBulletArray:
                    if i.bullet_rect.colliderect(j.enemy_bullet_rect):
                        EnemyBulletArray.remove(j)
                        BulletArray.remove(i)
                        dead=True
                        
                        break
                if not dead:
                    for j in EnemyArray:
                        if i.bullet_rect.colliderect(j.enemy_rect):
                            EnemyArray.remove(j)
                            BulletArray.remove(i)
                            gun_points+=1
                        
                            break
            
        
        if GA[0].alive:
            time_count+=1
        
        if time_count%enemy_spawn_rate==0:
            EnemyArray.append(Enemy())
        if time_count%100==0 and enemy_spawn_rate>=25:
            enemy_spawn_rate-=1
        if gun_points>=135:
            gun_type=4
        elif gun_points>=54:
            gun_type=3
        elif gun_points>=18:
            gun_type=2
        
            
                
            
        for i in EnemyArray:           
            i.moveDraw()
            if i.reload_ready<=0:
                i.reloadEnemy()
                EnemyBulletArray.append(EnemyBullet(i,GA[0]))
            i.reload_ready-=1
            
        for i in EnemyBulletArray:
            i.moveDraw()
                
            if GA[0].alive and i.enemy_bullet_rect.colliderect(GA[0].gun_rect):
                GA[0].alive=False
            elif i.out_of_bounds():
                EnemyBulletArray.remove(i)       
        
        if GA[0].alive:         
            pygame.display.set_caption("%d" %gun_points)
        else:
            pygame.display.set_caption("you died m9! g to restart %d" %gun_points)
            
        pygame.display.update()
        screen.blit(background,(0,0))
        time.sleep(0.01)
        print (len(BulletArray))   

if __name__ == '__main__':
    main()
    