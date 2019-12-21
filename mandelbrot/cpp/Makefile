default: anim

mandel: mandelbrot_gif.cpp pgmimage.cpp
	g++ -O3 $^ -o $@

anim: mandel
	./$<
#convert -loop 0 -delay 5 /tmp/frame*.pgm anim.gif
	$(eval frames := $(wildcard /tmp/frame*.pgm))
	make $(frames:.pgm=.gif)
	gifsicle -O3 -l -d5 /tmp/frame*.gif > anim.gif
	rm -f /tmp/frame*.pgm /tmp/frame*.gif

%.gif: %.pgm
	convert $< $@

clean:
	rm -f a.out *~ mandel anim.gif
