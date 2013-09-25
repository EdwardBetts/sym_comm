#!/usr/bin/python

from random import random as rndf, randrange as rnd

# set up heightmap
def init_heightmap(surface, maxheight):
	"""
	Generates a new topography for the given Map instance. It can be
	expected to have some hills, plateaus, and even some cute pits
	for water to filling them.
	Elevation levels will be between (-maxheight/10, maxheight) or 
	beneath	or below."""
	# create elevation seed points
	clusters=[]
	for i in range(min(surface.width*surface.height/100,200)):
		clusters+=[(rnd(surface.width), rnd(surface.height),
			(1.1*rndf()**2-.1)*maxheight)]
	# landschaftsgaertnerei
	# unten flach
	clusters.extend([[x,surface.height-1,0] 
		for x in range(surface.width)[::4]])
	# oben schoen berge
	clusters.extend([[x,0,maxheight] 
		for x in range(surface.width)[::4]])
	print 'generate heightmap'
	# assign elevation init values with clustering algorithm
	for y in range(surface.height):
		print '\r','.'*(30*y/surface.height),
		for x in range(surface.width):
			t = surface.tile(x,y)
			clsts = [((c[0]-x)**2+(c[1]-y)**2, c[2]) for c in clusters]
			nearest=sorted(clsts, key=lambda c:c[0])[0]
			if nearest[1] > maxheight/2 and nearest[1] < maxheight/5:
				t.elevation = nearest[1]+rndf()**2*10
			elif nearest[1] < 0:
				t.elevation = nearest[1]-rndf()**2*6
			else:
				t.elevation = t.elevation/1.1
	# smooth heightmap by calculating means of each
	# tile's neighbours elevation values
	iterations=2
	for i in range(iterations):
		for x in range(surface.width):
			surface.tile(x,surface.height-1).elevation=0
		topo = []
		for y in range(surface.height):
			print '\r', '#'*(30*(y+i*surface.height)/surface.height/iterations),
			topo.append([])
			for x in range(surface.width):
				n = surface.tile(x,y)
				topo[y].append(
					sum([nn.elevation for nn in
					n.neighbours.values()+[n]])
					/ (len(n.neighbours)+(1.+y/surface.height)))
		# assign smoothened heightmap values to tile instances
		for y in range(surface.height):
			for x in range(surface.width):
				surface.tile(x, y).level = topo[y][x]+2.



# let it rain!
def rain(surface, amount):
	"""
	Simulates a given amount of water falling down onto the given
	tile map."""
	drops={}
	while amount>0:
		x,y = rnd(surface.width), rnd(surface.height)
		n = rndf()*10
		drops[(x,y)] = drops.get((x,y),0)+n
		amount -= n
	# ok
	for (x,y),n in drops.items():
		surface.tile(x,y).waterlevel = n
