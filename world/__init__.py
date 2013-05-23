import world.tilemap
import game

__all__ = ["worldmap"]
__doc__="restructuredtext"



### Instantiate and initialize tile map ###
width, height = game.mapsize
maxelevation = game.mapelevation
map=world.tilemap.create(width, height, maxelevation)
