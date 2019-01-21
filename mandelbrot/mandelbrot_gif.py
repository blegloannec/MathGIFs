#!/usr/bin/env python3

import os
from math import *
from PIL import Image

def mandel_img(xc=0., yc=0., r=2., size=400, iterations=100):
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

def mandel_zoom(x, y, r, frames=200):
    os.system('rm -f /tmp/frame*.gif')
    x0 = y0 = 0.
    r0 = 2.
    lr0 = log(2.)
    lr = log(r)
    for a in range(frames+1):
        t = a/frames
        r1 = exp(lr0*(1.-t) + lr*t)
        it = round(100*(1.-log(r1,100)))
        Img = mandel_img(x,y,r1,iterations=it)
        Img.save('/tmp/frame%03d.gif' % a)
        Img.close()
    os.system('convert -loop 0 -delay 10 /tmp/frame*.gif mandel_anim.gif')
    os.system('rm -f /tmp/frame*.gif')

if __name__=='__main__':
    x,y = 0.01605,-0.8205
    mandel_zoom(x,y,0.001)
