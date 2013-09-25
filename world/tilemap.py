import pyglet.graphics as gfx
from pyglet.gl import *
from random import randint as rnd
from random import random as rndf

import game
import media
from world import generator
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

tex=None

# implementation of single tile map node
class Tile(object):
	"""
	Class for single map tile
	"""

	@staticmethod
	def new(topo):
		"""
		Creates, registers and returns a brand new Tile node instance"""
		return Tile(topo)
		

	counter=0

	def __init__(self, tilemap):
		super(Tile, self).__init__()
		ID = Tile.counter
		Tile.counter += 1

		self.map = tilemap
		self.x = ID % self.map.width
		self.y = ID // self.map.width
		self.ID = ID
		# topological elevation of this map tile; heightmap
		# feature
		self.elevation = 0

		# upper-left corner of this tile for to estimate
		# where it is to find on the graphical output
		self.coord=(self.x*20, self.y*20)

		# the tiles directly adjacent to this tile
		#TODO: store walking cost between nodes in here?
		self.neighbours = {}
		# coordinates of the graphical representation of this
		# tile, a four point polygon
		# TODO: implement, handle as a vertex list or whatev
		self.bounds = None

		# 0 = normal ground, 1 = water, 2 = dirt road
		#self.type = 0

		# vegetation level of this tile
		self._veget = 0

		# water level at this node. rendered tile elevation minus
		# water level should equal tile's original elevation value
		self._water = 0

		# indicator for how good one can walk on this tile
		# 1: minimum, the higher the better
		# TODO: heuristic/improve this!
		self._walkbl = 1

		# the resource this tile supplies
		self.resource = None


	@property
	def level(self):
	    return self.elevation
	@level.setter
	def level(self, level):
		"""
		sets the elevation value for this point. also, updates
		2d coordinates of reference center point"""
		if self.waterlevel > 0:
			diff = level - self.elevation
			self._water = max(0, self._water - diff)
		self.elevation = level
		x = self.x*20
		y = (topo.height-self.y)*20
		y += int(level)
		self.pos = (x,y)	

	@property
	def vegetation(self):
	    return self._veget
	@vegetation.setter
	def vegetation(self, level):
	    self._veget = level
	    self._walkbl = 5./(5+self._veget) / min(self._water/10,5.)

	@property*
	def waterlevel(self):
	    return self._water
	@waterlevel.setter
	def waterlevel(self, level):
	    self.elevation = self.elevation-self._water
	    self._water = level
	    self.elevation = self.elevation+self._water
	    self._walkbl = 5./(5+self._veget) / min(self._water/10,5.)

	@property
	def walkability(self):
	    return self._walkbl
	@walkability.setter
	def walkability(self, value):
	    self._walkbl = min(value, self._walkbl)


	# sets up links to neighbour nodes.
	def assign_neighbours(self):
		"""
		identifies the adjacent map tiles of this tiles and
		stores them in the self.neighbours dictionary with
		the respective relative cardinal direction as the key,
		like 'n', 'sw', 'nw' etc."""
		n = self.neighbours
		for key,rx,ry in nrel:
			#neighbour = self.map.tile((self.x+rx) % self.map.width,
							#(self.y+ry)) # % self.map.height)
			neighbour = self.map.tile(self.x+rx, self.y+ry)
			if neighbour:
				n[key] = neighbour

	@property
	def pos(self):
		return (self.x, self.y)


	# creates an array of bounding coordinates for this
	# tile's polygonal representation
	# [tile itself, east neighbour, southeast, south]
	def assign_bounds(self):
		"""
		assigns the coordinates of the polygon representing this
		map tile, taking adjacent tiles into account"""
		nn = self.neighbours
		x = self.coord[0]
		self.bounds=[x, self.coord[1]]
		for nx,d in [(x+20,'e'), (x+20,'se'), (x,'s')]:
			n = nn.get(d)
			if n:
				self.bounds+=[nx, n.coord[1]]
			else:
				if d == 'se' and 's' in nn:
					self.bounds+=[nx, nn.get('s').coord[1]]
				elif 'e' in nn and not d == 's':
					self.bounds+=[nx, nn.get('e').coord[1]-20]
				else:
					self.bounds+=[nx, self.coord[1]-20*int('s' in d)]


	def get_bounds(self):
		"""
		returns an array of a four-point polygon representing
		this map tile"""
		if not self.bounds:
			# start top-left, go clockwise
			self.assign_bounds()
		return self.bounds


	def accessability(self, tile):
		"""
		returns a value indicating how hard it is to walk from
		this tile to a (most likely) adjacent tile. The higher the value,
		the harder is it to walk this direction and the more likely are
		inhabitants to avoid it when walking around. """
		# distance
		g = [0,1,1.5][int(self.x!=tile.x) + int(self.y!=tile.y)]
		# tiles very own walkability parameters for special purposes
		g *= 1 + 2/(self._walkbl + tile._walkbl) # (default to 1)
		# slope
		g += tile.elevation - self.elevation

		return g


	# computes the distance between this node and a given one
	# considers diagonal links
	def distance(self, tile):
		return max(abs(self.x-tile.x), abs(self.y-tile.y))







