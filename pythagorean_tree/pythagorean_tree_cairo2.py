#!/usr/bin/env python3

import cairo
import math
import os

W = 600
H = W//2

def aux(ctx, nmax, n):
    if n>=0:
        xd, yd = cosa*cosa, 1.+cosa*sina
        ctx.move_to(0., 0.)
        ctx.line_to(1., 0.)
        ctx.line_to(1., 1.)
        ctx.line_to(xd, yd)
        ctx.line_to(0., 1.)
        ctx.close_path()
        ctx.set_source_rgb(0.4, 1.-0.8*n/nmax, 0.1)
        ctx.fill()
        ctx.save()
        ctx.translate(0., 1.)
        ctx.rotate(a)
        ctx.scale(cosa, cosa)
        aux(ctx, nmax, n-1)
        ctx.restore()
        ctx.save()
        ctx.translate(xd, yd)
        ctx.rotate(a-math.pi/2.)
        ctx.scale(sina, sina)
        aux(ctx, nmax, n-1)
        ctx.restore()


def tree(n=12):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    # background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    # tree
    k = 11
    ctx.translate((k//2)/k*W, H-10.)
    ctx.scale(W/10., -W/10.)
    aux(ctx, n, n)
    # output
    return surf


if __name__=='__main__':
    cosa, sina = 4./5., 3./5.
    a = math.atan2(sina, cosa)
    #a = math.pi/6.
    #cosa = math.cos(a); sina = math.sin(a)
    surf = tree(15)
    surf.write_to_png('tree.png')
