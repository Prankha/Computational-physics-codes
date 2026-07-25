import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

n=1000
d=2
w=10000

p=0.5
q=1-p
wpos=0
pos=[]
xpos=[]
ypos=[]
def random_walk(n):
    global d
    wpos=0
    for i in range(n):
        r=np.random.uniform()
        if r<p:
            wpos=wpos+1
        else:
            wpos=wpos-1
    return wpos
def random_walk_2d(n):
    x = 0
    y = 0
    p = 0.25
    q = 0.5
    s = 0.75
    t = 1
    for _ in range(n):
        r = np.random.uniform()
        if r < p:
            x += 1
        elif r < q:
            x -= 1
        elif r < s:
            y += 1
        else:
            y -= 1

    return x, y
def random_walk_3d(n):
    x, y, z = 0, 0, 0
    for _ in range(n):
        r = np.random.randint(6)
        if r == 0:
            x += 1
        elif r == 1:
            x -= 1
        elif r == 2:
            y += 1
        elif r == 3:
            y -= 1
        elif r == 4:
            z += 1
        else:
            z -= 1
    return x, y, z

#fwhm
def compute_fwhm(disp):
    counter = Counter(disp)
    x = sorted(counter.keys())
    prob = np.array([counter[k] for k in x]) / len(disp)

    peak = max(prob)
    hpeak = peak / 2
    indices = np.where(prob >= hpeak)[0]
    x1 = x[min(indices)]
    x2 = x[max(indices)]
    return x2 - x1, x, prob
# if d==1:
#     for i in range(w):
#         pos.append(random_walk(n))
#     # counting for prabability
#     counter = Counter(pos)
#
#     x = sorted(counter.keys())
#     prob = np.array([counter[k] for k in x]) / w
#     plt.figure()
#     plt.plot(x, prob)
#     plt.xlabel("number of walkers")
#     plt.ylabel("probability")
#     plt.savefig("1d.png",dpi=600, bbox_inches="tight")
# if d==2:
#     di = [random_walk_2d(n) for _ in range(w)]
#     counter = Counter(di)
#     xs = np.array([k[0] for k in counter.keys()])
#     ys = np.array([k[1] for k in counter.keys()])
#     probs = np.array(list(counter.values())) / w
#     fig = plt.figure(figsize=(9, 7))
#     ax = fig.add_subplot(111, projection="3d")
#
#     sc = ax.scatter(xs, ys, probs, c=probs, cmap="viridis", s=20)
#     ax.set_xlabel("x (final position)")
#     ax.set_ylabel("y (final position)")
#     ax.set_zlabel("probability")
#     ax.set_title(f"2D random walk: joint (x,y) distribution, n={n}")
#     fig.colorbar(sc, shrink=0.6, label="probability")
fwhm_results = []
f2 = open("fwhm_2dp.txt", "w")
f3 = open("fwhm_3dp.txt", "w")

for f in ( f2, f3):
    f.write("n\tw\tfwhm\tprob\tx\n")

for i in range(10, n - 1, 30):
    for d in ( 2, 3):
        pos = []
        for _ in range(w):
            if d == 1:
                pos.append(random_walk(i))
            elif d == 2:
                x, y = random_walk_2d(i)
                pos.append(np.sqrt(x**2 + y**2))
            else:
                x, y, z = random_walk_3d(i)
                pos.append(np.sqrt(x**2 + y**2 + z**2))

        fwhm_val, x_vals, prob_vals = compute_fwhm(pos)
        fwhm_results.append((d, i, fwhm_val))

        # store x_vals and prob_vals as comma-joined strings in their own columns
        x_str = ",".join(map(str, x_vals))
        prob_str = ",".join(map(str, prob_vals))

        target = f1 if d == 1 else f2 if d == 2 else f3
        target.write(f"{i}\t{w}\t{fwhm_val}\t{prob_str}\n")

    print(f"n={i} done")

f2.close()
f3.close()
print(fwhm_results)