

# Parameters of our space:
x_min   = 0
x_max   = 1
dx      = 0.001
n_x     = int( ( x_max - x_min ) / dx + 1 )
# n_x is the amount of points for x on the spere (include 0 => +1)
# or [x_min,x_max] not (x_min,x_max]

# time 
t_min   = 0
t_max   = 1
dt      = 0.001
n_t     = int (( t_max - t_min ) / dt + 1)

# speed 
c_c     = 1

bordercells_per_side = 1+1
# first border cell is to make the calculation work 
# second border cell exist to make the implementation cleaner -1 to be at the last relevant cell
# the second border cell could be added to only to the end of the array ...
# but there is no harm in adding it on both sides, makes for cleaner code

class Config:
    def __init__(self) -> None:
        self.x_max  = x_max
        self.x_min  = x_min
        self.dx     = dx
        self.n_x    = n_x

        self.t_min  = t_min
        self.t_max  = t_max
        self.dt     = dt
        self.n_t    = n_t

        self.c_c    = c_c
        self.bc_ps = bordercells_per_side
        pass

    def recalc(self):
        self.n_x = int( ( self.x_max - self.x_min ) / self.dx + 1 )
        self.n_t = int (( self.t_max - self.t_min ) / self.dt + 1)
        pass

    def test_stability(self):
        # stability equation: c Delta t / Delta x <= 1
        # for = 1 the simulation should be beautiful
        c = self.c_c
        dt = self.dt
        dx = self.dx
        print("Numerical Stability analysis:")
        print("c * dt / dx <= 1 (perfect for = 1) ")
        print(f"{c=}")
        print(f"{dx=}")
        print(f"{dt=}")
        print(f"c * dt / dx = {c*dt/dx:.2e}")

        pass