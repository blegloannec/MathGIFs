#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def feigenbaum(Imu=4000, Iter=400):
    Mu = np.linspace(2., 4., Imu)
    X = np.full(Imu, 0.5)
    for i in range(Iter):
        X = Mu * X * (1.-X)
        if 2*i>Iter:
            plt.plot(Mu, X, ',')  # ',k' for black
    plt.show()

def feigenbaum2(Imu=4000, Iter=400):
    Mu = np.linspace(1., 20., Imu)
    X = np.full(Imu, 0.5)
    for i in range(Iter):
        X = Mu * X * (1.-np.tanh(X))
        if 2*i>Iter:
            plt.plot(Mu, X, ',')
    plt.show()

if __name__=='__main__':
    feigenbaum()
