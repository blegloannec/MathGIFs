#include <cstdio>
#include <cassert>
#include "pgmimage.hpp"

PGMImage::PGMImage(int W, int H, color c) : W(W), H(H) {
  M = new color[W*H];
  for (int y=0; y<H; ++y)
    for (int x=0; x<W; ++x) M[x+y*W] = c;
}

PGMImage::~PGMImage() {
  delete M;
}

void PGMImage::set_pixel(int x, int y, color c) {
  assert(0<=x && x<W && 0<=y && y<H);
  M[x+y*W] = c;
}

void PGMImage::save(const char *fname) const {
  FILE *F = fopen(fname, "w");
  fprintf(F, "P5\n%d %d\n255\n", W, H);
  for (int y=0; y<H; ++y)
    for (int x=0; x<W; ++x)
      fprintf(F, "%c", M[x+y*W]);
  fclose(F);
}

void PGMImage::save_ascii(const char *fname) const {
  FILE *F = fopen(fname, "w");
  fprintf(F, "P2\n%d %d\n255\n", W, H);
  for (int y=0; y<H; ++y) {
    for (int x=0; x<W; ++x)
      fprintf(F, "%d ", M[x+y*W]);
    fprintf(F, "\n");
  }
  fclose(F);
}
