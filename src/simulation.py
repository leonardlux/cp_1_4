import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact

# custom files

from . opt_inital_distr import definition_interval_wrapper


class Simulation:
    def __init__(self,func_u_0,c):
        self.c = c
        bc = c.bc_ps # border cells per side
        self.bc = bc

        # first initalize matrix
        self.U = np.zeros( shape=( c.n_t, c.n_x + 2 * bc) )
        # initalize vectors of the correct size
        self.x = np.linspace( c.x_min, c.x_max, c.n_x )
        self.t = np.linspace( c.t_min, c.t_max, c.n_t )

        # limits the definition function to starting intervall
        self.func_u_0 = definition_interval_wrapper(c, func_u_0)
        self.analytical_exists = False

        # populate the array with the starting values 
        self.U[ 0, bc:-bc ] = self.func_u_0(self.x)

        pass
        
    def run(self):
        # as in task 3, we can use an iterative approach:
        # constants needed:
        alpha = self.c.c_c * self.c.dt / self.c.dx
        bc = self.bc # border cells per side

        for i_t in range(self.c.n_t - 1):
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
        alpha = self.c.dt / self.c.dx 
        bc = self.bc # border cells per side

        for i_t in range(self.c.n_t - 1):
            # beautify and less effort:
            U_p = self.U[ i_t, bc + 1: - bc + 1 ]
            U_m = self.U[ i_t, bc - 1: - bc - 1 ]
            U_i   = self.U[ i_t, bc : - bc ]
            # calculation
            self.U[ i_t + 1 , bc:-bc ] = \
                + U_i \
                - alpha /4   * ( U_p**2 - U_m**2 ) \
                + alpha**2 / 8 * (
                    + ( U_p + U_i ) * ( U_p**2 - U_i**2 )
                    - ( U_i + U_m ) * ( U_i**2 - U_m**2 )
                )
    
    def calc_analytical(self):
        # exact solution of basic transport equation
        # set indicator to True
        self.analytical_exists = True
        # Approach:
        # u_0(x) start distribution
        # solution: u(x,t) = u_0(x-c*t)
        c = self.c
        self.U_analy = np.zeros( shape=( c.n_t, c.n_x ) )
        for i_t in range(self.c.n_t):
            x_dash = self.x - c.c_c * self.t[i_t]
            #print(f"{x_dash=}")
            self.U_analy[i_t] = self.func_u_0(x_dash)
        pass

    def plot(self,save_to=""):

        fig  =  plt.figure(figsize = (12, 5))
        ax  = fig.add_subplot(projection = '3d')
        X, T = np.meshgrid( self.x, self.t)  
        ax.plot_surface(T, X, self.U[:, self.bc:-self.bc])
        ax.set_xlabel("$t$")
        ax.set_ylabel("$x$")
        ax.set_zlabel("$u(x)$")
        if save_to!="":
            plt.savefig(save_to)
        else:
            plt.show()

        pass
    
    def plot_diff_time(self,z_lim=1.1, times = [],save_to = ""):
        fig  =  plt.figure(figsize = (12, 5))
        ax0  = fig.add_subplot(131,)
        ax1  = fig.add_subplot(132,)
        ax2  = fig.add_subplot(133,)

        axs = [ ax0, ax1, ax2 ]
        if times == []:
            times = [
                0,              # start point
                int(self.c.n_t/2),   # half way through
                self.c.n_t -1,          # end of simulation
            ]
        # adjust for offset

        # plot everything
        for ax, t_i in zip(axs,times):
            ax.set_title(f"t = {self.c.dt*(t_i)}")
            ax.plot( 
                self.x, 
                self.U[ t_i, self.bc:-self.bc],
                )
            ax.set_xlim(0.3,0.7)
            ax.set_xlabel("$x$")
            ax.set_ylabel("$u(x)$")

        if save_to =="":
            plt.show()
        else:
            plt.savefig(save_to)

    def plot_interactive(self,t_i_steps=100,diff=False):
        def plotter(t):
            t = int(t)
            plt.figure(figsize = (20, 10))
            if not diff:
                plt.plot(self.U[t,self.bc:-self.bc],label="numerical")
                if self.analytical_exists:
                    plt.plot(self.U_analy[t],label="analytical")
                    plt.legend()
            else: 
                assert self.analytical_exists
                plt.plot(self.U[t,self.bc:-self.bc] - self.U_analy[t])
                plt.ylabel("numerical - analytical")


            plt.title(f"at $t={t*self.c.dt}$")
        interact(plotter, t = (0, self.c.n_t, t_i_steps));
    
