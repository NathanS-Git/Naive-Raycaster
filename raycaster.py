from pygame import *
from math import *
import random

init()

screen_width = 1600
screen_height = 900
screen = display.set_mode((screen_width,screen_height))
N = 200 # Number of rays
Nw = 10 # Number of walls
length = 2000 # Length of rays
move_speed = 8
look_speed = 7 # Rotation speed
fov = 0.5*pi # In radians
x,y = 0,0 # Starting position
raycaster_view = False # Default view, raycaster or first-person
tick = 0

key.set_repeat(1)
# Create random wall locations
seg = [[(random.randint(0,screen_width),random.randint(0,screen_height)),(random.randint(0,screen_width),random.randint(0,screen_height))] for _ in range(Nw)]

draw_width = screen_width//N
view_angle_offset = 0
drawing = True
clock = time.Clock()

def add_vec(p,q):
    return tuple(map(sum, zip(p,q)))

def sub_vec(p,q):
    return tuple(map(lambda xy: xy[0]-xy[1],zip(p,q)))

def dev_vec(p,q):
    return tuple(map(lambda xy: xy[0]/xy[1],zip(p,q)))

def mul_vec(p,q):
    return tuple(map(lambda xy: xy[0]*xy[1],zip(p,q)))

def cross_vec(p,q): # Defined 2D cross vector calculation
    return p[0]*q[1]-p[1]*q[0]

def dot_vec(p,q):
    return q[0]*p[0]+q[1]*p[1]

# Main display loop
while drawing:
    clock.tick(30)
    screen.fill((0,0,0))
    keys = key.get_pressed()
    event.get()
    if tick < 100:
        tick += 1
    
    if keys[K_w]: # Move forwards
        x += move_speed*cos((fov*(view_angle_offset+(N/2))/N))
        y += move_speed*sin((fov*(view_angle_offset+(N/2))/N))
    elif keys[K_s]: # Move backward
        x += move_speed*cos((fov*(view_angle_offset+(N/2))/N)+pi)
        y += move_speed*sin((fov*(view_angle_offset+(N/2))/N)+pi)
    if keys[K_e]: # Strafe right
        x += move_speed*cos((fov*(view_angle_offset+(N/2))/N)+pi/2)
        y += move_speed*sin((fov*(view_angle_offset+(N/2))/N)+pi/2)
    elif keys[K_q]: # Strafe left
        x += move_speed*cos((fov*(view_angle_offset+(N/2))/N)+3*pi/2)
        y += move_speed*sin((fov*(view_angle_offset+(N/2))/N)+3*pi/2)
    if keys[K_a]: # Look left
        view_angle_offset -= look_speed
    elif keys[K_d]: # Look right
        view_angle_offset += look_speed
    if keys[K_v] and tick > 15: # Change view
        tick = 0 # Reset cooldown
        raycaster_view = False if raycaster_view else True
    if keys[K_ESCAPE]: # Exit
        drawing = False
      
    if raycaster_view:
        for line in seg:
            draw.line(screen, (100,100,100), line[0], line[1])
    else:
        draw.rect(screen, (90,90,90), (0,screen_height//2,screen_width,screen_height))

    for ray in range(N):
        dx = cos(fov*(ray+view_angle_offset)/N)
        dy = sin(fov*(ray+view_angle_offset)/N)
        x_0 = x+dx*length
        y_0 = y+dy*length
        rec_t = [] # Record t values from algorithm below
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
            angle = (fov*(view_angle_offset+(N/2))/N) - (fov*(ray+view_angle_offset)/N)
            distance = min(rec_t)*abs(cos(angle)) # Obtaining true distance i.e. The shadow from the vector going to the wall, to the vector from where we view. This removes the fisheye effect
            height = (1/max(distance,0.1))*screen_height//10
            brightness = 1-sqrt(min(rec_t)) # Make brightness decay with the square of the distance
            colour = (brightness*255,brightness*255,brightness*255)

        if raycaster_view:
            draw.line(screen, (255,255,255), (x,y), (x_0,y_0))
        else:
            draw.rect(screen, colour, (draw_width*ray,screen_height//2-height//2,screen_width//N,height))
    
    display.update() 
quit()
