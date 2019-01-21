![Chasles relation](chasles.gif)

Consider two identical layers of random points and gently move one above the other. See the circles?

The composition of a rotation and a translation is a rotation.

See also [Теорема Шаля](http://images.math.cnrs.fr/Teorema-SHalya).

Compiling (using ImageMagick):
```
$ python2 russian_chasles.py
$ convert -loop 0 -delay 10 /tmp/frame*.gif chasles.gif
$ rm -f /tmp/frame*.gif
```
