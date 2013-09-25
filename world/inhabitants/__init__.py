import math
from random import randint as rnd
from pyglet.graphics import Batch
from pyglet.sprite import Sprite

import world

#import jaja

# -*- coding: utf-8 -*-

__doc__="restructuredtext"
#n__all__=["jaja"]

batch = Batch()
registry = []

# tilemap
topo = world.surface
find_path = world.find_path

class Inhabitant(object):
	def __init__(self, img, x, y):
		super(Inhabitant, self).__init__()
		register(self)
		self.x, self.y = (x,y)
		self.pathfinder=None
		self.path = [] # extra copy for custom tumbling or alternative path factories
		self.speed=.05
		self.image = img
		self.sprite = Sprite(img, batch=batch)
		self.update()
	
	def update(self):
		grpos = topo.ground_position(self.x, self.y)
		if grpos:
			x,y=grpos
			self.sprite.set_position(x-10,y)

	def move(self):
		dx = self.path[0].x-self.x
		dy = self.path[0].y-self.y
		if dx**2+dy**2 < .01:
			self.path.pop(0)
			if len(self.path)<1:
				self.pathfinder=None
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

# update all living beings currently registered at once
def update():
	for being in registry:
		if being.path and len(being.path)>0:
			being.move()
		elif being.pathfinder:
			#if not being.pathfinder.isRunning():
			being.path = being.pathfinder.result() #TODO: deep copy?
			if being.path:
				being.path = [n for n in being.path] #TODO: really neccessary?
		else:
			if rnd(0,100)<50:
				tile = topo.tile(int(round(being.x)), int(round(being.y)))
				dest = topo.tile(rnd(0,topo.width-1), rnd(0,topo.height-1))
				if tile.distance(dest) < 8:
					being.pathfinder = find_path(tile, dest)
				#for i in range(10):
					#tile=tile.neighbours.values()[rnd(0,len(tile.neighbours)-1)]
					#being.path += [tile]

def draw():
	for being in registry:
		if being.pathfinder:
			being.pathfinder.draw()
	batch.draw()
	
