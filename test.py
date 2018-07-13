import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

data = np.array([ [0, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0],
         [0, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0],
         [1, 0, 2, 2, 1, 2, 0, 0, 2, 0, 2],
         [1, 0, 2, 2, 0, 2, 0, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2],
         [0, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2],
         [1, 2, 0, 0, 2, 1, 2, 2, 0, 0, 2],
         [0, 0, 2, 1, 0, 0, 2, 0, 0, 0, 0],
         [2, 1, 2, 2, 0, 0, 0, 2, 0, 0, 2],
         [2, 2, 2, 0, 2, 0, 0, 0, 2, 2, 2],
         [2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0],
         [2, 2, 1, 2, 0, 0, 0, 2, 2, 2, 0],
         [2, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2],
         [2, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2]])


ypos, xpos  = np.indices(data.shape)

xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros(xpos.shape)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = plt.cm.jet(data.flatten()/float(data.max()))
ax.bar3d(xpos,ypos,zpos, .5,.5,data.flatten(), color=colors)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()