##################################################################
##################################################################
##################################################################
#######################                         ##################
####################### Tile Map implementation ##################
#######################                         ##################
##################################################################
##################################################################
##################################################################
##################################################################


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
		self.tex = None


	# create content
	def init(self, maxheight):
		"""creates links between adjacent tiles, generates heightmap
		and computes coordinates for graphical representation of
		contained tiles"""
		while Tile.counter < self.width*self.height:
			n = Tile(self)
			self.tiles[(n.x,n.y)] = n
		print "   map tiles instantiated: %d" % Tile.counter
		for pos,tile in self.tiles.items():
			tile.assign_neighbours()
		generator.init_heightmap(self, maxheight)
		# compute coords for polygon representation
		for pos,tile in self.tiles.items():
			tile.assign_bounds()


	# return tile at requested position
	def tile(self, x, y):
		"""returns the map tile at the given index ``(x,y)``"""
		return self.tiles.get((x,y), None)




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
			vcut = [nodes[p1].coord[ax]+
				(nodes[p2].coord[ax]-nodes[p1].coord[ax])*vx
				for p1, p2, ax in param]
			rx = vcut[0]+(vcut[2]-vcut[0])*vy
			ry = vcut[1]+(vcut[3]-vcut[1])*vy
			return (rx,ry)
		return None


	# REPR
	def __repr__(self):
		"""
		returns a string representation of the world's heighmap"""
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
		its height"""
		return self.width*self.height


	def image(self):
		"""
		dummy method that returns the graphical representation
		of a random map tile as a vertex_list, just for debugging"""
		# http://packages.python.org/pyglet/api/pyglet.image.AbstractImage-class.html#blit_into
		if not self.tex:
			self.tex = load_tex()
		if self.tex:
			#glEnable(self.tex.target)
			if self.batch is None:
				self.batch = gfx.Batch()
				glActiveTexture(GL_TEXTURE0+0)
				glBindTexture(self.tex.target, self.tex.id)
				txmx=self.tex.tex_coords[3]-self.tex.tex_coords[0]
				txmy=self.tex.tex_coords[7]-self.tex.tex_coords[4]
				for x in range(0,self.width):
					for y in range(0,self.height):
						tile = self.tiles[(x,y)]
						val=200
						for cx, cy in [(1,0), (1,1)]:
							nn = self.tiles.get((x+cx,y+cy), None)
							if nn:
								val+=int(nn.elevation-tile.elevation)
						cols=(max(0,min(255,val)),)*12
						# schoen auch die ecken!
						nn = [(tile.waterlevel, tile.elevation)]
						for d in ['e', 'ne', 'n']:
							if d in tile.neighbours:
								nn.append((tile.neighbours.get(d).waterlevel,
									tile.neighbours.get(d).elevation))
							else:
								nn.append((None, 0))
						# elevation?
						cns = [(e>(20+3*rndf()), w>0)
							for (w,e) in nn]
						# gras, wasser tex ids
						gx = sum([int(v[0])*2**i for i,v in enumerate(cns)])
						wx = sum([int(v[1])*2**i for i,v in enumerate(cns)])
						coor = (wx*txmx/16,gx*txmy/16,
										(wx+1)*txmx/16,gx*txmy/16,
										(wx+1)*txmx/16,(gx+1)*txmy/16,
										wx*txmx/16,(gx+1)*txmy/16)
						coor = (wx*txmx/16,gx*txmy/16,
										(wx+1)*txmx/16,gx*txmy/16,
										(wx+1)*txmx/16,(gx+1)*txmy/16,
										wx*txmx/16,(gx+1)*txmy/16)
						self.batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
							[0,1,2,0,2,3],
							('v2i', tile.get_bounds()),
							('t2f', coor), #(0., 0., .12, 0., .12, .12, 0., .12)),
							('c3B', cols))
		return self.batch



def load_tex():
	#tex = media.world_tex('ground.png')
	t = pyglet.image.load('media/world/ground.png')
	tex = media.atlas.add(t)
	if not tex:
		return
	#data=tex.get_image_data().get_data('RGBA', tex.width*4)
	target=GL_TEXTURE_2D
	#tex=img.get_texture()
	#tid=tex.id
	#tid=glGenTextures(1)
	#glActiveTexture?
	glEnable(tex.target)
	glBindTexture(tex.target, tex.id)
	glTexParameteri(tex.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(tex.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	#glTexParameteri(tex.target, GL_TEXTURE_WRAP_S, GL_CLAMP)
	#glTexParameteri(tex.target, GL_TEXTURE_WRAP_T, GL_CLAMP)
	print tex.width, tex.height
	#glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex.width, tex.width,
		 #0, GL_RGBA, GL_UNSIGNED_BYTE, data)
	print tex.tex_coords
	#glDisable(target)
	tex.save('t.png')
	return tex



# create instance
def new(width, height, maxlevel):
	"""
	Creates a new Map instance with a basic heightmap and returns it."""
	surface = Map(width, height)
	surface.init(maxlevel)
	return surface



