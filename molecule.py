import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

def line(x):
    y=np.linspace(0,10,100)
    return y

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

n=1
T=1000
lx,ly=10,10
dx=lx/10
dy=ly/10
vx,vy=2,1
dt=(np.sqrt(dx**2+dy**2))/20*(np.sqrt(vx**2+vy**2))
p1,p2=5,5

fig, ax = plt.subplots()

ax.set_xlim(0, lx)
ax.set_ylim(0, ly)
ax.set_aspect("equal")

plot_walls(ax, lx, ly)
trajectory, = ax.plot([], [], "b-", linewidth=1)
particle, = ax.plot([p1], [p2], "ro")

x = []
y = []

def update(frame):
    global p1, p2, vx, vy

    p1 += vx * dt
    p2 += vy * dt

    if p1 >= lx:
        p1 = lx
        vx = -vx
    elif p1 <= 0:
        p1 = 0
        vx = -vx

    if p2 >= ly:
        p2 = ly
        vy = -vy
    elif p2 <= 0:
        p2 = 0
        vy = -vy

    x.append(p1)
    y.append(p2)

    # trajectory
    trajectory.set_data(x, y)

    # current particle
    particle.set_data([p1], [p2])
    return trajectory, particle
ani = anim.FuncAnimation(
    fig,
    update,
    frames=1000,
    interval=20,
    blit=True
)

plt.show()
