#!/usr/bin/env python3

import numpy as np
from PIL import Image
import os, random
random.seed()

EPS = 1e-6
randcol = lambda: tuple(random.randint(0,255) for _ in range(3))


class NewtonImg:
    def __init__(self, Poly, radius=30., size=801, iterations=20):
        self.P = np.array(Poly).astype('f')
        self.DP = np.polyder(self.P)
        self.Roots = np.roots(self.P)
        self.size = size
        self.itmax = iterations
        self.Z = []
        for iy in range(size):
            y = 2*radius*iy/size - radius
            for ix in range(size):
                x = 2.*radius*ix/size - radius
                self.Z.append(complex(x,y))
        self.Z = np.array(self.Z)
        self.Iter = np.array([0]*self.Z.size)
        for i in range(iterations+1):
            self.Z -= np.polyval(self.P, self.Z) / np.polyval(self.DP, self.Z)
            PZ = np.polyval(self.P, self.Z)
            Zero = np.abs(PZ) < EPS
            self.Iter = np.where(Zero, self.Iter, i)

    def gray(self):
        Data = 255 * (self.itmax-self.Iter) // self.itmax
        Img = Image.new('L', (self.size, self.size))
        Img.putdata(Data)
        return Img
    
    def rgb(self, Colors=None):
        if Colors is None:
            Colors = [randcol() for _ in range(self.Roots.size)]
        else:
            assert len(Colors)>=self.Roots.size
        Dist = np.array([np.abs(self.Z-r) for r in self.Roots])
        Data = np.argmin(Dist, axis=0)
        RGB = [np.array([Colors[c][i] for c in Data]) for i in range(3)]
        RGB = RGB * (self.itmax - self.Iter) // self.itmax
        Img = Image.new('RGB', (self.size, self.size))
        Data = list(zip(*RGB))
        Img.putdata(Data)
        return Img


# Anim.
def random_newton_anim(degree=3, frames=20, radius=20., size=201, iterations=30):
    P = [4.*random.random()-2. for _ in range(degree)] + [1.]
    for t in range(frames):
        for i in range(degree):
            P[i] += 0.03
        Img = NewtonImg(P, radius, size, iterations).rgb()
        Img.save('/tmp/frame%04d.gif' % t)
    os.system('gifsicle -O3 -l -d10 /tmp/frame*.gif > anim.gif')
    os.system('rm -f /tmp/frame*.gif')


# MAIN
if __name__=='__main__':
    #P = (1, 0, 0, -1)
    #P = (1,0,0,0,-1)
    #P = (1,0,0,0,15,0,0,0,-16)
    P = (1, 0 ,-300, -3000)
    Colors = [(255,0,0), (0,255,0), (0,0,255)]
    Img = NewtonImg(P).rgb(Colors)
    Img.save('out.png')
    #Img = np_newton(tuple([1]+[random.randint(-2,2) for i in range(3)]))
    #random_newton_anim(3)
