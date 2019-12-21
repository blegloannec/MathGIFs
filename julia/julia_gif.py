#!/usr/bin/env python3

import os
from math import sin,cos,pi
from PIL import Image
import random
random.seed()

def julia_img(c, size=500, iterations=50):
    Img = Image.new('L',(size,size),255)
    Pix = Img.load()
    for ix in range(size):
        x = 4.*ix/size-2.  # interval [-2,2]
        for iy in range(size):
            y = 4.*iy/size-2.
            z = complex(x,y)
            i = 0
            while i<iterations and abs(z)<2.:
                z = z*z + c
                i += 1
            Pix[ix,iy] = 255 - (255*i)//iterations
    return Img

def julia_anim(c, frames=150):
    os.system('rm /tmp/frame*.gif')
    for a in range(frames):
        ca = c * complex(cos(2*pi*a/frames),sin(2*pi*a/frames))
        Img = julia_img(ca)
        Img.save('/tmp/frame%04d.gif' % a)
        Img.close()
    #os.system('convert -loop 0 -delay 5 /tmp/frame*.gif julia_anim.gif')
    os.system('gifsicle -O3 -l -d5 /tmp/frame*.gif > julia_anim.gif')
    os.system('rm /tmp/frame*.gif')

if __name__=='__main__':
    #c = complex(-0.4,0.6)
    c = complex(-0.7885,0)
    #c = complex(random.random(),random.random())
    print(c)
    julia_anim(c)
