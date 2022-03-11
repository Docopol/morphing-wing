import matplotlib.pyplot as plt
import numpy as np

# make data
x1 = np.linspace(0, 10, 100)
y1 = 4 + 2 * np.sin(2 * x1)
y2 = 4 + 2 * np.cos(2 * x1)

#grid
x = np.linspace(0, 8, 1)
y = np.linspace(0, 8, 1)

# plot
fig, ax = plt.subplots(1,2)


ax[0].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')
ax[0].plot(x1, y2, linewidth=2.0, label = 'cos',  color = 'blue' ) 
ax[0].plot (x, y, linewidth = 1.0, color = 'grey')

ax[0].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))


plt.legend(['sin','cos'])


ax[1].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')
plt.show()
