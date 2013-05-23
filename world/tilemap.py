import pyglet.graphics as gfx
from random import randint as rnd
import game
# -*- coding: utf-8 -*-

__doc__="restructuredtext"

# set up variables for local use
nrel = [(u'n', 0,-1),
	 (u'ne', 1,-1),
	  (u'e', 1, 0),
	 (u'se', 1, 1),
	  (u's', 0, 1),
	 (u'sw',-1, 1),
	  (u'w',-1, 0),
	 (u'nw',-1,-1)]



# implementation of single tile map node
class Tile(object):
	"""
	Class for single map tile
	"""

	counter=0

	def __init__(self):
		super(Tile, self).__init__()

		ID = Tile.counter
		Tile.counter += 1

		self.x = ID % topo.width
		self.y = ID // topo.width
		# topological elevation of this map tile; heightmap
		# feature
		self.elevation = 0

		# upper-left corner of this tile for to estimate
		# where it is to find on the graphical output
		self.pos=(self.x*20, self.y*20)

		# the tiles directly adjacent to this tile
		#TODO: store walking cost between nodes in here?
		self.neighbours = {}
		# coordinates of the graphical representation of this
		# tile, a four point polygon
		# TODO: implement, handle as a vertex list or whatev
		self.bounds = []

		# 0 = normal ground, 1 = water, 2 = dirt road
		self.type = 0

		# vegetation level of this tile
		# TODO: implement
		self.vegetation = 0

		# indicator for how good one can walk on this tile
		# 1: minimum, the higher the better
		# TODO: heuristic/improve this!
		self.walkability = 1

		# the resource this tile supplies
		self.resource = None



	# sets up links to neighbour nodes.
	def assign_neighbours(self):
		"""
		identifies the adjacent map tiles of this tiles and
		stores them in the self.neighbours dictionary with
		the respective relative cardinal direction as the key,
		like 'n', 'sw', 'nw' etc.
		"""
		n = self.neighbours

		for key,rx,ry in nrel:
			neighbour = topo.tile((self.x+rx) % topo.width,
							(self.y+ry)) # % topo.height)
			if neighbour:
				n[key] = neighbour


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
		map tile, taking adjacent tiles into account
		"""
		n = self.neighbours
		#mean = lambda x1,x2: (x1 + x2) // 2
		#meany= lambda n1,n2: mean(mean(n1.pos[1], n1.neighbours[u'n'].pos[1]),
								#mean(n2.pos[1], n2.neighbours[u'n'].pos[1]))

		x = self.pos[0]
		#self.bounds = [ x-10, meany(n['w'], self),
						#x+10, meany(n['e'], self),
						#x+10, meany(n['se'], n['s']),
						#x-10, meany(n['sw'], n['s']) ]
		self.bounds=[x, self.pos[1]]
		for x,dir in [(x+20,'e'), (x+20,'se'), (x,'s')]:
			if dir in n:
				self.bounds+=[x, n[dir].pos[1]]
			else:
				self.bounds+=[x,self.pos[1]+20*int('s' in dir)]


	def get_bounds(self):
		"""
		returns an array of a four-point polygon representing
		this map tile
		"""
		if not self.bounds:
			# start top-left, go clockwise
			self.assign_bounds()
		return self.bounds


	def accessability(self, tile):
		"""
		returns a value indicating how hard it is to walk from
		this tile to a (most likely) adjacent tile 
		"""
		#TODO: 
		g = [0,1,1.5][int(self.x!=tile.x)+int(self.y!=tile.y)]
		g *= 1+2/(self.walkability+tile.walkability)
		g += tile.elevation-self.elevation
		return g


	# computes the distance between this node and a given one
	# considers diagonal links
	def distance(self, tile):
		return max(abs(self.x-tile.x), abs(self.y-tile.y))





##### Tile Map implementation #####


class Map(object):
	"""
	singleton providing world implementation as a tile map
	"""


	def __init__(self, width, height):
		super(Map, self).__init__()
		print "  instantiate world map object with dimensions %dx%d" \
			% (width, height)
		self.width = width
		self.height = height

		self.tiles = {}


	def init_map(self, maxheight):
		"""
		creates links between adjacent tiles, generates heightmap
		and computes coordinates for graphical representation of
		contained tiles
		"""
		while Tile.counter < self.width*self.height:
			n = Tile()
			self.tiles[(n.x,n.y)] = n

		print "   map tiles instantiated: %d" % Tile.counter

		for pos,tile in self.tiles.items():
			tile.assign_neighbours()

		self.init_heightmap(maxheight)

		for pos,tile in self.tiles.items():
			tile.assign_bounds()


	# return tile at requested position
	def tile(self, x, y):
		"""
		returns the map tile at the given index ``(x,y)``
		"""
		return self.tiles.get((x,y), None)


	# set up heightmap
	def init_heightmap(self, maxheight):

		# initiate heightmap with random values
		for y in range(self.height):
			for x in range(self.width):
				elv = rnd(0,1)*rnd(0,1)*rnd(0,maxheight*10)/10.
				self.tile(x,y).elevation = elv


		# smooth heightmap by calculating means of each
		# tile's neighbours elevation values
		for i in range(2):
			topo = []
			for y in range(self.height):
				topo.append([])
				for x in range(self.width):
					n = self.tile(x,y)
					topo[y].append(
						sum([nn.elevation for nn in
						n.neighbours.values()+[n]])
						/ (len(n.neighbours)+1.))

			# assign smoothened heightmap values to tile instances
			for y in range(self.height):
				for x in range(self.width):
					self.tile(x, y).set_elevation(topo[y][x])


	# REPR
	def __repr__(self):
		"""
		returns a string representation of the world's heighmap
		"""
		out=[]
		for y in range(self.height):
			row = []
			for x in range(self.width):
				row.append(self.tile(x,y).elevation)
			out.append(' '.join([' .:#'[int(v>=5)+int(v>=8)+int(v>=10)] for v in row]))
			#'#' if v >= 10 else
					# '-' if v >= 5 else ' ' for v in row]))

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
		of a random map tile as a vertex_list, just for debugging
		"""
		# http://packages.python.org/pyglet/api/pyglet.image.AbstractImage-class.html#blit_into
		tile = self.tiles.values()[rnd(0,len(self)-1)]
		vertices = gfx.vertex_list(4,
			('v2i', tile.get_bounds()),
			('c3B', (0, 0, 255)*4))
		return vertices




# APi stuff
topo=None

# factory method
def create(width, height, maxelevation):
	global topo
	if not topo:
		topo=Map(width, height)
		topo.init_map(maxelevation)
	return topo


# A* path finding initiator
def find_path(orig, dest):
	x,y=orig
	orig = topo.tile(x,y)
	x,y=dest
	dest = topo.tile(x,y)
	return pathfinder.AStar(orig, dest)
