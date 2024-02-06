import numpy as np
from . import config as c

def definition_interval_wrapper(config,func):
    x_min = config.x_min
    x_max = config.x_max
    def new_func(X): 
        # Why the flying fuck do i need to copy this ? 
        X = X.copy()  
        mask_def = np.logical_and(X >= x_min, X <= x_max)
        X[mask_def] = func(X[mask_def])
        X[~mask_def] = np.zeros(len(X))[~mask_def]
        return X
    return new_func

def initial_sin(X):
    return np.sin(np.pi*X)

def initial_uniform(X):
    return np.ones(len(X))

def initial_spike(X):
    x = np.zeros(len(X))
    x[int(len(X)/2)] = 1
    return x

def initial_normal(X):
    mu = 0.5
    sigma = 0.05
    x = 0.1 * (1/(sigma*np.sqrt(2*np.pi))) * np.exp(-((X - mu)/sigma)**2 / 2)
    return x

if __name__ == "__main__":
    pass