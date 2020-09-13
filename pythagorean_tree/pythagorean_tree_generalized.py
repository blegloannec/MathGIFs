#!/usr/bin/env python3

import cairo
import cmath
import os
import random
random.seed()

W = 600
H = W//2

def aux(ctx, nmax, n, a, b):
    if n>=0:
        ad = (b-a)*1j
        d = a+ad
        c = b+ad
        o = (c+d)/2
        oc = c-o
        k = random.randint(1,2)
        T = sorted(cmath.pi*random.random() for t in range(k))
        #T = [cmath.pi*(i+(random.random()-0.5)/1)/(k+1) for i in range(1,k+1)]
        E = [c]
        E.extend(o + oc*cmath.rect(1, t) for t in T)
        E.append(d)
        ctx.move_to(a.real, H-a.imag)
        ctx.line_to(b.real, H-b.imag)
        for e in E:
            ctx.line_to(e.real, H-e.imag)
        ctx.set_source_rgb(0, 1.-0.8*n/nmax, 0)
        ctx.fill_preserve()
        ctx.set_line_width(1)
        ctx.stroke()
        for i in range(1, len(E)):
            aux(ctx, nmax, n-1, E[i], E[i-1])

def tree(n=8):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    # background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    # tree
    k = 11
    a = complex((k//2)/k*W, 10)
    b = complex((k//2+1.)/k*W, 10)
    aux(ctx, n, n, a, b) 
    # output
    return surf

if __name__=='__main__':
    surf = tree()
    surf.write_to_png('general.png')
