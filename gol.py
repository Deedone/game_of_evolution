import pygame
import sys
import random
from pygame.locals import *

class Cell:
    def __init__(self,alive=0,y=0,x=0):
        self.x = x
        self.y = y
        self.color = (200,200,200)
        self.alive = alive
        self.gen = [random.randint(0,1) for _ in range(8)] #generate random genome
        self.gen[2] = self.gen[3] = 0 #make shure that best-survivable cells would not appear at start

    def draw(self):
        if not self.alive:
            return
        self.color = (100*sum(self.gen[0:2]),100*sum(self.gen[2:4]),50*sum(self.gen[4:10]))
        pygame.draw.rect(screen,self.color,(self.x*SIZE,self.y*SIZE,SIZE,SIZE))


    def born(self):
        self.alive = 1
        for y,x in self.getnearest():
            if field[y][x].alive:
                self.gen = field[y][x].gen[:]#copy first encountered gene
                break
        if random.randint(0,100) == 50:
            self.gen[random.randint(0,7)] = random.randint(0,1)

    def move(self):
        global field
        if not self.alive:
            return
        arr = []
        self.alive = 0   #temporary pretend dead to avoid miscalculations

        for y,x in self.getnearest():
            if field[y][x].alive:
                continue
            n = self.check(1,y,x)
            if self.gen[n]:
                arr.append((y,x))
        self.alive = 1
        
        if len(arr)>0: #move to a random nice place
            y,x = arr[random.randint(0,len(arr)-1)]
            self.alive = 0
            field[y][x].alive = 1
            field[y][x].gen = self.gen[:]
        
            
    def check(self,ret=0,y=-1,x=-1): #checks if cell should be alive, returns number of alive neighbors if ret = 1
        if y==x==-1:
            y,x = self.y,self.x
        nei = sum([field[i][j].alive for i,j in self.getnearest(y,x)])
        if ret:
            return nei
        #return a rule for this cell, rules will be applyed after all cells checked
        if not self.alive and nei==3:   return (self,1)
        if self.alive and (nei<2 or nei>3): return (self,0)


    def getnearest(self,yb=-1,xb=-1):#returns a list of neighbors cells for a place
        if yb==xb==-1:
            yb,xb = self.y,self.x
        for i in range(-1,2):
            for j in range(-1,2):
                if i == j == 0:
                    continue
                y = yb+i
                x = xb+j
                #we don't want to go over the map
                if x < 0: x+=width//SIZE
                if x >= width//SIZE: x-=width//SIZE
                if y < 0: y+= height//SIZE
                if y >= height//SIZE: y-=height//SIZE
                yield (y,x)
                
#some initializations    
SIZE = 10
if len(sys.argv) == 3:
    width,height = int(sys.argv[1]),int(sys.argv[2])
else:
    width,height = 600,400
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Corpse\'s game of life ')
clock = pygame.time.Clock()
field = [[Cell(random.randint(0,1),y,x) for x in range(width//SIZE)] for y in range(height//SIZE)]
celllist = [cel for row in field for cel in row]

switch = 0
while True:#main loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            break
    screen.fill((50,50,50))
    switch = not switch
    
 
    if switch:
        random.shuffle(celllist) #make random order of moves
        for i in celllist:
                i.move()
    else:
        arr = []
        for i in celllist:
            resp = i.check()
            if resp != None: 
                arr.append(i.check())       
            
        
        for cell,alive in arr:
            if alive:
                cell.born()
            else:
                cell.alive = 0

    for c in celllist:
        c.draw()

    pygame.display.flip()
    clock.tick(30)
