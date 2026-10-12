import numpy as np
import matplotlib.pyplot as plt
import random as r
import time as tt
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
    def __init__(self,x,y,vx,vy,rad,c,energy,m):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.energy=energy
        self.radius = rad
        self.color = c
        self.mass=m
        self.ax = 0.0
        self.ay = 0.0
        self.ax_new = 0.0
        self.ay_new = 0.0

    def move(self, dt, lx, ly, e):
        self.x += self.vx * dt + 0.5 * self.ax * dt**2
        self.y += self.vy * dt + 0.5 * self.ay * dt**2

        if self.x + self.radius >= lx and self.vx > 0:
            self.vx = -e * self.vx

        elif self.x - self.radius <= 0 and self.vx < 0:
            self.vx = -e * self.vx

        if self.y + self.radius >= ly and self.vy > 0:
            self.vy = -e * self.vy

        elif self.y - self.radius <= 0 and self.vy < 0:
            self.vy = -e * self.vy

    def kick(self, dt):
        self.vx += 0.5 * (self.ax + self.ax_new) * dt
        self.vy += 0.5 * (self.ay + self.ay_new) * dt
        self.ax = self.ax_new
        self.ay = self.ay_new

    def __repr__(self):
        return f"Particle(x={self.x}, y={self.y})"
start= tt.perf_counter()
# def collision(p,a:particle):
    # for _ in p:
    #     if a != _:
    #         dist = np.sqrt((a.x - _.x) ** 2+(a.y - _.y) ** 2)
    #         if dist <= a.radius:
    #             a.vx = -a.vx
    #             a.vy = -a.vy
in_time=0
n=5
T=1
constant_restitution = 1
lx,ly=30,30
eps,sigma=1.0,1.0
color = plt.cm.hsv(np.linspace(0, 1, n))
p=[]
#creating particles
for _ in range(n):
    while True:
        x, y = r.randint(1, lx - 1), r.randint(1, lx - 1)
        if all(np.hypot(x - q.x, y - q.y) > 1.5 * sigma for q in p):
            break
    vx,vy=r.gauss(0,1),r.gauss(0,1)
    e=constant_restitution
    rad=0.2
    m=r.randint(1,10)
    c=color[_]
    i=particle(x,y,vx,vy,rad,c,e,m)
    p.append(i)
    
def near_par(a:particle):
    proc=False
    inf_r= (a.x**2 + a.y**2)**0.5 + 2.5
    gx, gy = np.arange(-inf_r, inf_r, 0.625), np.arange(-inf_r, inf_r,0.625)
    for _ in p:
        if _ is not a:
            dist= np.sqrt((a.x-_.x)**2 + (a.y-_.y)**2)
            if dist <= inf_r:
                proc=True
            else:
                proc=False
    return proc

#leynard potential force cal
def leynard(a,p_list):
    Fx,Fy=0.0,0.0
    for b in p_list:
        if b is not a:
            proc=near_par(b)
            if proc==True:
                rx,ry=a.x-b.x,a.y-b.y
                r2=rx**2+ry**2
                s6=(sigma**2/r2)**3
                f=24*eps*(2*s6**2-s6)/r2
                Fx+=f*rx
                Fy+=f*ry
    return Fx,Fy

def lj_potential(p_list):
    U=0.0
    for i in range(len(p_list)):
        for j in range(i+1,len(p_list)):
            r2=(p_list[i].x-p_list[j].x)**2+(p_list[i].y-p_list[j].y)**2
            s6=(sigma**2/r2)**3
            U+=4*eps*(s6**2-s6)
    return U

def acc(p_list, new=False):
    for a in p_list:
        Fx,Fy=leynard(a,p_list)
        if new:
            a.ax_new,a.ay_new=Fx/a.mass,Fy/a.mass
        else:
            a.ax,a.ay=Fx/a.mass,Fy/a.mass
acc(p)

dt=0.0005
steps_per_frame=20
nframes = 1000

energy = []
time = []
pos_hist = []

def advance(frame):
    for _ in range(steps_per_frame):
        for particle in p:
            particle.move(dt,lx,ly,1)
        acc(p,new=True)
        for particle in p:
            particle.kick(dt)

    e=lj_potential(p)
    for i in p:
        e+=0.5*i.mass*(i.vx**2+i.vy**2)
    energy.append(e)
    time.append(frame*steps_per_frame*dt)
    pos_hist.append([(q.x, q.y) for q in p])

for frame in range(nframes):
    advance(frame)

energy = np.array(energy)
np.savez("run.npz", pos=np.array(pos_hist), t=np.array(time), E=energy,
         lx=lx, ly=ly, colors=color)

plt.plot(time,energy)

plt.xlabel("t"); plt.ylabel("Energy")
plt.show()
end= tt.perf_counter()
print(end-start)
near=[]
for i in range(0,2):
    if p[i] is not p[1]:
        proc=near_par(p[i])
        if proc==True:
            near.append(p[i])
print(near)
