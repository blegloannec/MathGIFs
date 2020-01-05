#!/usr/bin/env python3

from PIL import Image
import math

def feigenbaum(size=900, iterations=500):
    Img = Image.new('1',(size,size),1)
    Pix = Img.load()
    for imu in range(size):
        mu = 2.*imu/size+2.
        x = 0.5
        for i in range(iterations):
            x = mu*x*(1.-x)
            if 2*i>iterations:
                Pix[imu,size-1-round(x*size)] = 0
    return Img

def feigenbaum2(size=900, iterations=500):
    Img = Image.new('1',(size,size),1)
    Pix = Img.load()
    for imu in range(size):
        mu = 20.*imu/size+1.
        x = 0.5
        for i in range(iterations):
            x = mu*x*(1.-math.tanh(x))
            if 2*i>iterations:
                Pix[imu,size-1-round(x*size/6.)] = 0
    return Img

if __name__=='__main__':
    Img = feigenbaum()
    #Img = feigenbaum2()
    Img.save('out.png')
    Img.close()
