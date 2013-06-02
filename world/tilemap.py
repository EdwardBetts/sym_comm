import pyglet.graphics as gfx
from pyglet.gl import *
from random import randint as rnd
from random import random as rndf
import game
import media
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

ground_texture = media.world_txt('ground.png')
glBindTexture(GL_TEXTURE_2D, ground_texture.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
print ground_texture.width, ground_texture.height
#glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 32, 32, 
#	0, GL_RGBA, GL_UNSIGNED_BYTE, ground_texture.get_image_data())

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
		self.ID = ID
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
		self.bounds = None

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
		x = self.x*20
		y = (topo.height-self.y)*20
		y += int(elevation)
		self.pos = (x,y)


	# creates an array of bounding coordinates for this
	# tile's polygonal representation
	# [tile itself, east neighbour, southeast, south]
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
		for nx,dir in [(x+20,'e'), (x+20,'se'), (x,'s')]:
			if dir in n:
				self.bounds+=[nx, n[dir].pos[1]]
			else:
				self.bounds+=[nx, self.pos[1]+20*int('s' in dir)]


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
		self.batch=None


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
		# create elevation seed points
		clusters=[]
		for i in range(min(self.width*self.height/100,200)):
			clusters+=[(rnd(0,self.width-1), rnd(0,self.height-1),
				rndf()**2*maxheight)]
		print 'generate heightmap'
		# assign elevation init values with clustering algorithm
		for y in range(self.height):
			print '\r','.'*(30*y/self.height),
			for x in range(self.width):
				t = self.tile(x,y)
				clsts = [((c[0]-x)**2+(c[1]-y)**2, c[2]) for c in clusters]
				nearest=sorted(clsts, key=lambda c:c[0])[0]
				if nearest[1] > maxheight/2:
					t.elevation=nearest[1]+rndf()**2*10
				else:
					t.elevation=0
		# smooth heightmap by calculating means of each
		# tile's neighbours elevation values
		iterations=2
		for i in range(iterations):
			topo = []
			for y in range(self.height):
				print '\r', '#'*(30*(y+i*self.height)/self.height/iterations),
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


	# takes a point identified by a pair of float values
	# computes screen coordinates of that point
	def ground_position(self, x, y):
		# retrieve surrounded nodes
		ix, iy = (int(x), int(y))
		nodes = [self.tile(ix, iy), self.tile(ix+1, iy), 
						self.tile(ix, iy+1), self.tile(ix+1, iy+1)]
		if all(map(lambda x:x, nodes)):
			vx,vy = (x-ix, y-iy)
			param = [(0,1,0), (0,1,1), (2,3,0), (2,3,1)]
			vcut = [nodes[p1].pos[ax]+(nodes[p2].pos[ax]-nodes[p1].pos[ax])*vx
				for p1, p2, ax in	param]
			rx = vcut[0]+(vcut[2]-vcut[0])*vy
			ry = vcut[1]+(vcut[3]-vcut[1])*vy
			return (rx,ry)
		return None

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
			out.append(' '.join([' .:+#&'[int(v>1)+int(v>2)+int(v>4)+int(v>7)+int(v>10)] for v in row]))

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
		#tile = self.tiles.values()[rnd(0,len(self)-1)]
		#vertices = gfx.vertex_list(4,
		#	('v2i', tile.get_bounds()),
		#	('c3B', (255,0,0,150,50,0,50,150,0,100,200,50)))
	
		if self.batch is None:
			self.batch = gfx.Batch()
			for x in range(0,self.width):
				for y in range(0,self.height):
					tile = self.tiles[(x,y)]
					val=200
					for cx, cy in [(1,0), (1,1)]:
						nn = self.tiles.get((x+cx,y+cy), None)
						if nn:
							val+=int(nn.elevation-tile.elevation)
					cols=(max(0,min(255,val)),)*12
					self.batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
						[0,1,2,0,2,3],
						('v2i', tile.get_bounds()),
						('t2f', (0., 0., .12, 0., .12, .12, 0., .12)),
						('c3B', cols))
		return self.batch




# APi stuff
topo=None

# factory method
def create(width, height, maxelevation):
	global topo
	if not topo:
		topo=Map(width, height)
		topo.init_map(maxelevation)
	return topo

def get():
	return topo

# A* path finding initiator
def find_path(orig, dest):
	x,y=orig
	orig = topo.tile(x,y)
	x,y=dest
	dest = topo.tile(x,y)
	return pathfinder.AStar(orig, dest)
