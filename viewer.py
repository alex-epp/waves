from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl


class Viewer:
    '''
    Animates a wireframe plot of a surface. Expects to recieve data through
    a 'solver', i.e. a class with:
        X, Y          -- 1D arrays representing x and y ranges.
        Z             -- 2D array representing z values for each x and y.
        update(frame) -- function that updates z values based on the current
                         frame number.
    
    Usage:
    >>> import numpy as np
    >>> class ExampleSolver:
    ...     def __init__(self):
    ...         self.X = np.arange(-10, 10)
    ...         self.Y = np.arange(-10, 10)
    ...         self.update(0)
    ...
    ...     def update(self, frame):
    ...         x, y = np.meshgrid(self.X, self.Y)
    ...         self.Z = 0.1*np.sin(frame/30*np.pi) * (x**2 - y**2)
    ...
    >>> Viewer(ExampleSolver()).start()
    '''
    def __init__(self, solver, title='Function Viewer'):
        '''
        Initializes the viewer (sets up Qt, creates pyqtgraph plot).
        Does not actually open the viewer window until start() is called.

        Arguments:
            solver -- solver to extract data from
            title  -- title of the graph window
        '''
        # Create GL view widget
        self.app = QtGui.QApplication([])
        self.view = gl.GLViewWidget()
        self.view.show()
        self.view.setBackgroundColor(200, 200, 200)
        self.view.setWindowTitle(title)
        self.view.setCameraPosition(distance=max(*solver.Z.shape))

        # Add function plot
        self.solver = solver
        self.plot = gl.GLSurfacePlotItem(
                           x=solver.X,
                           y=solver.Y,
                           z=solver.Z,
                           computeNormals=False,
                           smooth=False,
                           drawEdges=True,
                           drawFaces=False,
                           antialias=True,)

        self.view.addItem(self.plot)

        # Keep track of current frame
        self.frame = 0

    def start(self):
        '''
        Opens the viewer window and begins callbacks. Note start() takes control of
        the current thread and does not exit until the user closes the viewer window.
        '''
        # Call update() at 30 FPS
        timer = QtCore.QTimer()
        timer.timeout.connect(self._update)
        timer.start(30)

        # Start Qt application
        QtGui.QApplication.instance().exec_()

    def _update(self):
        '''
        Private update function, called by Qt. Calls solver.update(), and updates
        display with the results.
        '''
        # Calculate next Z values
        self.solver.update(self.frame)
        self.frame += 1
        
        # Update plot with Z values
        self.plot.setData(z=self.solver.Z)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
