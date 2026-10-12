import numpy as np
import matplotlib.pyplot as plt
import random as r
import time as tt

class particle():
    def __init__(self,x,y,z,vx,vy,vz,rad,c,cr,m):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.cons_res= cr
        self.radius = rad
        self.color = c
        self.mass=m
        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.0
        self.ax_new = 0.0
        self.ay_new = 0.0
        self.az_new = 0.0

    def move(self, dt, lx, ly, lz, e):
        self.x += self.vx * dt + 0.5 * self.ax * dt**2
        self.y += self.vy * dt + 0.5 * self.ay * dt**2
        self.z += self.vz *dt+ 0.5*self.az*dt**2

        if self.x + self.radius >= lx and self.vx > 0:
            self.vx = -e * self.vx

        elif self.x - self.radius <= 0 and self.vx < 0:
            self.vx = -e * self.vx

        if self.y + self.radius >= ly and self.vy > 0:
            self.vy = -e * self.vy

        elif self.y - self.radius <= 0 and self.vy < 0:
            self.vy = -e * self.vy
        
        if self.z + self.radius >= lz and self.vz > 0:
            self.vz = -e * self.vz

        elif self.z - self.radius <= 0 and self.vz < 0:
            self.vz = -e * self.vz

    def kick(self, dt):
        self.vx += 0.5 * (self.ax + self.ax_new) * dt
        self.vy += 0.5 * (self.ay + self.ay_new) * dt
        self.vz += 0.5 * (self.az + self.az_new) * dt
        self.ax = self.ax_new
        self.ay = self.ay_new
        self.az = self.az_new
    def __repr__(self):
        return f"Particle(x={self.x}, y={self.y}, z={self.z})"
start= tt.perf_counter()

n=50
T=1
constant_restitution = 0.8
lx,ly, lz=30,30,30
eps,sigma=1.0,1.0
color = plt.cm.hsv(np.linspace(0, 1, n))
r_infl = 2.5 
cell_size = r_infl
nx = int(np.ceil(lx / cell_size))
ny = int(np.ceil(ly / cell_size))
ny = int(np.ceil(lz / cell_size))
p=[]
#creating particles
for _ in range(n):
    while True:
        x, y, z= r.randint(1, lx - 1), r.randint(1, lx - 1), r.randint(1, lz - 1)
        if all(np.sqrt((x - q.x)**2 + (y - q.y)**2 + (z - q.z)**2)> 1.5 * sigma for q in p):
            break
    vx,vy,vz=r.gauss(0,1),r.gauss(0,1),r.gauss(0,1)
    e=constant_restitution
    rad=0.2
    m=r.randint(1,10)
    c=color[_]
    i=particle(x,y,z,vx,vy,vz,rad,c,e,m)
    p.append(i)

def build_grid(p_list):
    grid = {}

    for particle in p_list:
        # Find the cell containing this particle
        ix = int(particle.x/cell_size)
        iy = int(particle.y/cell_size)
        iz = int(particle.z/cell_size)
        cell = (ix, iy, iz)

        if cell not in grid:
            grid[cell] = []

        grid[cell].append(particle)

    return grid

def get_near(a, grid):
    near = []

    ix = int(a.x / cell_size)
    iy = int(a.y / cell_size)
    iz = int(a.z/cell_size)

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1,0,1):
                cell = (ix + dx, iy + dy, iz+dz)

                for b in grid.get(cell, []):
                    if b is a:
                        continue

                    rx = a.x - b.x
                    ry = a.y - b.y
                    rz=a.z-b.z

                    if 0 < rx**2 + ry**2 + rz**2<= r_infl**2:
                        near.append(b)

    return near

#leynard potential force cal
def leynard(a, grid):
    Fx, Fy, Fz = 0.0, 0.0, 0.0
    for b in get_near(a, grid):
        rx = a.x - b.x
        ry = a.y - b.y
        rz = a.z - b.z
        r2 = rx**2 + ry**2 + rz**2
        s6 = (sigma**2 / r2)**3
        f = 24 * eps * (2 * s6**2 - s6) / r2
        Fx += f * rx
        Fy += f * ry
        Fz += f * rz
    return Fx, Fy, Fz

def lj_potential(p_list):
    U = 0.0
    for i in range(len(p_list)):
        for j in range(i + 1, len(p_list)):
            dx = p_list[i].x - p_list[j].x
            dy = p_list[i].y - p_list[j].y
            dz = p_list[i].z - p_list[j].z

            r2 = dx**2 + dy**2 + dz**2

            if 0 < r2 <= r_infl**2:
                s6 = (sigma**2 / r2)**3
                U += 4 * eps * (s6**2 - s6)
    return U

def acc(p_list, new=False):
    grid = build_grid(p_list)
    for a in p_list:
        Fx, Fy, Fz = leynard(a, grid)
        if new:
            a.ax_new = Fx / a.mass
            a.ay_new = Fy / a.mass
            a.az_new = Fz / a.mass
        else:
            a.ax = Fx / a.mass
            a.ay = Fy / a.mass
            a.az = Fz / a.mass

# def par_coll(p,e):
#     for i in range(len(p_list)):
#         for j in range(i + 1, len(p_list)):
#             a = p_list[i]
#             b = p_list[j]

#             dx = b.x - a.x
#             dy = b.y - a.y
#             dz = b.z - a.z

#             dist2 = dx**2 + dy**2 + dz**2
#             min_dist = a.radius + b.radius
#             if dist2 == 0 or dist2 >= min_dist**2:
#                 continue
#             elif dist2 < min_dist**2:
#                 a.vx = -e*a.vx
#                 a.vy = -e*a.vy
#                 a.vz = -e*a.vz
            
#                 b.vx = -e*b.vx
#                 b.vy = -e*b.vy
#                 b.vz = -e*b.vz

dt=0.005
steps_per_frame=20
nframes = 1000

energy = []
time = []
pos_hist = []

def advance(frame):
    for _ in range(steps_per_frame):
        for particle in p:
            particle.move(dt,lx,ly,lz,1)
        acc(p,new=True)
        for particle in p:
            particle.kick(dt)

    e=lj_potential(p)
    for i in p:
        e+=0.5*i.mass*(i.vx**2+i.vy**2+i.vz**2)
    energy.append(e)
    time.append(frame*steps_per_frame*dt)
    pos_hist.append([(q.x, q.y ,q.z) for q in p])

for frame in range(nframes):
    advance(frame)
end= tt.perf_counter()
energy = np.array(energy)
np.savez("run.npz", pos=np.array(pos_hist), t=np.array(time), E=energy,
         lx=lx, ly=ly, lz=lz, colors=color)

plt.plot(time,energy)
# plt.xticks(np.arange(0, 101, 5))
# plt.axis("equal")
plt.xlabel("t"); plt.ylabel("Energy")
plt.show()

print(end-start)
