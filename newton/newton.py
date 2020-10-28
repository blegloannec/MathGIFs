#!/usr/bin/env python3

import numpy as np
from PIL import Image
import os, random
random.seed()

EPS = 1e-6
randcol = lambda: tuple(random.randint(100,255) for _ in range(3))
random_colors = lambda n: [randcol() for _ in range(n)]


class NewtonImg:
    def __init__(self, poly, x1=-10.,y1=-10., x2=10.,y2=10., width=801,height=801, iterations=20):
        self.P = np.array(poly).astype('f')
        self.DP = np.polyder(self.P)
        self.Roots = np.sort(np.roots(self.P))
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
        self.compute_filter()
    
    def compute(self):
        self.Iter = np.zeros(self.Z.size)
        for i in range(1,self.itmax+1):
            self.Z -= np.polyval(self.P, self.Z) / np.polyval(self.DP, self.Z)
            PZ = np.polyval(self.P, self.Z)
            Zero = np.abs(PZ) < EPS
            self.Iter = np.where(Zero, self.Iter, i)

    # faster version using filtering
    def compute_filter(self):
        Zf = self.Z.copy()
        Idx = np.arange(self.Z.size)
        self.Iter = np.full(self.Z.size, self.itmax)
        for i in range(self.itmax):
            Zf -= np.polyval(self.P, Zf) / np.polyval(self.DP, Zf)            
            PZ = np.polyval(self.P, Zf)
            Zero = np.abs(PZ) < EPS
            Keep = ~Zero
            for z,iz in zip(Zf[Zero], Idx[Zero]):
                self.Z[iz] = z
                self.Iter[iz] = i
            Zf = Zf[Keep]
            Idx = Idx[Keep]
    
    def gray(self):
        Data = 255 * (self.itmax-self.Iter) // self.itmax
        Img = Image.new('L', (self.width, self.height))
        Img.putdata(Data)
        return Img
    
    def rgb(self, colors=None):
        if colors is None:
            colors = random_colors(self.Roots.size)
        else:
            assert len(colors) >= self.Roots.size
        Dist = np.array([np.abs(self.Z-r) for r in self.Roots])
        Data = np.argmin(Dist, axis=0)
        RGB = np.array([[colors[c][i] for c in Data] for i in range(3)])
        RGB = RGB * (self.itmax - self.Iter) // self.itmax
        Img = Image.new('RGB', (self.width, self.height))
        Data = list(zip(*RGB))
        Img.putdata(Data)
        return Img


# Anim.
def newton_anim(P1, P2, frames=50, x0=0.,radius=5., size=601, iterations=30, colors=None):
    assert len(P1) == len(P2)
    assert frames >= 2
    P1 = np.array(P1).astype('f')
    P2 = np.array(P2).astype('f')
    if colors is None:
        colors = random_colors(P1.size-1)
    else:
        assert len(colors) >= P1.size-1
    for t in range(frames):
        P = ((frames-1-t)*P1 + t*P2) / (frames-1)
        Img = NewtonImg(P, x0-radius,-radius, x0+radius,radius, size,size, iterations).rgb(colors)
        Img.save('/tmp/frame%04d.gif' % t)
    os.system('gifsicle -O3 -l -d15 /tmp/frame*.gif > anim.gif')
    os.system('rm -f /tmp/frame*.gif')


# MAIN
if __name__=='__main__':
    #P = (1, 0, 0, -1)  # X³-1
    #P = (1, 0, 0, 0, -1)
    #P = (1, 0, -2, 2)  # example with non converging areas
    #P = (1, 0, 0, 0, 15, 0, 0, 0, -16)
    P = (1, 0 ,-300, -3000)
    #P = tuple([1]+[random.randint(-5,5) for _ in range(3)])
    #Colors = [(255,100,100), (100,255,100), (100,100,255)]
    Colors = [(100,170,200), (240,240,215), (192,215,192)]
    #Img = NewtonImg(P, x1=-20.,y1=-25., x2=30.,y2=25., iterations=25).rgb(Colors)
    #Img = NewtonImg(P).rgb(Colors)
    #Img.save('out.png')
    P1 = (1,-6,6,-5)
    P2 = (1,-5,6,-30)
    newton_anim(P1, P2, x0=2., colors=Colors)
