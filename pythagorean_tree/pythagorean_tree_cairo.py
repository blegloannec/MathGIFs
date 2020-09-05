#!/usr/bin/env python3

import cairo
import math
import os

#cosa, sina = 4./5., 3./5.

W = 600
H = W//2

def aux_hollow(cosa, sina, ctx, nmax, n, xa,ya, xb,yb):
    if n>=0:
        dx, dy = xb-xa, yb-ya
        xc, yc = xa-dy, ya+dx
        xd, yd = xc + cosa*(cosa*dx-sina*dy), yc + cosa*(sina*dx+cosa*dy)
        xe, ye = xb-dy, yb+dx
        ctx.move_to(xa, H-ya)
        ctx.line_to(xb, H-yb)
        ctx.line_to(xe, H-ye)
        ctx.line_to(xc, H-yc)
        ctx.set_source_rgb(0, 1.-0.8*n/nmax, 0)
        ctx.fill()
        aux_hollow(cosa, sina, ctx, nmax, n-1, xc,yc, xd,yd)
        aux_hollow(cosa, sina, ctx, nmax, n-1, xd,yd, xe,ye)

def aux_full(cosa, sina, ctx, nmax, n, xa,ya, xb,yb):
    if n>=0:
        dx, dy = xb-xa, yb-ya
        xc, yc = xa-dy, ya+dx
        xd, yd = xc + cosa*(cosa*dx-sina*dy), yc + cosa*(sina*dx+cosa*dy)
        xe, ye = xb-dy, yb+dx
        ctx.move_to(xa, H-ya)
        ctx.line_to(xb, H-yb)
        ctx.line_to(xe, H-ye)
        ctx.line_to(xd, H-yd)
        ctx.line_to(xc, H-yc)
        ctx.set_source_rgb(0, 1.-0.8*n/nmax, 0)
        ctx.fill_preserve()
        ctx.set_line_width(1)
        ctx.stroke()
        aux_full(cosa, sina, ctx, nmax, n-1, xc,yc, xd,yd)
        aux_full(cosa, sina, ctx, nmax, n-1, xd,yd, xe,ye)

def tree(cosa, sina, n=12, aux=aux_full):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    # background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    # tree
    k = 11
    aux(cosa, sina, ctx, n, n, (k//2)/k*W,10., (k//2+1.)/k*W,10.)
    # output
    return surf

def main():
    d = 12
    aux = aux_hollow
    n = 100
    for i in range(n):
        a = math.pi/2. * i/n
        cosa = math.cos(a)
        sina = math.sin(a)
        surf  = tree(cosa, sina, d, aux)
        fname = f'frame{i:04d}'
        surf.write_to_png(f'{fname}.png')
        os.system(f'convert {fname}.png {fname}.gif')
    os.system(f'gifsicle --colors 256 -d8 -l -O3 frame*.gif > anim{d}.gif')
    os.system('rm frame*.gif frame*.png')

if __name__=='__main__':
    main()
