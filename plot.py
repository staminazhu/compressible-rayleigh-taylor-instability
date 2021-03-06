# Copyright (C) 2017 Christian T. Jacobs

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy
import h5py
from matplotlib.pylab import *
import matplotlib.animation as animation
import matplotlib
plt.style.use('dark_background')
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
Writer = animation.writers['avconv']
writer = Writer(fps=8, metadata=dict(title="Compressible Rayleigh-Taylor instability", artist="Christian T. Jacobs"), bitrate=1800)

Nh = 1
Nx = 1022
Ny = 1022
Nxh = Nx+2*Nh
Nyh = Ny+2*Nh

Lx = 1.0
Ly = 3.0

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111,aspect='equal')

cbar = None
def update(i):
    global cbar
    j = int(i)*250
    f = h5py.File("fields_%d.h5" % j, 'r')
    group = f['fields']

    x = linspace(0, Lx, Nxh)

    u = group["r"].value
    u = u.reshape((Nyh, Nxh))
    print i, j, u.min(), u.max()
    
    ax.cla()
    cmap = plt.cm.get_cmap("jet")
    c = ax.imshow(u[0:Nyh, 0:Nxh], extent = [0, Lx, 0, Ly], origin="lower", interpolation="none", cmap=cmap)
    if not cbar:
        cbar = plt.colorbar(c, aspect=50, pad=0.12, orientation='vertical')
        cbar.set_label(r'$\rho$', fontsize=14)
        cbar.set_ticks([0, 0.5, 1.0, 1.5, 2.0, 2.5])
    
    ax.set_xlabel(r"$x$", fontsize=14, labelpad=-0.5)
    ax.set_ylabel(r"$y$", fontsize=14, labelpad=-1.0)
    ax.set_title("Compressible Rayleigh-Taylor instability\nChristian T. Jacobs, 2017\n", fontsize=9)
    
    return ax

ani = animation.FuncAnimation(fig, update, frames=range(125,650), interval=100, repeat=False)
ani.save('compressible-rayleigh-taylor-instability.mp4', writer=writer)
