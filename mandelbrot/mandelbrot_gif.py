#!/usr/bin/env python3

from PIL import Image
import numpy as np
import math, os, random
random.seed()


class MandelImg:
    def __init__(self, xc=0., yc=0., r=2., size=500, iterations=150):
        self.size = size
        self.itmax = iterations
        C = []
        for iy in range(size-1,-1,-1):
            y = 2.*r*iy/size + yc-r
            for ix in range(size):
                x = 2.*r*ix/size + xc-r  # interval [xc-r,xc+r]
                C.append(complex(x,y))
        C = np.array(C)
        c0 = complex(0)
        Z = np.array([c0]*C.size)
        self.Iter = np.array([self.itmax]*C.size)
        for i in range(self.itmax):
            Z *= Z
            Z += C
            Over = np.abs(Z) > 2.
            Z = np.where(Over, c0, Z)
            C = np.where(Over, c0, C)
            self.Iter = np.where(Over, i, self.Iter)
    
    def gray(self):
        Data = 255*(self.itmax-self.Iter) // self.itmax
        Img = Image.new('L', (self.size,self.size))
        Img.putdata(Data)
        return Img
    
    def rgb(self, nbcol=5):
        randcol = lambda: tuple(random.randint(0,255) for _ in range(3))
        MainCol = [randcol() for _ in range(nbcol+1)]
        stripe = (self.itmax+nbcol-1) // nbcol
        FullCol = []
        for i in range(self.itmax+1):
            q,r = divmod(i, stripe)
            col = tuple(((stripe-r)*a+r*b)//stripe for a,b in zip(MainCol[q-1],MainCol[q]))
            FullCol.append(col)
        Img = Image.new('RGB', (self.size,self.size))
        Img.putdata([FullCol[i] for i in self.Iter])
        return Img


# Anim.
def mandel_zoom(x, y, r, frames=100):
    os.system('rm -f /tmp/frame*.gif')
    lr0 = math.log(2.)
    lr = math.log(r)
    for a in range(frames+1):
        t = a/frames
        r1 = math.exp(lr0*(1.-t) + lr*t)
        it = round(100*(1.-math.log(r1,100)))
        Img = MandelImg(x,y,r1,iterations=it).gray()
        Img.save('/tmp/frame%03d.gif' % a)
        Img.close()
    #os.system('convert -loop 0 -delay 10 /tmp/frame*.gif anim.gif')
    os.system('gifsicle -O3 -l -d10 /tmp/frame*.gif > anim.gif')
    os.system('rm -f /tmp/frame*.gif')


if __name__=='__main__':
    x,y = 0.01605,-0.8205
    MandelImg(x,y,0.05).rgb().save('out.png')
    #mandel_zoom(x,y,0.001)
