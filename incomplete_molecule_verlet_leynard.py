import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import random as r

def make_grid(p_list, lx, ly, cell_size):
    grid = {}
    for particle in p_list:
        # Determine which cell contains the particle
        cell_x = int(particle.x // cell_size)
        cell_y = int(particle.y // cell_size)
        cell = (cell_x, cell_y)
        if cell not in grid:
            grid[cell] = []
        grid[cell].append(particle)
    return grid

def plot_walls(ax,width, height):
    # Bottom wall
    x1 = [0, width]
    y1 = [0, 0]

    # Top wall
    x2 = [0, width]
    y2 = [height, height]

    # Left wall
    x3 = [0, 0]
    y3 = [0, height]

    # Right wall
    x4 = [width, width]
    y4 = [0, height]

    plt.plot(x1, y1, 'k-')
    plt.plot(x2, y2, 'k-')
    plt.plot(x3, y3, 'k-')
    plt.plot(x4, y4, 'k-')

    plt.axis("equal")

class particle():
    def __init__(self,m,x,y,vx,vy,rad,c,energy,ax=0,ay=0):
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.energy=energy
        self.radius = rad
        self.color = c
        self.ax= ax
        self.ay= ay

    def move(self, dt, lx, ly, e):
        self.x += self.vx * dt + 0.5 * self.ax * dt**2
        self.y += self.vy * dt + 0.5 * self.ay * dt**2

        if self.x + self.radius >= lx:
            self.vx = -e * self.vx

        elif self.x - self.radius <= 0:
            self.vx = -e * self.vx

        if self.y + self.radius >= ly:
            self.vy = -e * self.vy

        elif self.y - self.radius <= 0:
            self.vy = -e * self.vy
    
    def vel_change(self,new_ax, new_ay, dt):
        self.vx += 0.5 * (self.ax + new_ax) * dt
        self.vy += 0.5 * (self.ay + new_ay) * dt
        self.ax = new_ax
        self.ay = new_ay
    # def coulomb(other):

    def __repr__(self):
        return f"Particle(x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy})"

def ac(a, grid, cell_size, ep, si, radinf=2.5):

    ax = 0.0
    ay = 0.0
    cell_x = int(a.x // cell_size)
    cell_y = int(a.y // cell_size)
    ncell = int(np.ceil(radinf / cell_size))
    for gx in range(cell_x - ncell, cell_x + ncell + 1):
        for gy in range(cell_y - ncell, cell_y + ncell + 1):
            cell = (gx, gy)
            if cell not in grid:
                continue
            for particle_j in grid[cell]:
                if particle_j is a:
                    continue
                dx = (particle_j.x - a.x)*0.1
                dy = (particle_j.y -a.y)*0.1

                dist2 = dx**2 + dy**2
                if dist2 > radinf**2:
                    continue

                dist = np.sqrt(dist2)
                if dist > a.radius:
                    sr6 = (si / dist)**6
                    sr12 = sr6**2
                    force = (24*ep*(2 * sr12 - sr6)/dist)
                    if dist < 2:
                        fx = -force * dx / dist
                        fy = -force * dy / dist
                        ax -= fx / a.m
                        ay -= fy / a.m
                    else:
                        fx = force * dx / dist
                        fy = force * dy / dist
                        ax += fx / a.m
                        ay += fy / a.m
    return ax, ay


n=6
T=10
ep=1
si=2
cell_size=0.3
radinf=2
constant_restitution = 1
lx,ly=30,30
dx=lx/10
dy=ly/10
color = plt.cm.hsv(np.linspace(0, 1, n))
p=[]
for _ in range(n):
    m = r.randint(1,5)
    x,y=r.randint(1,lx-1),r.randint(1,lx-1)
    vx,vy=r.gauss(),r.gauss()
    e=constant_restitution
    rad=0.8
    c=color[_]
    i=particle(m,x,y,vx,vy,rad,c,e)
    p.append(i)
vels=[]
for _ in p:
    v=np.sqrt(_.vx**2+_.vy**2)
    vels.append(v)
dt=(np.sqrt(dx**2+dy**2))/(20.0*(max(vels)))
fig, ax = plt.subplots()
ax.set_xlim(0, lx)
ax.set_ylim(0, ly)
ax.set_aspect("equal")
plot_walls(ax, lx, ly)
motion = []
energy = []
time = []
for particle in p:
    point, = ax.plot([particle.x], [particle.y], "o",color=particle.color)
    motion.append(point)

def update(frame):
    grid = make_grid(p,lx,ly,cell_size)

    for particle in p:

        ax, ay = ac(particle,grid,cell_size,ep,si,radinf)
        particle.ax = ax
        particle.ay = ay

    for particle in p:
        particle.move(dt,lx,ly,1)  
    new_grid = make_grid(p, lx, ly, cell_size)

    n_acc=[]
    for particle in p:

        ax, ay = ac(particle,new_grid,cell_size,ep,si,radinf)
        n_acc.append((ax, ay))
    for i, particle in enumerate(p):

        n_ax, n_ay = n_acc[i]
        particle.vel_change(n_ax,n_ay,dt)

    for particle, point in zip(p, motion):
        point.set_data([particle.x], [particle.y])
    
    e = 0

    #Kinetic
    for i in p:
         e+= i.m * 0.5 * (i.vx**2 + i.vy**2)

    # Lennard energy
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            dx = p[j].x - p[i].x
            dy = p[j].y - p[i].y
            dist = np.sqrt(dx**2 + dy**2)
            if dist > np.sqrt(5):
                e += 4*ep*((si/dist)**12-(si/dist)**6)

    energy.append(e)
    time.append(frame*dt)
    return motion



ani = anim.FuncAnimation(
    fig,
    update,
    frames=1000,
    interval=20,
    blit=False
)
plt.show()
plt.plot(time,energy)
plt.show()
