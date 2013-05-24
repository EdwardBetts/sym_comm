from pyglet.graphics import Batch
from pyglet.sprite import Sprite
import world
import math
import random

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
		self.path = []
		self.speed=.05
		self.image = img
		self.sprite = Sprite(img, batch=batch)
		
		self.update()
		
	def update(self):
		grpos = world.get().ground_position(self.x, self.y)
		if grpos:
			x,y=grpos
			self.sprite.set_position(x-10,y+20)

	def move(self):
		dx = self.path[0].x-self.x
		dy = self.path[0].y-self.y
		if dx**2+dy**2 < .01:
			self.path.pop(0)
		else:
			r = math.sqrt(dx**2+dy**2)
			dx *= self.speed/r
			dy *= self.speed/r
			self.x+=dx
			self.y+=dy
			self.update()

def register(being):
	global registry
	registry+=[being]

def update():
	for being in registry:
		if len(being.path)>0:
			being.move()
		else:
			tile = world.get().tile(int(being.x), int(being.y))
			for i in range(10):
				tile=tile.neighbours.values()[random.randint(0,len(tile.neighbours)-1)]
				being.path += [tile]

def draw():
	batch.draw()
	

#world = world.get()
