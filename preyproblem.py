import matplotlib.pyplot as plt
r=0.1
f=0.3
r0=[0.01,1,2,1.5]
f0=[2,1,2,1.5]
dt=10**(-4)
T=50
a=1.5
b=1
c=3
d=1
rt=[]
ft=[]
time=[]
t=0
plt.figure(figsize=(8, 6))
R, F = np.meshgrid(
    np.linspace(0, 25, 10),
    np.linspace(0, 25, 10)
)

R_dot = a*R - b*R*F
F_dot = -c*F + d*F*R

plt.quiver(
    R, F,
    R_dot, F_dot,
    angles='xy',
    scale_units='xy',
    scale=100,
    width=0.002
)
for rabbits in r0:
    for fox in f0:
        r=rabbits
        f=fox
        rt=[]
        ft=[]
        t=0
        while t<T:
            r_dot=a*r-b*r*f
            f_dot=-c*f+d*f*r
            rt.append(r)
            ft.append(f)
            r=r+r_dot*dt
            f=f+f_dot*dt
            t+=dt
        plt.plot(rt,ft)
plt.xlabel('Rabbits population')
plt.ylabel('Fox population')
plt.scatter(0,0)
plt.scatter(3,1.5)
plt.show()

# plt.figure(figsize=(8, 6))
# while t<T:
#     r_dot=a*r-b*r*f
#     f_dot=-c*f+d*f*r
#     time.append(t)
#     rt.append(r)
#     ft.append(f)
#     t=t+dt
#     r = r+r_dot*dt
#     f = f+f_dot*dt
#     t+=dt
# plt.plot(time,rt)
# plt.plot(time,ft)
# plt.show()
