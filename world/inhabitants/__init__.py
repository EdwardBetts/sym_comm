from pyglet.graphics import Batch
from pyglet.sprite import Sprite
import world

#import jaja

# -*- coding: utf-8 -*-

__doc__="restructuredtext"
#n__all__=["jaja"]

batch = Batch()
registry = []

class Inhabitant(object):

	def __init__(self, img, x, y):
		super(Inhabitant, self).__init__()
		register(self)
		self.x, self.y = (x,y)
		self.path = None
		self.speed=.05
		self.image = img
		self.sprite = Sprite(img, batch=batch)
		
		self.update()
		
	def update(self):
		grpos = world.get().ground_position(self.x, self.y)
		if grpos:
			x,y=grpos
			self.sprite.set_position(x,y)

def register(being):
	global registry
	registry+=[being]

def draw():
	batch.draw()
	

#world = world.get()
