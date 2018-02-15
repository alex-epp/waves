from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import scipy.ndimage as ndimage


class WaveSolver:
    def __init__(self):
        self.N = 20
        self.c2 = 0.1
        self.stencil = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])*self.c2
        self.X = np.arange(-self.N, self.N, dtype=np.float)
        self.Y = np.arange(-self.N, self.N, dtype=np.float)
        self.Z = np.zeros((self.N*2, self.N*2), dtype=np.float)
        self.Z_prev = self.Z
        
       
    def update(self, frame):
        if frame < 30:
            self.Z[:,0] = np.sin(frame/10)*np.ones(self.N*2)*5
        
        Z_next = ndimage.convolve(self.Z, self.stencil, mode='constant')
        Z_next = Z_next - self.Z_prev + 2*self.Z
        self.Z_prev, self.Z = self.Z, Z_next


class WaveViewer:
    def __init__(self, wave_solver):
        # Create GL view widget
        self.app = QtGui.QApplication([])
        self.view = gl.GLViewWidget()
        self.view.show()
        self.view.setBackgroundColor(200, 200, 200)
        self.view.setWindowTitle('Wave Equation')
        self.view.setCameraPosition(distance=50)

        # Add wave
        self.wave_solver = wave_solver
        self.wave_plot = gl.GLSurfacePlotItem(
                           x=wave_solver.X,
                           y=wave_solver.Y,
                           computeNormals=False,
                           smooth=False,
                           drawEdges=True,
                           antialias=True,
                           color=(28/256, 107/256, 160/256, 1.0),)

        self.view.addItem(self.wave_plot)
        self.frame = 0
    
    def update(self):
        self.wave_solver.update(self.frame)
        self.frame += 1
        self.wave_plot.setData(z=self.wave_solver.Z)


    def start(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(30)

        QtGui.QApplication.instance().exec_()

ws = WaveSolver()
wv = WaveViewer(ws)
wv.start()
