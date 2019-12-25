#!/usr/bin/env python3

import os
from math import *
from PIL import Image
import numpy as np

def mandel_img(xc=0., yc=0., r=2., size=200, iterations=100):
    Img = Image.new('L',(size,size),255)
    Pix = Img.load()
    for ix in range(size):
        x = 2.*r*ix/size + xc-r  # interval [xc-r,xc+r]
        for iy in range(size):
            y = 2.*r*iy/size + yc-r
            c = complex(x,y)
            z = complex(0,0)
            i = 0
            while i<iterations and abs(z)<2.:
                z = z*z + c
                i += 1
            Pix[ix,size-1-iy] = 255 - (255*i)//iterations
    return Img

def mandel_numpy_img(xc=0., yc=0., r=2., size=200, iterations=100):
    Img = Image.new('L',(size,size))
    C = []
    for iy in range(size-1,-1,-1):
        y = 2.*r*iy/size + yc-r
        for ix in range(size):
            x = 2.*r*ix/size + xc-r  # interval [xc-r,xc+r]
            c = complex(x,y)
            C.append(c)
    C = np.array(C)
    c0 = complex(0)
    Z = np.array([c0]*(size*size))
    I = np.array([0]*(size*size))
    for i in range(iterations):
        Z = Z*Z + C
        Over = np.greater(abs(Z), 2.)
        Z = np.where(Over, c0, Z)
        C = np.where(Over, c0, C)
        I = np.where(Over, 255-(255*i)//iterations, I)
    Img.putdata(I)
    return Img

def mandel_zoom(x, y, r, frames=100):
    os.system('rm -f /tmp/frame*.gif')
    lr0 = log(2.)
    lr = log(r)
    for a in range(frames+1):
        t = a/frames
        r1 = exp(lr0*(1.-t) + lr*t)
        it = round(100*(1.-log(r1,100)))
        #Img = mandel_img(x,y,r1,iterations=it)
        Img = mandel_numpy_img(x,y,r1,iterations=it)
        Img.save('/tmp/frame%03d.gif' % a)
        Img.close()
    #os.system('convert -loop 0 -delay 10 /tmp/frame*.gif anim.gif')
    os.system('gifsicle -O3 -l -d10 /tmp/frame*.gif > anim.gif')
    os.system('rm -f /tmp/frame*.gif')

if __name__=='__main__':
    x,y = 0.01605,-0.8205
    mandel_zoom(x,y,0.001)
