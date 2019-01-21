#!/usr/bin/env python

from PIL import Image,ImageChops
import random
random.seed()

W,H = 520,380
A = 2

def gen():
    size = A*W,A*H
    img = Image.new('1',size,1)
    pix = img.load()
    for _ in xrange(W*H/4):
        x,y = random.randint(0,W-1),random.randint(0,H-1)
        for i in xrange(A*x,A*(x+1)):
            for j in xrange(A*y,A*(y+1)):
                pix[i,j] = 0
    return img

def anim(img0,seq):
    w,h = img0.size
    cropd = A*34
    cropbox = (cropd,cropd,w-cropd,h-3*cropd)
    i = 0
    for _ in xrange(9):
        img0.crop(cropbox).save('/tmp/frame%03d.gif' % i)
        i += 1
    curr = img0
    for O in seq:
        if O[0]=='r':
            amax,step = O[1],O[2]
            for a in xrange(0,amax+step,step):
                ImageChops.darker(img0,curr.rotate(a)).crop(cropbox).save('/tmp/frame%03d.gif' % i)
                i += 1
            curr = curr.rotate(amax)
        elif O[0]=='t':
            (xf,yf),(dx,dy) = O[1],O[2]
            x,y = 0,0
            while (x,y)!=(xf,yf):
                ImageChops.darker(img0,ImageChops.offset(curr,x,y)).crop(cropbox).save('/tmp/frame%03d.gif' % i)
                i += 1
                x += dx
                y += dy
            curr = ImageChops.offset(curr,xf,yf)

anim(gen(),[('r',6,1),('t',(20,-20),(1,-1)),('t',(0,40),(0,2)),('t',(-20,-20),(-1,-1)),('r',-6,-1)])
