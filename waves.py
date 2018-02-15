import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.animation as animation
import matplotlib.cm as cm
import scipy.ndimage as ndimage


class Waves:
    def __init__(self):
        self.N = 20
        self.c2 = 0.1
        self.stencil = np.array([[0, self.c2, 0], [self.c2, 2-4*self.c2, self.c2], [0, self.c2, 0]])
        X = np.arange(0, self.N)
        Y = np.arange(0, self.N)
        self.X, self.Y = np.meshgrid(X, Y)
        self.tX, self.tY = np.transpose(self.X), np.transpose(self.Y)
        self.Z = np.zeros_like(self.X, dtype=np.float)
        self.Z_prev = self.Z
        
        self.fig = plt.figure()
        self.ax = p3.Axes3D(self.fig)

        self.linec = art3d.Line3DCollection(self.get_lines())
        self.ax.add_collection(self.linec)

        self.ax.set_zlim3d([-1, 1], auto=False)
        self.ax.set_xlim3d([0, self.N])
        self.ax.set_ylim3d([0, self.N])

    def get_lines(self):
        tZ = np.transpose(self.Z)
        return ([zip(xl, yl, zl) for xl, yl, zl in zip(self.X, self.Y, self.Z)]
            + [zip(xl, yl, zl) for xl, yl, zl in zip(self.tX, self.tY, tZ)])
       
    def update(self, num):
        if num < 30:
            self.Z[:,0] = np.sin(num/10)*np.ones(self.N)*.5
        
        Z_next = ndimage.convolve(self.Z, self.stencil, mode='constant') - self.Z_prev
        self.Z_prev, self.Z = self.Z, Z_next

        self.linec.set_segments(self.get_lines())
    

w = Waves()

def update(num):
    return w.update(num)

surf_ani = animation.FuncAnimation(w.fig, update, None, fargs=(),
                                   interval=0, blit=False)

plt.show()
