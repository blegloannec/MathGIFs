#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def plot(nb_pts=10**4, iterations=15, w=0.5):
    X = np.linspace(0., 1., nb_pts)
    X1 = X.copy()
    Y = np.zeros(nb_pts)
    d = 1.
    for _ in range(iterations):
        Y += np.abs(X1-np.round(X1)) * d
        X1 *= 2.
        d *= w
        plt.plot(X, Y, lw=0.5)
    plt.show()

if __name__=='__main__':
    plot()
    #plot(w=2./3.)
