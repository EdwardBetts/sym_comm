import pyglet
import os

ext_img = ['png', 'jpg', 'gif', 'tiff', 'bmp']

pyglet.resource.path=['.']
pyglet.resource.reindex()

path_inhabitants = os.sep.join(['media', 'inhabitants', ''][0:])
WORLD = path_world = os.sep.join(['media', 'world', ''][0:])

# loads the image at location given by
# filename and template like 'path/{filename}'
# as Textureregion
def load(filename, path):
	temp = path+'{filename}'
	# extension accepted?
	if filename.split('.')[-1] in ext_img:
		return pyglet.resource.texture(
			temp.format(filename=filename))
	else:
		# try to find an image resource matching the 
		# given filename
		for ext in ext_img:
			try:
				guess = temp.format(filename=
					'.'.join([filename, ext]))
				return pyglet.resource.texture(guess)
			except Exception, e:
				pass


# loads Textureregion for inhabitant
def inhabitant_txt(filename):
	# return sth
	ret = load(filename, path_inhabitants)
	if not ret:
		ret = pyglet.resource.texture('jaja01.png')
	if ret:
		return ret.get_texture()
	return None

# loads Textureregion for world/map imagery
def world_tex(filename):
	ret = load(filename, path_world)
	if ret:
		return ret #.get_texture()
	return None
	

def image(path, filename):
	return pyglet.image.load(''.join([path, filename]))
