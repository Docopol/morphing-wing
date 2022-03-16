import matplotlib.pyplot as plt
import numpy as np

# make data
x1 = np.linspace(0, 10, 100)
y1 = 4 + 2 * np.sin(2 * x1)
y2 = 4 + 2 * np.cos(2 * x1)

# plot


# symmetry (bending analysis), FEm vs experimental, time vs asymetry (optional)
fig, ax = plt.subplots(2,2)

# symmetry analyis plot

ax[0,0].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')

ax[0,0].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

ax[0,0].set_title('Sample Title')

# FEM vs experimental data

ax[1,0].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')
ax[1,0].plot(x1, y2, linewidth=2.0, label = 'cos',  color = 'blue' ) 

ax[1,0].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

ax[1,0].legend(['sin','cos'])


#asymmetry over time (optional)
ax[1,1].plot(x1, y2, linewidth=2.0, label = 'cos', color = 'blue')


ax[1,1].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))


plt.show()
