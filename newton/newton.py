#!/usr/bin/env python3

import os
import numpy as np
from PIL import Image
import random
random.seed()

Col = [(255,0,0),(0,255,0),(0,0,255)]
Col += [tuple(random.randint(0,255) for _ in range(3)) for _ in range(20)]


# Handmade version
def diffP(P):
    return [i*P[i] for i in range(1,len(P))]

def evalP(P,z):
    res = complex(0,0)
    for c in reversed(P):
        res = z*res + c
    return res

def newton(P, radius=20., size=501, iterations=50):
    D = diffP(P)
    R = np.roots(P)
    Data = []
    for iy in range(size):
        y = 2*radius*iy/size-radius
        for ix in range(size):
            x = 2.*radius*ix/size-radius
            z0 = z = complex(x,y)
            i = 0
            while i<iterations and abs(evalP(P,z))>0.01:
                z -= evalP(P,z)/evalP(D,z)
                i += 1
            d = abs(evalP(P,z))
            c = min(range(len(R)), key=(lambda i: abs(z-R[i])))
            Data.append(Col[c])
    Img = Image.new('RGB',(size,size))
    Img.putdata(Data)
    return Img


# Using numpy
def np_newton(P, radius=20., size=501, iterations=50):
    DP = np.polyder(P)
    Z = []
    for iy in range(size):
        y = 2*radius*iy/size - radius
        for ix in range(size):
            x = 2.*radius*ix/size - radius
            Z.append(complex(x,y))
    Z = np.array(Z)
    for _ in range(iterations):
        Z -= np.polyval(P,Z) / np.polyval(DP,Z)
    R = np.roots(P)
    R.sort()
    Data = []
    Dmax = [0.01]*len(R)
    for z in Z:
        d,c = min((abs(z-r),c) for c,r in enumerate(R))
        Dmax[c] = max(Dmax[c],d)
        Data.append((c,d))
    Data = [tuple(int(a*(1.-d/Dmax[c])) for a in Col[c]) for c,d in Data]
    Img = Image.new('RGB',(size,size))
    Img.putdata(Data)
    return Img

def random_newton_anim(degree=3, frames=20, radius=20., size=201, iterations=30):
    P = [4.*random.random()-2. for _ in range(degree)] + [1.]
    for t in range(frames):
        for i in range(degree):
            P[i] += 0.03
        Img = np_newton(P, radius, size, iterations)
        Img.save('/tmp/frame%04d.gif' % t)
    os.system('gifsicle -O3 -l -d10 /tmp/frame*.gif > anim.gif')
    os.system('rm -f /tmp/frame*.gif')


# MAIN
if __name__=='__main__':
    Img = newton([-1,0,0,1])
    #Img = np_newton([-1,0,0,0,1])
    #Img = np_newton([-16,0,0,0,15,0,0,0,1])
    #Img = np_newton([random.randint(-2,2) for i in range(3)]+[1])
    Img.save('out.png')
    Img.close()
    #random_newton_anim(3)
