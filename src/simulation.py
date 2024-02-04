import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact

# custom files
from . import config 

c = config.config["4.2"]

class Simulation:
    def __init__(self,func_u_0):
        #TODO config wird übergeben
        bc = c["bc_ps"] # border cells per side
        self.bc = bc

        # first initalize matrix
        self.U = np.zeros( shape=( c["n_t"], c["n_x"] + 2 * bc) )
        # initalize vectors of the correct size
        self.x = np.linspace( c["x_min"], c["x_max"], c["n_x"] )
        self.t = np.linspace( c["t_min"], c["t_max"], c["n_t"] )

        # populate the array with the starting values 
        self.U[ 0, bc:-bc ] = func_u_0(self.x)

        pass
        
    def run(self):
        # as in task 3, we can use an iterative approach:
        # constants needed:
        alpha = c["c"] * c["dt"] / c["dx"]
        bc = self.bc # border cells per side

        for i_t in range(c["n_t"] - 1):
            self.U[ i_t + 1 , bc:-bc ] = \
                + self.U[ i_t , bc:-bc ] \
                - 0.5 * alpha * (
                    + self.U[ i_t, bc + 1: - bc + 1 ]
                    - self.U[ i_t, bc - 1: - bc - 1 ]
                ) + 0.5 * alpha ** 2 * (
                    +     self.U[ i_t, bc + 1: - bc + 1 ]
                    - 2 * self.U[ i_t, bc : - bc ]
                    +     self.U[ i_t, bc - 1: - bc - 1 ]
                ) 

    def run_hopf(self):
        # as in task 3, we can use an iterative approach:
        # constants needed:
        alpha = c["dt"] / ( 4 * c["dx"] )
        bc = self.bc # border cells per side

        for i_t in range(c["n_t"] - 1):
            # beautify and less effort:
            U_p = self.U[ i_t, bc + 1: - bc + 1 ]
            U_m = self.U[ i_t, bc - 1: - bc - 1 ]
            U_i   = self.U[ i_t, bc : - bc ]
            # calculation
            self.U[ i_t + 1 , bc:-bc ] = \
                + U_i \
                - alpha    * ( U_p**2 - U_m**2 ) \
                + alpha**2 * (
                    + ( U_p + U_i ) * ( U_p**2 - U_i**2 )
                    - ( U_i + U_m ) * ( U_i**2 - U_m**2 )
                )
                


    def plot(self,):

        fig  =  plt.figure(figsize = (12, 5))
        ax  = fig.add_subplot(projection = '3d')
        X, T = np.meshgrid( self.x, self.t)  
        ax.plot_surface(T, X, self.U[:, self.bc:-self.bc])


        pass
    
    def plot_interactive(self,t_i_steps=100):
        def plotter(t):
            t = int(t)
            plt.figure(figsize = (20, 10))
            plt.plot(self.U[t,self.bc:-self.bc])

            plt.title(f"at $t={t*c['dt']}$")
        interact(plotter, t = (0, c["n_t"], t_i_steps));
