import matplotlib.pyplot as plt
import numpy as np

r=0.1
s=0.3
r0=[0.01,1,2,1.5]
s0=[2,1,2,1.5]
dt=10**(-3)
T=100
a=3
b=2
c=1
d=2
e=1
f=1
rt=[]
st=[]
time=[]
t=0
plt.figure(figsize=(8, 6))
for rabbits in r0:
    for sheep in s0:
        r=rabbits
        s=sheep
        rt=[]
        st=[]
        t=0
        while t<T:
            r_dot=a*s-b*r*s-c*(r**2)
            s_dot=d*r-e*s*r-f*(s**2)
            rt.append(r)
            st.append(s)
            r=r+r_dot*dt
            s=s+s_dot*dt
            t+=dt
        plt.plot(rt, st)
plt.xlabel('Rabbits population')
plt.ylabel('Sheep population')
plt.show()

# plt.figure(figsize=(8, 6))
# while t<T:
#     r_dot=a*s-b*r*s-c*(r**2)
#     s_dot=d*r-e*s*r-f*(s**2)
#     time.append(t)
#     rt.append(r)
#     st.append(s)
#     t=t+dt
#     r = r+r_dot*dt
#     s = s+s_dot*dt
#     t+=dt
# plt.plot(time,rt)
# plt.plot(time,st)
# plt.legend(['r','s'])
# plt.show()

