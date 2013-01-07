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

#https://groups.google.com/forum/?fromgroups=#!topic/pyglet-users/6rzUzuY5af8
def get_pixel_from_image(image, x, y):
        #Grab 1x1-pixel image. Converting entire image to ImageData takes much longer than just
        #grabbing the single pixel with get_region() and converting just that.
        image_data = image.get_region(x,y,1,1).get_image_data()
        #Get (very small) image as a string. The magic number '4' is just len('RGBA').
        data = image_data.get_data('RGBA',4)
        #Convert Unicode strings to integers. Provided by Alex Holkner on the mailing list.
        components = map(ord, list(data))
        #components only contains one pixel. I want to return a color that I can pass to
        #pyglet.gl.glColor4f(), so I need to put it in the 0.0-1.0 range.
        return [float(c) / 255.0 for c in components]

