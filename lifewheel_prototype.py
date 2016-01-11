#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

labels = ['Family','Friends','Relationship','Job','Leisure','Health','Personal Development','Environment']
data = np.array([9, 5, 8, 6, 7, 7, 5, 7])

N = len(labels)
theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
radii = data
width = 2 * np.pi / N

ax = plt.subplot(111, polar=True)

bars = ax.bar(theta, radii, width=width, align='center', bottom=0.0)
ax.yaxis.set_ticks([0,1,2,3,4,5,6,7,8,9])
ax.xaxis.set_ticks(theta)
ax.xaxis.set_ticklabels(labels)


for r, bar in zip(theta, bars):
    bar.set_facecolor(plt.cm.jet(r / np.pi / 2))
    bar.set_alpha(0.8)

plt.show()
