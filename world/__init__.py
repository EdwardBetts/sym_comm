import game
import tilemap
import pathfinder

#__all__ = ["tilemap", "inhabitants"]
__doc__="restructuredtext"



### Instantiate and initialize tile map ###
width, height = game.mapsize
maxelevation = game.mapelevation

surface = tilemap.new(width, height, maxelevation)
for i in range(4):
	tilemap.generator.rain(surface, 200, 
		springs=[s for s in surface.highest(50)[::10]])
tilemap.generator.rain(surface, 500)
tilemap.generator.smoothen(surface,2)
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


