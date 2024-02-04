import numpy as np
from . import config as c

def initial_sin(X):
    return np.sin(np.pi*X)

def inital_spike(X):
    x = np.zeros(len(X))
    x[int(len(X)/2)] = 1
    return x