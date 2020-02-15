#!/usr/bin/env python3

import sys, random
from PIL import Image
from math import gcd
random.seed()

BackCol = (0,0,0)

def randcol():
    return tuple(random.randint(0,255) for _ in range(3))

def pascal(size, depth=2, mod=2):
    T = [[0]*size]
    T[0][0] = 1
    for n in range(1,size):
        L = [0]*size
        L[0] = 1
        for k in range(1,n+1):
            L[k] = sum(T[-1][k-i] if k-1>=0 else 0 for i in range(depth)) % mod
        T.append(L)
    Col = [randcol() for _ in range(mod)]
    Col[0] = BackCol
    Data = []
    for L in T:
        Data += [Col[c] for c in L]
    Img = Image.new('RGB', (size,size))
    Img.putdata(Data)
    return Img


if __name__=='__main__':
    size = 750
    depth = random.randint(2,1<<4)
    mod = random.randint(2,1<<4)
    mod //= gcd(mod,depth)
    #while mod<2:
    #    mod = random.randint(2,1<<3)
    #    mod //= gcd(mod,depth)
    print(size, depth, mod, file=sys.stderr)
    Img = pascal(size, depth, mod)
    Img.save('out.png')
    Img.close()
