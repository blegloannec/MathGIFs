#include <cstdio>
#include <complex>
#include <cmath>
#include "pgmimage.hpp"
using namespace std;

typedef double flt;
typedef complex<flt> cpx;

PGMImage mandel_img(flt xc=0., flt yc=0., flt r=2., int S=400, int Itr=100) {
  PGMImage Img(S,S);
  for (int i=0; i<S; ++i) {
    flt x = 2.*r*((flt)i)/((flt)S) + xc-r;
    for (int j=0; j<S; ++j) {
      flt y = 2.*r*((flt)j)/((flt)S) + yc-r;
      cpx z(0.,0.), c(x,y);
      int k = 0;
      while (k<Itr && abs(z)<=2.) {
	z = z*z + c;
	++k;
      }
      Img.set_pixel(i,S-1-j,255-255*k/Itr);
    }
  }
  return Img;
}

void mandel_zoom(flt x, flt y, flt r, int size=400, int frames=200) {
  flt lr0 = log(2.), lr = log(r);
  for (int a=0; a<=frames; ++a) {
    flt t = ((flt)a)/((flt)frames);
    flt r1 = exp(lr0*(1.-t) + lr*t);
    int it = round(100.*(1.-log(r1)/log(100)));
    PGMImage Img = mandel_img(x,y,r1,size,it);
    char fname[100];
    sprintf(fname,"/tmp/frame%03d.pgm",a);
    Img.save(fname);
  }
}

int main() {
  flt x = 0.01605, y= -0.8205;
  mandel_zoom(x,y,0.001);
  return 0;
}
