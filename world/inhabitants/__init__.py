from world import worldmap as world
# -*- coding: utf-8 -*-

__doc__="restructuredtext"

class Inhabitant(object):

	def __init__(self, x, y):
		super(Inhabitant, self).__init__()

		self.pos = (x,y)
		