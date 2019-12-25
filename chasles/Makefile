default: chasles.gif

chasles.gif: russian_chasles.py
	python2 $<
#convert -loop 0 -delay 10 /tmp/frame*.gif chasles.gif
	gifsicle -O3 -l -d10 /tmp/frame*.gif > chasles.gif
	rm -f /tmp/frame*.gif

clean:
	rm -f /tmp/frame*.gif chasles.gif
