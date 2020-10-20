#!/usr/bin/env python3

import numpy as np
from PIL import Image
import os, random
random.seed()

EPS = 1e-6
randcol = lambda: tuple(random.randint(100,255) for _ in range(3))
random_colors = lambda n: [randcol() for _ in range(n)]


class NewtonImg:
    def __init__(self, Poly, x1=-10.,y1=-10., x2=10.,y2=10., width=801,height=801, iterations=20):
        self.P = np.array(Poly).astype('f')
        self.DP = np.polyder(self.P)
        self.Roots = np.roots(self.P)
        self.width  = width
        self.height = height
        self.itmax = iterations
        self.Z = []
        for iy in range(self.height-1,-1,-1):
            y = ((self.height-iy)*y1 + iy*y2) / self.height
            for ix in range(self.width):
                x =((self.width-ix)*x1 + ix*x2) / self.width
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
        Img = Image.new('L', (self.width, self.height))
        Img.putdata(Data)
        return Img
    
    def rgb(self, Colors=None):
        if Colors is None:
            Colors = random_colors(self.Roots.size)
        else:
            assert len(Colors)>=self.Roots.size
        Dist = np.array([np.abs(self.Z-r) for r in self.Roots])
        Data = np.argmin(Dist, axis=0)
        RGB = [np.array([Colors[c][i] for c in Data]) for i in range(3)]
        RGB = RGB * (self.itmax - self.Iter) // self.itmax
        Img = Image.new('RGB', (self.width, self.height))
        Data = list(zip(*RGB))
        Img.putdata(Data)
        return Img


# Anim.
def random_newton_anim(degree=3, frames=20, radius=20., size=201, iterations=30):
    Colors = random_colors(degree)
    P = [4.*random.random()-2. for _ in range(degree)] + [1.]
    for t in range(frames):
        for i in range(degree):
            P[i] += 0.03
        Img = NewtonImg(P, -radius,-radius, radius,radius, size,size, iterations).rgb(Colors)
        Img.save('/tmp/frame%04d.gif' % t)
    os.system('gifsicle -O3 -l -d10 /tmp/frame*.gif > anim.gif')
    os.system('rm -f /tmp/frame*.gif')


# MAIN
if __name__=='__main__':
    #P = (1, 0, 0, -1)  # X³-1
    #P = (1, 0, 0, 0, -1)
    #P = (1, 0, -2, 2)  # example with non converging areas
    #P = (1, 0, 0, 0, 15, 0, 0, 0, -16)
    #P = (1, 0 ,-300, -3000)
    P = tuple([1]+[random.randint(-5,5) for _ in range(3)])
    Colors = [(255,100,100), (100,255,100), (100,100,255)]
    #Img = NewtonImg(P, x1=-15.,y1=-20., x2=25.,y2=20., iterations=25).rgb()
    Img = NewtonImg(P).rgb(Colors)
    Img.save('out.png')
    #random_newton_anim(3)
