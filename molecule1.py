import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import random as r

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
    def __init__(self,x,y,vx,vy,rad,c,energy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.energy=energy
        self.radius = rad
        self.color = c

    def move(self, dt, lx, ly, e):
        self.x += self.vx * dt
        self.y += self.vy * dt - 0.5 * g * dt**2
        self.vy -= g * dt

        if self.x + self.radius >= lx:
            penetration = self.x + self.radius - lx
            self.x = lx - self.radius - penetration
            self.vx = -e * self.vx

        elif self.x - self.radius <= 0:
            penetration = -(self.x - self.radius)
            self.x = self.radius + penetration
            self.vx = -e * self.vx

        if self.y + self.radius >= ly:
            penetration = self.y + self.radius - ly
            self.y = ly - self.radius - penetration
            self.vy = -e * self.vy

        elif self.y - self.radius <= 0:
            penetration = -(self.y - self.radius)
            self.y = self.radius + penetration
            self.vy = -e * self.vy
    # def coulomb(other):

    def __repr__(self):
        return f"Particle(x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy})"

def collision(p,a:particle):
    for _ in p:
        if a != _:
            dist = np.sqrt((a.x - _.x) ** 2+(a.y - _.y) ** 2)
            if dist <= a.radius:
                a.vx = -a.vx
                a.vy = -a.vy

n=1
T=10
constant_restitution = 1
lx,ly=30,30
dx=lx/10
dy=ly/10
g=1
color = plt.cm.hsv(np.linspace(0, 1, n))
p=[]
for _ in range(n):
    x,y=r.randint(1,lx-1),r.randint(1,lx-1)
    vx,vy=r.gauss(),r.gauss()
    e=1
    rad=0.2
    c=color[_]
    i=particle(x,y,vx,vy,rad,c,e)
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
    for particle, point in zip(p, motion):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        particle.move(dt,lx,ly,1)        
        # collision(p, particle)
        point.set_data([particle.x], [particle.y])
    
    e=0
    for i in p:
        e+=0.5*(i.vx**2+i.vy**2)+g*i.y
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
