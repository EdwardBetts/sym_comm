import world.tilemap
import game
#import inhabitants
#import world.inhabitants

#__all__ = ["tilemap", "inhabitants"]
__doc__="restructuredtext"



### Instantiate and initialize tile map ###
width, height = game.mapsize
maxelevation = game.mapelevation
tilemap=tilemap.create(width, height, maxelevation)

def get():
	return tilemap

