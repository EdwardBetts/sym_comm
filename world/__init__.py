import game
import tilemap
import pathfinder

#__all__ = ["tilemap", "inhabitants"]
__doc__="restructuredtext"



### Instantiate and initialize tile map ###
width, height = game.mapsize
maxelevation = game.mapelevation

# creates tilemap instance, initializes it
def create():
	"""
	Creates a new tilemap instance and initiates it using
	geosimulation methods for heightmap, water and ground vegetation
	generation. Returns said instance."""
	print 'create tile map instance'
	surface = tilemap.new(width, height, maxelevation)
	#for i in range(5):
		#tilemap.generator.rain(surface, 2000)
	springlevel=len(surface)/5
	springrange=springlevel/2
	print springlevel
	print 'run water simulation'
	for i in range(1):
		tilemap.generator.rain(surface, 40, 
			springs=[s for s in surface.highest(
			springlevel+(springrange)/(i+1))[springlevel::springrange/5]])
	print 'smooth out heightmap irritations'
	tilemap.generator.smoothen(surface,1)
	print 'run grass growing simulation'
	tilemap.generator.sprout(surface)
	print 'apply tile map node parameters, compute node polygon coordinates'
	surface.init_mesh()
	print 'return tile map instance'
	return surface


# draw world and components
def draw():
	"""
	Draw world components"""
	tilemap.draw()

# A* path finding initiator
def find_path(orig, dest):
	"""
	Returns a pathfinder instance?"""
	#x,y=orig.pos
	#orig = surface.tile(x,y)
	#x,y=dest.pos
	#dest = surface.tile(x,y)
	return pathfinder.astar(orig, dest)


surface = create()
