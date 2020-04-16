#SNAKE BY NAGAARON#

#FRAMEWORKS-------------------------------------------------------------------

import pygame
import random

#CLASSES----------------------------------------------------------------------

#Cube Class
class Cube(object):
    def __init__(self,x,y,color,dirnx=1,dirny=0,):
        self.pos = (x,y)
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        self.r = 50
    def move(self,dirnx,dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos =(self.pos[0]+self.dirnx*self.r, self.pos[1]+self.dirny*self.r)
        
    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.pos[0],self.pos[1],self.r,self.r))
    
#Snake Class
class Snake(object):
    
    body =[]    	   # list of Cube Objects
    turns = {}        # dictionary with tunrs
    
    def __init__(self,r):
        
        self.head = Cube(50,100,(255,0,0))
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0
        
    def move(self,window,s):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_COMMA]:
            self.add_cube()
            
        if keys[pygame.K_SPACE]:
            self.reset()

        if keys[pygame.K_LEFT] and (self.dirnx != 1 and self.dirny != 0):
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        if keys[pygame.K_RIGHT] and (self.dirnx != -1 and self.dirny != 0):
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        if keys[pygame.K_UP] and (self.dirnx != 0 and self.dirny != 1):
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        if keys[pygame.K_DOWN] and (self.dirnx != 0 and self.dirny != 1):
            self.dirnx = 0
            self.dirny = 1 
            self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]

        for j,i in enumerate(self.body):
            p = i.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                i.move(turn[0],turn[1])
                if j==len(self.body)-1:
                    self.turns.pop(p)
            else:
                if i.dirnx == -1 and i.pos[0] <= 0:
                    i.pos = (s-i.r,i.pos[1])
                elif i.dirnx == 1 and i.pos[0] >= s-i.r:
                    i.pos = (0,i.pos[1])
                elif i.dirny == 1 and i.pos[1] >= s-i.r:
                    i.pos = (i.pos[0],0)
                elif i.dirny == -1 and i.pos[1] <= 0:
                    i.pos = (i.pos[0],s-i.r)
                else:
                    i.move(i.dirnx,i.dirny)
            i.draw(window)
            if j !=0:
                if i.pos == self.body[0].pos:
                    self.reset()
                
                
    def add_cube(self):

        dx = self.body[-1].dirnx
        dy = self.body[-1].dirny
        if dx == 0 and dy == -1:
            self.body.append(Cube(self.body[-1].pos[0],self.body[-1].pos[1]+self.body[-1].r,(255,0,0)))
        if dx == 0 and dy == 1:
            self.body.append(Cube(self.body[-1].pos[0],self.body[-1].pos[1]-self.body[-1].r,(255,0,0)))
        if dx == 1 and dy == 0:
            self.body.append(Cube(self.body[-1].pos[0]-self.body[-1].r,self.body[-1].pos[1],(255,0,0)))
        if dx == -1 and dy == 0:
            self.body.append(Cube(self.body[-1].pos[0]+self.body[-1].r,self.body[-1].pos[1],(255,0,0)))    
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def reset(self): 
        self.head = Cube(2*self.head.r,2*self.head.r,(255,0,0))
        self.body = [self.head]
        self.turns ={}
        self.dirnx = 1
        self.dirny = 0
    
#FUNCTIONS--------------------------------------------------------------------

def neues_essen(window,schlange):
    global essen
    if schlange.body[0].pos == essen.pos:
        schlange.add_cube()
        newx = essen.r*round(random.randint(0,450)/essen.r)
        newy = essen.r*round(random.randint(0,450)/essen.r)
        essen = Cube(newx,newy,(0,0,255))


        
def draw_grid(window,s,r):
    for x in range(0,s,r):
        pygame.draw.line(window,(255,255,255),(x,0),(x,s))
        pygame.draw.line(window,(255,255,255),(0,x),(s,x))

def draw_window(window,s,r,schlange,essen):
    window.fill((0,0,0))
    schlange.move(window, s)
    essen.draw(window)
    draw_grid(window,s,r)
    pygame.display.update()
    
def main_loop():
    global essen
    screen_width = 500
    row_width = 50
    game_on = True
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((screen_width,screen_width))
    pygame.display.set_caption("Snake")
    essen = Cube(row_width*round(random.randint(0,450)/row_width),row_width*round(random.randint(0,450)/row_width),(0,0,255))
    schlange = Snake(row_width)
    while game_on:
        clock.tick(10)
        e_in_s = True
        draw_window(window,screen_width,row_width,schlange,essen)
        neues_essen(window,schlange)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
main_loop()      
