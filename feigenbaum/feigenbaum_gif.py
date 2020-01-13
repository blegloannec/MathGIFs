#!/usr/bin/env python3

from PIL import Image, ImageDraw
import os, math

ColMode = 'RGB'
ColBrdr = (50, 50, 50)
ColBack = (255,255,255)
ColDiag = ( 50,100,255)
ColGrph = (255,  0,  0)
ColVert = (255,100,100)

def feigenbaum(size=500, iterations=300):
    Img1 = Image.new(ColMode, (size,size), ColBack)
    Pix1 = Img1.load()
    height2 = size//4
    iter2 = min(size, iterations)
    Seq2 = []
    for imu in range(size):
        mu = 2.*imu/size+2.
        Img2 = Image.new(ColMode, (size,height2), ColBack)
        Pix2 = Img2.load()
        x = 0.5
        for i in range(iterations):
            if i<iter2:
                Pix2[i*size//iter2, height2-1-int(height2*x)] = ColGrph
            x = mu*x*(1.-x)
            if 2*i>iterations:
                Pix1[imu, size-1-int(x*size)] = ColDiag
        Seq2.append(Img2)
    for f in range(size):
        Img = Image.new(ColMode, (size+2,size+height2+3), ColBrdr)
        Img.paste(Img1,(1,1))
        Img.paste(Seq2[f],(1,size+2))
        ImageDraw.Draw(Img).line((f+1,1,f+1,size), fill=ColVert)
        Img.save('/tmp/frame%04d.gif' % f)
    os.system('gifsicle -O3 -l -d3 /tmp/frame*.gif > feigenbaum_anim.gif')
    os.system('rm -f /tmp/frame*.gif')

if __name__=='__main__':
    feigenbaum()
