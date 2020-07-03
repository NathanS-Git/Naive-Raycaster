from pygame import *
from math import *
import random
init()
screen = display.set_mode((1600,900))
N = 300 # Number of rays
Nw = 10 # Number of walls
length = 2000 # Length of rays

def addVec(p,q):
    return tuple(map(sum, zip(p,q)))

def subVec(p,q):
    return tuple(map(lambda xy: xy[0]-xy[1],zip(p,q)))

def devVec(p,q):
    return tuple(map(lambda xy: xy[0]/xy[1],zip(p,q)))

def mulVec(p,q):
    return tuple(map(lambda xy: xy[0]*xy[1],zip(p,q)))

def crossVec(p,q):
    return p[0]*q[1]-p[1]*q[0]

def dotVec(p,q):
    return q[0]*p[0]+q[1]*p[1]

# Create wall locations
seg = [[(random.randint(0,1600),random.randint(0,900)),(random.randint(0,1600),random.randint(0,900))] for _ in range(Nw)]

while True:
    screen.fill((0,0,0))
    for e in event.get():
        x,y = mouse.get_pos()

    for line in seg:
        draw.line(screen, (255,0,0), line[0], line[1])

    for l in range(N):
        dx = cos((2*l*pi/N))
        dy = sin((2*l*pi/N))
        x_0 = x+dx*length
        y_0 = y+dy*length
        rect = []
        recu = []
        for line in seg:
            # Two vectors p+tr, and q+us
            # Implemented algorithm given from https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
            p = (x,y)
            r = (dx*length,dy*length)
            q = line[0]
            s = tuple(map(lambda xy: xy[0]-xy[1], zip(line[1],line[0])))
            t = crossVec(subVec(q,p),s)/crossVec(r,s)
            u = crossVec(subVec(q,p),r)/crossVec(r,s)
            test = crossVec(r,s)
            if test and 0 <= t <= 1 and 0 <= u <= 1:
                rect.append(t)
                recu.append(u)
                x_0 = p[0]+rect[rect.index(min(rect))]*r[0] 
                y_0 = p[1]+rect[rect.index(min(rect))]*r[1]
        
        draw.line(screen, (255,255,255), (x,y), (x_0,y_0))
    
    display.update() 
quit()