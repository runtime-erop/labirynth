import pygame as pg
import random

w, h = 600, 650
rows, cols = 20, 20
cell = w // cols

colors = {
    'bg': (30, 30, 46),
    'wall': (137, 180, 250),
    'player': (245, 194, 231),
    'text': (166, 227, 161)
}

pg.init()
screen = pg.display.set_mode((w, h))
font = pg.font.SysFont('Arial', 30)
clock = pg.time.Clock()

controls = {
    pg.K_w: (-1, 0),
    pg.K_s: (1, 0),
    pg.K_a: (0, -1),
    pg.K_d: (0, 1)
}
key = None

def make_maze():
    grid = [[1]*cols for _ in range(rows)]
    stack = [(random.randrange(rows//2)*2, random.randrange(cols//2)*2]
    
    while stack:
        x,y = stack[-1]
        grid[x][y] = 0
        
        options = []
        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            nx,ny = x+dx,y+dy
            if 0<=nx<rows and 0<=ny<cols and grid[nx][ny]:
                options.append((nx,ny))
        
        if options:
            nx,ny = random.choice(options)
            grid[(x+nx)//2][(y+ny)//2] = 0
            stack.append((nx,ny))
        else:
            stack.pop()
    
    grid[rows-1][0] = grid[0][cols-1] = 0
    return grid

def find_empty(x,y):
    q = [(x,y)]
    seen = set()
    
    while q:
        cx,cy = q.pop(0)
        if not maze[cx][cy]:
            return [cx,cy]
        
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx,ny = cx+dx,cy+dy
            if 0<=nx<rows and 0<=ny<cols and (nx,ny) not in seen:
                q.append((nx,ny))
                seen.add((nx,ny))

maze = make_maze()
player = [rows-1, 0]
shift_time = 5000
last_shift = pg.time.get_ticks()
last_move = 0

def draw():
    screen.fill(colors['bg'])
    
    for x in range(rows):
        for y in range(cols):
            if maze[x][y]:
                pg.draw.rect(screen, colors['wall'], (y*cell, x*cell, cell, cell))
    
    pg.draw.rect(screen, colors['player'], 
                (player[1]*cell+cell//4, player[0]*cell+cell//4, cell//2, cell//2))
    
    time_left = max(0, shift_time - (pg.time.get_ticks() - last_shift))
    timer = font.render(f"Shift in: {time_left//1000}", True, colors['text'])
    screen.blit(timer, (10, 10))
    
    pg.display.flip()

running = True
while running:
    clock.tick(30)
    
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        elif e.type == pg.KEYDOWN and e.key in controls:
            key = e.key
        elif e.type == pg.KEYUP and e.key == key:
            key = None
    
    if key and pg.time.get_ticks() - last_move > 100:
        dx,dy = controls[key]
        nx,ny = player[0]+dx, player[1]+dy
        if 0<=nx<rows and 0<=ny<cols and not maze[nx][ny]:
            player = [nx,ny]
        last_move = pg.time.get_ticks()
    
    if pg.time.get_ticks() - last_shift > shift_time:
        if random.random() < 0.2:
            rows += 1
            cols += 1
            cell = w // cols
        
        maze = make_maze()
        if maze[player[0]][player[1]]:
            player = find_empty(*player)
        last_shift = pg.time.get_ticks()
    
    draw()

pg.quit()
