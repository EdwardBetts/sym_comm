import pyglet
import os

ext_img = ['png', 'jpg', 'gif', 'tiff', 'bmp']

path_inhabitants = os.sep.join(['media', 'inhabitants'])


def inhabitant(filename):

	temp = path_inhabitants+os.sep+'{filename}'

	# does the filename come with an extension?
	if filename.split('.') in ext_img:
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

	
	# return sth
	pyglet.resource.image('jaja01.png')