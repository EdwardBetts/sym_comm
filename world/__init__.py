import worldmap

__all__ = ["worldmap"]
__doc__="restructuredtext"



def create_map(width, height, maxelevation=25):
	"""
	creates a map by calling the worldmap.create method
	returns initialized map instance
	"""
	global _map
	print "creating world map with dimensions %dx%dx%d" % \
		(width, height, maxelevation)
	worldmap.create(width, height, maxelevation)
	print "retrieving world map singleton"
	_map = worldmap.get()
	print "world map creation complete"
	return _map


def map():
	global _map
	if _map is not None:
		print "returning map object: %d" % len(_map)
		return _map
	else:
		print "no map instantiated. creating..."
		create_map(30,20,25)


_map=None