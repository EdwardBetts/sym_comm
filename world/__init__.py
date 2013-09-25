import game
import tilemap
import pathfinder

#__all__ = ["tilemap", "inhabitants"]
__doc__="restructuredtext"



### Instantiate and initialize tile map ###
width, height = game.mapsize
maxelevation = game.mapelevation

surface = tilemap.new(width, height, maxelevation)
#tilemap.generator.rain(surface, 100)

# A* path finding initiator
def find_path(orig, dest):
	"""
	Returns a pathfinder instance?"""
	x,y=orig.pos
	orig = surface.tile(x,y)
	x,y=dest.pos
	dest = surface.tile(x,y)
	return pathfinder.astar(orig, dest)


