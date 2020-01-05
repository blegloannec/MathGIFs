#!/usr/bin/env python3

import matplotlib.pyplot as plt

def plot(xdata, ydata):
    #plt.axis([0,100000,0,1.5])
    plt.figure(dpi=40)
    fig = plt.gcf()
    DPI = fig.get_dpi()
    fig.set_size_inches(1000./float(DPI),1000./float(DPI))
    plt.scatter(xdata, ydata, marker='.', s=0.02)
    #plt.scatter(xdata, ydata, marker=',') #, s=1)
    plt.show()

def main():
    X = []
    Y = []
    Imu = 4000
    for imu in range(Imu+1):
        mu = 2.*imu/Imu + 2.
        x = 0.5
        for i in range(400):
            x = mu*x*(1.-x)
            if i>200:
                X.append(mu)
                Y.append(x)
    plot(X,Y)

main()
