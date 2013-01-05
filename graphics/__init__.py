import pyglet
from pyglet.gl import *
import pyglet.graphics as gfx
from random import randint as rnd


def raster():
	xy=()
	for x in range(0,100):
		xy += (x*10, rnd(90,110))
	vertices = gfx.vertex_list(len(xy)/2,
				('v2i', xy),
				('c3B', (0, 0, 255)*(len(xy)/2)))
	return vertices


