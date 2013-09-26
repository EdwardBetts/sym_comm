import game
import tilemap
import pathfinder

#__all__ = ["tilemap", "inhabitants"]
__doc__="restructuredtext"



### Instantiate and initialize tile map ###
width, height = game.mapsize
maxelevation = game.mapelevation

surface = tilemap.new(width, height, maxelevation)
#for i in range(5):
	#tilemap.generator.rain(surface, 2000)
for i in range(2):
	tilemap.generator.rain(surface, 40, 
		springs=[s for s in surface.highest(400/(i+1))[100::20]])
tilemap.generator.smoothen(surface,1)
surface.init_mesh()

# A* path finding initiator
def find_path(orig, dest):
	"""
	Returns a pathfinder instance?"""
	#x,y=orig.pos
	#orig = surface.tile(x,y)
	#x,y=dest.pos
	#dest = surface.tile(x,y)
	return pathfinder.astar(orig, dest)


