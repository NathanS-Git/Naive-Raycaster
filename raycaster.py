from pygame import *
from math import *
import random
init()
screen_width = 1600
screen_height = 900
screen = display.set_mode((screen_width,screen_height))
N = 200 # Number of rays
Nw = 10 # Number of walls
length = 1000 # Length of rays
move_speed = 8
look_speed = 10
fov = 0.3*pi # In radians
x,y = 0,0 # Starting position
raycaster_view = False # Default view, raycaster or first-person

key.set_repeat(1)
# Create random wall locations
seg = [[(random.randint(0,screen_width),random.randint(0,screen_height)),(random.randint(0,screen_width),random.randint(0,screen_height))] for _ in range(Nw)]
draw_width = screen_width/N
view_angle_offset = 0
drawing = True

def add__vec(p,q):
    return tuple(map(sum, zip(p,q)))

def sub_vec(p,q):
    return tuple(map(lambda xy: xy[0]-xy[1],zip(p,q)))

def dev_vec(p,q):
    return tuple(map(lambda xy: xy[0]/xy[1],zip(p,q)))

def mul_vec(p,q):
    return tuple(map(lambda xy: xy[0]*xy[1],zip(p,q)))

def cross_vec(p,q):
    return p[0]*q[1]-p[1]*q[0]

def dot_vec(p,q):
    return q[0]*p[0]+q[1]*p[1]

# Main display loop
while drawing:
    screen.fill((0,0,0))
    for e in event.get():
        #x,y = mouse.get_pos()

        if e.type == KEYDOWN:
            if e.key == K_w: # Move forward
                x += move_speed*cos((fov*(view_angle_offset+(N/2))/N))
                y += move_speed*sin((fov*(view_angle_offset+(N/2))/N))
            elif e.key == K_s: # Move backward
                x += move_speed*cos((fov*(view_angle_offset+(N/2))/N)+pi)
                y += move_speed*sin((fov*(view_angle_offset+(N/2))/N)+pi)
            if e.key == K_e: # Strafe right
                x += move_speed*cos((fov*(view_angle_offset+(N/2))/N)+pi/2)
                y += move_speed*sin((fov*(view_angle_offset+(N/2))/N)+pi/2)
            elif e.key == K_q: # Strafe left
                x += move_speed*cos((fov*(view_angle_offset+(N/2))/N)+3*pi/2)
                y += move_speed*sin((fov*(view_angle_offset+(N/2))/N)+3*pi/2)
            if e.key == K_a: # Look left
                view_angle_offset -= look_speed
            elif e.key == K_d: # Look right
                view_angle_offset += look_speed
            if e.key == K_v: # Change view
                raycaster_view = False if raycaster_view else True
            if e.key == K_ESCAPE: # Exit
                drawing = False
            
    if raycaster_view:
        for line in seg:
            draw.line(screen, (255,0,0), line[0], line[1])

    for l in range(N):
        dx = cos(fov*(l+view_angle_offset)/N)
        dy = sin(fov*(l+view_angle_offset)/N)
        x_0 = x+dx*length
        y_0 = y+dy*length
        rec_t = []
        for wall in seg:
            # Two vectors p+tr, and q+us
            # Implemented algorithm given from https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
            p = (x,y)
            r = (dx*length,dy*length)
            q = wall[0]
            s = tuple(map(lambda xy: xy[0]-xy[1], zip(wall[1],wall[0])))
            rxs = cross_vec(r,s)
            t = cross_vec(sub_vec(q,p),s)/rxs
            u = cross_vec(sub_vec(q,p),r)/rxs
            if rxs and 0 <= t <= 1 and 0 <= u <= 1:
                rec_t.append(t)
                x_0 = p[0]+min(rec_t)*r[0]
                y_0 = p[1]+min(rec_t)*r[1]

        height = 0
        colour = (0,0,0)
        if rec_t:
            angle = (fov*(view_angle_offset+(N/2))/N) - (fov*(l+view_angle_offset)/N)
            distance = min(rec_t)*abs(cos(angle)) # Obtaining true distance i.e. The shadow from the vector going to the wall, to the vector from where we view. This removes the fisheye effect
            height = (1/max(distance,0.1))*screen_height//10
            brightness = 1-sqrt(min(rec_t)) # Make brightness decay with the square of the distance
            colour = (brightness*255,brightness*255,brightness*255)

        if raycaster_view:
            draw.line(screen, (255,255,255), (x,y), (x_0,y_0))
        else:
            draw.rect(screen, colour, (draw_width*l,screen_height//2-height//2,screen_width//N,height))
    
    display.update() 
quit()