import pyglet
import os

ext_img = ['png', 'jpg', 'gif', 'tiff', 'bmp']

pyglet.resource.path=['.']
pyglet.resource.reindex()

path_inhabitants = os.sep.join(['media', 'inhabitants'])
WORLD = path_world = os.sep.join(['media', 'world'])


atlas = pyglet.image.atlas.TextureAtlas(width=1024, height=1024)

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
