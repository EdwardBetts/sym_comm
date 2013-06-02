import pyglet
import os

ext_img = ['png', 'jpg', 'gif', 'tiff', 'bmp']

path_inhabitants = os.sep.join(['media', 'inhabitants', ''])
path_world = os.sep.join(['media', 'world', ''])

# loads the image at location given by
# filename and template like 'path/{filename}'
# as TextureRegion
def load(filename, path):
	temp = path+'{filename}'
	# extension accepted?
	if filename.split('.')[-1] in ext_img:
		return pyglet.resource.image(
			temp.format(filename=filename))
	else:
		# try to find an image resource matching the 
		# given filename
		for ext in ext_img:
			try:
				guess = temp.format(filename=
					'.'.join([filename, ext]))
				return pyglet.resource.image(guess)
			except Exception, e:
				pass


# loads TextureRegion for inhabitant
def inhabitant_txt(filename):
	# return sth
	ret = load(filename, path_inhabitants)
	if not ret:
		ret = pyglet.resource.image('jaja01.png')
	if ret:
		return ret.get_texture()
	return None

# loads TextureRegion for world/map imagery
def world_txt(filename):
	ret = load(filename, path_world)
	if ret:
		return ret.get_texture()
	return None
	
