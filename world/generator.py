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
	print 'generate heightfield for map {}x{} with max level {}'.format(
		surface.width, surface.height, maxheight)
	# create elevation seed points
	clusters=[]
	for i in range(min(surface.width*surface.height/100,200)):
		y = rnd(surface.height)
		clusters+=[(rnd(surface.width), y,
			(rndf()-(.5*y/surface.height)) * maxheight)]
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
			if nearest[1] > maxheight*2/3:
				t.elevation = nearest[1]+ maxheight/5.*rndf()
			elif nearest[1] < 0:
				t.elevation = nearest[1]
			else:
				t.elevation = nearest[1]+ maxheight/4.*(-.5+rndf())
			t.elevation = t.elevation + maxheight/4.*(-.5+rndf())
	smoothen(surface,2)




def smoothen(surface, iterations):
	# smooth heightmap by calculating means of each
	# tile's neighbours elevation values
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
def rain(surface, amount, springs=None):
	"""
	Simulates a given amount of water falling down onto the given
	tile map."""
	print 'It rains: {} units of rain water'.format(amount),
	if springs:
		print 'and {} springs.'.format(len(springs)),
	# water already in map
	drops={t:t.waterlevel for t in surface.tiles.values()
		if t.waterlevel > 0} # key: tile, value: water
	while amount>0:
		x,y = rnd(surface.width), rnd(surface.height)
		t=surface.tile(x,y)
		n = rndf()*10+2
		drops[t] = drops.get(t,0) + n
		amount -= n
	print 'Number of wet tiles at beginning is {}.'.format(len(drops))
	# 
	wettrans=[1]
	speed=10.
	count=0
	erosion=0.
	while max(wettrans)>.05 and count<5000:
		count += 1
		#fldd = {k:v for k,v in drops.items()}
		fldd = {}
		wettest=0
		# quellen
		if springs:
			for s in springs:
				drops[s] = drops.get(s,0) + 5./(1.+count/10)
		# flooding
		for t,w in drops.items():
			for n in sorted(t.neighbours.values(), 
				key=lambda n:drops.get(n,0)):
				# see how much this neighbour can possibly take
				nw = drops.get(n,0) 
				gap = min(w + t.elevation - (nw + n.elevation), w)
				# if neighbour has potential, transfer 1/3 of it
				if gap > 0:
					share = gap/3
					fldd[n] = fldd.get(n,0)+share
					# erode!
					if share>.5:
						if max([nn.elevation-n.elevation 
							for nn in n.neighbours.values()])<20:
							n.elevation -= share/10
							erosion += share/10
					fldd[t] = fldd.get(t,0)-share
					w -= share
					wettest = max(share, wettest)
		# update water map
		for k,v in fldd.items():
			level = drops.get(k,0)+v
			drops[k] = level
			if level<.05 and abs(v)<.05:
				del drops[k]
		wettrans = [wettest] + wettrans[:5]
		if max(wettrans)<speed/2:
			speed /= 2
			print 'Floating deccelerated under {:.2f}'.format(
				max(wettrans))
		#print 'Wettest transfer had {:.2f} units water.'.format(
			#wettest),
		#print 'Total amount is {:.2f}, max {:.2f}'.format(
			#sum(drops.values()), max(drops.values()))
	# ok enough
	for t in surface.tiles.values():
		t.waterlevel = drops.get(t,0)
	print '{} floodings. Last transfer: {:.2f}. Total on map: {:.2f} on {} tiles.'.format(
		count, wettest, surface.water(), len(drops)),
	print 'Grade of erosion was {:.2f}.'.format(erosion)
