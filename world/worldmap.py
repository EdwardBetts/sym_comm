import pyglet.graphics as gfx
# -*- coding: utf-8 -*-

__doc__="restructuredtext"


class Node(object):
	"""
	Class for single map tile
	"""

	counter=0

	def __init__(self):
		super(Node, self).__init__()

		ID = Node.counter
		Node.counter += 1

		self.x = ID % worldmap.width
		self.y = ID // worldmap.width
		self.elevation = 0

		self.pos=(self.x*20, self.y*20-self.elevation)

		self.neighbours = {}
		self.bounds = []

		# 0 = normal ground, 1 = water, 2 = dirt road
		self.type = 0


	def assign_neighbours(self):

		n = self.neighbours
		nrel = [(u'n', 0,-1),
			 (u'ne', 1,-1),
			  (u'e', 1, 0),
			 (u'se', 1, 1),
			  (u's', 0, 1),
			 (u'sw',-1, 1),
			  (u'w',-1, 0),
			 (u'nw',-1,-1)]

		for key,rx,ry in nrel:
			n[key] = worldmap.node((self.x+rx) % worldmap.width,
							(self.y+ry) % worldmap.height)


	def assign_bounds(self):

		n = self.neighbours

		mean = lambda x1,x2: (x1 + x2) // 2
		meany= lambda n1,n2: mean(mean(n1.y, n1.neighbours[u'n'].y),
								mean(n2.y, n2.neighbours[u'n'].y))

		#TODO: spheric world
		self.bounds = [ self.x-10, meany(n['w'], self),
						self.x+10, meany(n['e'], self),
						self.x-10, meany(n['se'], n['s']),
						self.x+10, meany(n['sw'], n['s']) ]


	def get_bounds(self):

		if not self.bounds:
			# start top-left, go clockwise
			self.bounds = [self.pos[0]-10, ]



class WorldMap(object):
	"""
	singleton providing world implementation as a tile map
	"""


	def __init__(self, width, height):
		super(WorldMap, self).__init__()
		self.width = width
		self.height = height

		self.nodes = {}


	def init_map(self):

		while Node.counter < self.width*self.height:
			n = Node()
			self.nodes[(n.x,n.y)] = n

		for pos,node in self.nodes.items():
			node.assign_neighbours()

		for pos,node in self.nodes.items():
			node.assign_bounds()

	def node(self, x, y):
		return self.nodes.get((x,y), None)


	def node_at(self, x, y):
		i = (y % self.height) * self.width + (x % self.width)
		return self.nodes[i]


worldmap = WorldMap(30,20)
worldmap.init_map()