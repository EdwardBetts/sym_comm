import pyglet
import media
import world.inhabitants

image = media.inhabitant_txt('jaja01')

class Jaja(world.inhabitants.Inhabitant):

	def __init__(self, x, y):
		super(Jaja, self).__init__(image, x, y)
		
		
def create(x, y):
	return Jaja(x, y)
	
