#!/usr/bin/env python3

import numpy as np
from PIL import Image
import cmath, os, random
random.seed()


# Handmade version
def julia_img(c, size=500, iterations=50):
    Img = Image.new('L', (size,size), 255)
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


# Numpy version
def np_julia_img(c, size=500, iterations=50):
    Z = []
    for iy in range(size-1,-1,-1):
        y = 4.*iy/size-2.        
        for ix in range(size):
            x = 4.*ix/size-2.  # interval [-2,2]
            Z.append(complex(x,y))
    Z = np.array(Z)
    I = np.array([iterations]*Z.size)
    C = np.array([c]*Z.size)
    c0 = complex(0)
    for i in range(iterations):
        Z *= Z
        Z += C
        Over = np.abs(Z) > 2.
        Z = np.where(Over, c0, Z)
        C = np.where(Over, c0, C)
        I = np.where(Over, i, I)
    Img = Image.new('L', (size,size))
    Img.putdata(255 * (iterations-I) // iterations)
    return Img


# Anim.
def julia_anim(c, frames=150):
    os.system('rm /tmp/frame*.gif')
    for a in range(frames):
        ca = c * cmath.rect(1., cmath.tau*a/frames)
        Img = julia_img(ca)
        Img.save('/tmp/frame%04d.gif' % a)
    #os.system('convert -loop 0 -delay 5 /tmp/frame*.gif anim.gif')
    os.system('gifsicle -O3 -l -d5 /tmp/frame*.gif > anim.gif')
    os.system('rm /tmp/frame*.gif')


# MAIN
if __name__=='__main__':
    #c = complex(-0.4,0.6)
    c = complex(-0.7885,0)
    #c = complex(random.random(),random.random())
    print(c)
    #julia_img(c).save('out.png')
    julia_anim(c)
