default: mandel

mandel: mandelbrot_gif.cpp pgmimage.cpp
	g++ -O3 $^ -o $@

anim: mandel
	./$<
	convert -loop 0 -delay 5 /tmp/frame*.pgm anim.gif
	rm -f /tmp/frame*.pgm

clean:
	rm -f a.out *~ mandel anim.gif
