import numpy as np
import scipy.ndimage as ndimage
import viewer


class WaveSolver:
    '''
    Approximates a solution of the wave equation on a surface.
    '''
    def __init__(self):
        '''
        Setup initial conditions
        '''
        # Configuration values
        self.N = 20 # x and y values are in the range [-N, N]
        self.c2 = 0.1 # Propagation speed

        # Stencil used to approximate Laplacian
        self.stencil = np.array([[.5, 1, .5], [1, -6, 1], [.5, 1, .5]])*self.c2
        
        # Setup input values
        self.X = np.arange(-self.N, self.N, dtype=np.float)
        self.Y = np.arange(-self.N, self.N, dtype=np.float)
        # Clear output to 0
        self.Z = np.zeros((self.N*2, self.N*2), dtype=np.float)
        self.Z_prev = self.Z
        
    def update(self, frame):
        '''
        Excecutes one step of the approximation
        '''
        # Clamp edges
        self.Z[:,0] = np.zeros_like(self.Z[:,0])
        self.Z[0,:] = np.zeros_like(self.Z[0,:])
        self.Z[:,-1] = np.zeros_like(self.Z[:,-1])
        self.Z[-1,:] = np.zeros_like(self.Z[-1,:])
        
        # Provide initial input energy
        if frame < 30:
            self.Z[:,0] = np.sin(frame/10)*np.ones(self.N*2)*5
        
        # Update wave state
        Z_next = ndimage.convolve(self.Z, self.stencil, mode='constant')
        Z_next = Z_next - self.Z_prev + 2*self.Z
        self.Z_prev, self.Z = self.Z, Z_next


if __name__ == '__main__':
    wave_solver = WaveSolver()
    wave_viewer = viewer.Viewer(wave_solver, 'Wave Equation')
    wave_viewer.start()
