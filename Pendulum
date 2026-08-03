#Code for simple pendulum simulation 
#can be worked on for visual addition as well

import numpy as np
import matplotlib.pyplot as plt

g=9.8
l=9.8
dt=0.01
T=50

intial_theta = [1, 10, 30, 50, 90, 120, 179.99]
rt = np.radians(intial_theta)
plt.figure(figsize=(8,6))
for th0 in rt:
    n = int(T/dt)
    theta = th0
    tdot = 0
    theta_array = []
    tdot_array = []
    t=0
    time=[]
    while t<=T:
        theta_array.append(theta)
        tdot_array.append(tdot)
        tdot=tdot+dt*(-g/l*np.sin(theta)) #comes form the lagrangian formalism for pendulum
        theta=theta+dt*tdot               #comes from the finite differences
        t+=dt
        time.append(t)
    plt.plot(theta_array, tdot_array, label=f"{np.degrees(th0):.0f}°")
    # plt.plot(time, theta_array, label=f"{np.degrees(th0):.0f}°")
plt.xlabel(r'$\theta$')
plt.ylabel(r'$\dot{\theta}$')
plt.grid(True)
plt.legend()
plt.show()
