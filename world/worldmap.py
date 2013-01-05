import pyglet.graphics as gfx
from random import randint as rnd
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
		# topological elevation of this map node; heightmap
		# feature
		self.elevation = 0

		# kind of a center point of this node for to estimate
		# where it is to find on the graphical output
		self.pos=(self.x*20+10, self.y*20+10-self.elevation)

		# the nodes directly adjacent to this node
		self.neighbours = {}
		# coordinates of the graphical representation of this
		# node, a four point polygon
		# TODO: implement, handle as a vertex list or whatev
		self.bounds = []

		# 0 = normal ground, 1 = water, 2 = dirt road
		self.type = 0

		# vegetation level of this node
		# TODO: implement
		self.vegetation = 0

		# indicator for how good one can walk on this node
		# TODO: heuristic
		self.walkability = 1

		# the resource this node supplies
		self.resource = None


	def assign_neighbours(self):
		"""
		identifies the adjacent map tiles of this nodes and
		stores them in the self.neighbours dictionary with
		the respective relative cardinal direction as the key,
		like 'n', 'sw', 'nw' etc.
		"""

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
		"""
		assigns the coordinates of the polygon representing this
		map tile, taking adjacent nodes into account
		"""

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
		"""
		returns an array of a four-point polygon representing
		this map tile
		"""

		if not self.bounds:
			# start top-left, go clockwise
			self.bounds = [self.pos[0]-10, ]


	def accessability(self, from_node):
		"""
		returns a value indicating how hard it is to walk from
		the adjacent node from_node to this one
		"""
		return self.walkability



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

		print "map nodes instantiated: %d" % Node.counter

		for pos,node in self.nodes.items():
			node.assign_neighbours()

		self.init_heightmap()

		for pos,node in self.nodes.items():
			node.assign_bounds()


	def node(self, x, y):
		"""
		returns the map node at the given index ``(x,y)``
		"""
		return self.nodes.get((x,y), None)


#	def node_at(self, x, y):
#		i = (y % self.height) * self.width + (x % self.width)
#		return self.nodes[i]


	def init_heightmap(self):

		# initiate heightmap with random values
		for y in range(self.height):
			for x in range(self.width):
				elv = rnd(0,1)*rnd(0,1)*rnd(0,200)/10.
				self.node(x,y).elevation = elv


		# smooth heightmap by calculating means of each
		# node's neighbours elevation values
		topo = []
		for y in range(self.height):
			topo.append([])
			for x in range(self.width):
				n = self.node(x,y)
				topo[y].append(
					sum([nn.elevation for nn in
					n.neighbours.values()+[n]])
					/ (len(n.neighbours)+1.))

		# assign smoothened heightmap values to node instances
		for y in range(self.height):
			for x in range(self.width):
				self.node(x, y).elevation = topo[y][x]


	def __repr__(self):
		"""
		returns a string representation of the world's heighmap
		"""
		out=[]
		for y in range(self.height):
			row = []
			for x in range(self.width):
				row.append(self.node(x,y).elevation)
			out.append(' '.join(['#' if v >= 10 else
					 '-' if v >= 5 else ' ' for v in row]))

		return '\n'.join(out)



worldmap = WorldMap(30,20)
worldmap.init_map()