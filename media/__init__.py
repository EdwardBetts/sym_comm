import pyglet
import os
import time

ext_img = ['png', 'jpg', 'gif', 'tiff', 'bmp']

pyglet.resource.path=['textures']
pyglet.resource.reindex()

path_inhabitants = os.sep.join(['media', 'inhabitants'])
WORLD = path_world = os.sep.join(['media', 'world'])


# create texture atlas for whatevs. TODO: who uses this?
atlas = pyglet.image.atlas.TextureAtlas(width=1024, height=1024)

# obtain buffer manager singleton for screenshots etc.
buffer_manager = pyglet.image.get_buffer_manager()

# string identifying the current date (day prec) on startup
# TODO: why again?
# startup_date = date_string()

# format the current date like 130405 (year, month, day)
def date_string():
	lt = time.localtime()
	return '{}{:0>2}{:0>2}'.format(lt.tm_year, lt.tm_mon, lt.tm_mday)[2:]

# loads the image at location given by
# filename and template like 'path/{filename}'
# as Textureregion
def load(filename, path):
	temp = os.sep.join([path,'{}'])
	# extension accepted?
	if filename.split('.')[-1] in ext_img:
		ret = pyglet.resource.image(temp.format(filename))
		print ret
		return atlas.add(ret)
	else:
		# try to find an image resource matching the 
		# given filename
		for ext in ext_img:
			try:
				guess = temp.format(
					'.'.join([filename, ext]))
				ret = pyglet.resource.image(guess)
				return atlas.add(ret)
			except Exception, e:
				pass

#TODO: possibly hardly any of the following makes any sense
# loads Textureregion for inhabitant
def inhabitant_tex(filename):
	# return sth
	ret = load(filename, path_inhabitants)
	return ret

# loads Textureregion for world/map imagery
def world_tex(filename):
	ret = load(filename, path_world)
	return ret
	

def image(path, filename):
	ret = pyglet.image.load(''.join([path, filename]))
	return atlas.add(ret)


def sprite(path, filename):
	return pyglet.resource.image(os.sep.join([path, filename]))


def atlas_load(filename):
	"""
	Loads an image file located in the textures directory
	and specified by the given filename, adds it to the
	texture atlas and returns the resulting texture."""
	t = pyglet.image.load(os.path.join('textures','ground.png'))
	tex = atlas.add(t)
	return tex



# takes a screenshot and saves it to the screenshot directory
def screenshot():
	date = date_string()
	screenshot_id = 1
	for fn in os.listdir('screenshots'):
		if date in fn:
			try:
				i = int(fn.split('_')[-1][:3])
				screenshot_id = max(i+1, screenshot_id)
			except:
				pass
	fn = 'screen{}_{:0>3}.png'.format(date, screenshot_id)
	screen = buffer_manager.get_color_buffer()
	try:
		screen.save(os.path.join('screenshots', fn))
		print 'screenshot saved under {}.'.format(fn)
	except:
		print 'could not write to file {}.'.format(fn)
