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

		self.x = ID % _world.width
		self.y = ID // _world.width
		# topological elevation of this map node; heightmap
		# feature
		self.elevation = 0

		# kind of a center point of this node for to estimate
		# where it is to find on the graphical output
		self.pos=(self.x*20+10, self.y*20+10)

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
			n[key] = _world.node((self.x+rx) % _world.width,
							(self.y+ry) % _world.height)


	def set_elevation(self, elevation):
		"""
		sets the elevation value for this point. also, updates
		2d coordinates of reference center point
		"""
		self.elevation = elevation
		x, y = self.pos
		y += int(elevation)
		self.pos = (x,y)



	def assign_bounds(self):
		"""
		assigns the coordinates of the polygon representing this
		map tile, taking adjacent nodes into account
		"""

		n = self.neighbours

		mean = lambda x1,x2: (x1 + x2) // 2
		meany= lambda n1,n2: mean(mean(n1.pos[1], n1.neighbours[u'n'].pos[1]),
								mean(n2.pos[1], n2.neighbours[u'n'].pos[1]))

		#TODO: spheric world
		x = self.pos[0]
		self.bounds = [ x-10, meany(n['w'], self),
						x+10, meany(n['e'], self),
						x+10, meany(n['se'], n['s']),
						x-10, meany(n['sw'], n['s']) ]


	def get_bounds(self):
		"""
		returns an array of a four-point polygon representing
		this map tile
		"""
		if not self.bounds:
			# start top-left, go clockwise
			self.assign_bounds()
		return self.bounds


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
		print "  instantiate world map object with dimensions %dx%d" \
			% (width, height)
		self.width = width
		self.height = height

		self.nodes = {}


	def init_map(self, maxheight):

		while Node.counter < self.width*self.height:
			n = Node()
			self.nodes[(n.x,n.y)] = n

		print "   map nodes instantiated: %d" % Node.counter

		for pos,node in self.nodes.items():
			node.assign_neighbours()

		self.init_heightmap(maxheight)

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


	def init_heightmap(self, maxheight):

		# initiate heightmap with random values
		for y in range(self.height):
			for x in range(self.width):
				elv = rnd(0,1)*rnd(0,1)*rnd(0,maxheight*10)/10.
				self.node(x,y).elevation = elv


		# smooth heightmap by calculating means of each
		# node's neighbours elevation values
		for i in range(2):
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
					self.node(x, y).set_elevation(topo[y][x])


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


	def __len__(self):
		"""
		returns the size of this map, which is its width times
		its height
		"""
		return self.width*self.height


	def image(self):
		"""
		dummy method that returns the graphical representation
		of a random map node as a vertex_list, just for debugging
		"""
		# http://packages.python.org/pyglet/api/pyglet.image.AbstractImage-class.html#blit_into
		node = self.nodes.values()[rnd(0,len(self)-1)]
		vertices = gfx.vertex_list(4,
			('v2i', node.get_bounds()),
			('c3B', (0, 0, 255)*4))
		return vertices



def get():
	"""
	returns the only existent instance of this class
	"""
	global _world
	return _world


def create(width, height, maxelevation):
	"""
	initializes the world map singleton with the given parameters
	"""
	global _world
	print " get world map instance"
	_world = WorldMap(width, height)
	print " initialize world map with max elevation %d" % maxelevation
	_world.init_map(maxelevation)
	print " world map creation done: %d" % len(_world)

_world = None