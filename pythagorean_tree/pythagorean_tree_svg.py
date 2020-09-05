#!/usr/bin/env python3

# SVG drawing (recycled from Project Euler 395)

import math

cosa, sina = 4./5., 3./5.
#a = math.pi/4.; cosa = math.cos(a); sina = math.sin(a)

w, h = 800, 500
def tree_svg(SVG, nmax, n, xa,ya, xb,yb):
    if n>=0:
        dx, dy = xb-xa, yb-ya
        xc, yc = xa-dy, ya+dx
        xd, yd = xc + cosa*(cosa*dx-sina*dy), yc + cosa*(sina*dx+cosa*dy)
        xe, ye = xb-dy, yb+dx
        SVG.append(f'<polygon points="{xa:.3f},{h-ya:.3f} {xb:.3f},{h-yb:.3f} {xe:.3f},{h-ye:.3f} {xc:.3f},{h-yc:.3f}" style="fill:rgb(0,{50+205*(nmax-n)//nmax},0);"/>')
        tree_svg(SVG, nmax, n-1, xc,yc, xd,yd)
        tree_svg(SVG, nmax, n-1, xd,yd, xe,ye)

def svg(n=12):
    SVG = [f'<svg width="{w}" height="{h}">']
    tree_svg(SVG, n, n, w/2.,10., w/2.+w/7.,10.)
    SVG.append('</svg>')
    F = open(f'tree{n}.svg', 'w')
    F.write('\n'.join(SVG))
    F.close()

if __name__=='__main__':
    svg()
