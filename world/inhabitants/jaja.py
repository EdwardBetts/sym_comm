import os
import pyglet
import media
import world.inhabitants

path = os.sep.join(['media', 'inhabitants'])
img = media.sprite(path, 'jaja01.png')

class Jaja(world.inhabitants.Inhabitant):

	def __init__(self, x, y):
		super(Jaja, self).__init__(img, x, y)
		
		
def create(x, y):
	return Jaja(x, y)
	
