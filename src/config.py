# Parameters
config = {}

# Task: 4.2 
# Parameters of our space:
x_min   = 0
x_max   = 1
dx      = 0.005
n_x     = int( ( x_max - x_min ) / dx + 1 )
# n_x is the amount of points for x on the spere (include 0 => +1)
# or [x_min,x_max] not (x_min,x_max]

# time 
t_min   = 0
t_max   = 4
dt      = 0.002
n_t     = int (( t_max - t_min ) / dt + 1)

# speed 
c_c     = 0.01

bordercells_per_side = 1+1
# first border cell is to make the calculation work 
# second border cell exist to make the implementation cleaner -1 to be at the last relevant cell
# the second border cell could be added to only to the end of the array ...
# but there is no harm in adding it on both sides, makes for cleaner code

config["4.2"] = {
        # x-values
        "x_min":    x_min,
        "x_max":    x_max, 
        "dx":       dx,
        "n_x":      n_x,
        # t-values
        "t_min":    t_min,
        "t_max":    t_max, 
        "dt":       dt,
        "n_t":      n_t,
        # other parameters
        "c":        c_c,
        "bc_ps":    bordercells_per_side,
    }