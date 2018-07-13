
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot(data, dic, fig, position):
    # setup the figure and axes
    ypos, xpos = np.indices(data.shape)
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(xpos.shape)

    ax = fig.add_subplot(position, projection='3d')


    colors = plt.cm.jet(data.flatten() / float(data.max()))
    ax.bar3d(xpos, ypos, zpos, .5, .5, data.flatten())
    ax.set_title(dic['sv']['Group.router'])

    ax.set_xlabel(dic['x'])
    ax.set_ylabel(dic['y'])
    ax.set_zlabel(dic['z'])

