#!/usr/bin/env python3

import sys, subprocess
from PIL import Image, ImageFilter

if __name__=='__main__':
    try:
        Img = Image.open(sys.argv[1])
    except:
        print(f'usage: {sys.argv[0]} img_file')
        sys.exit(1)
    for f in range(200):
        #Img = Img.filter(ImageFilter.BLUR)
        Img = Img.filter(ImageFilter.SMOOTH)
        #Img.filter(ImageFilter.SMOOTH_MORE)
        #Img.save(f'/tmp/frame{f:03d}.gif')
        Img = Img.filter(ImageFilter.SHARPEN)
        Img.save(f'/tmp/frame{f:03d}.gif')
    subprocess.run('gifsicle -O3 -l -d5 --colors 256 /tmp/frame*.gif > anim.gif', shell=True)
    subprocess.run('rm -f /tmp/frame*.gif', shell=True)
