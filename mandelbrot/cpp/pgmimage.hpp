class PGMImage {
public:
  typedef unsigned char color;
  int W,H;
  color *M;

  PGMImage(int, int, color=0);
  ~PGMImage();
  
  void set_pixel(int, int, color);
  void save(const char*) const;
  void save_ascii(const char*) const;
};
