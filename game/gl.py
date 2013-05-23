import pyglet
from pyglet.gl import *
from random import randint as rnd
import media
import graphics
import world

class Window(pyglet.window.Window):

	def __init__(self):
		# double_buffer = True, depth_size = 24
		# window flip() is invoked after every on_draw() event
		super(Window, self).__init__()
		self.label = pyglet.text.Label('Gebrauchswert')

		self.batch = pyglet.graphics.Batch()
		self.jaja = pyglet.sprite.Sprite(
			media.inhabitant('jaja01'), batch=self.batch)

		self.clock = pyglet.clock.ClockDisplay()

		impt = pyglet.image.SolidColorImagePattern((100,180,90,200))
		self.bg = pyglet.image.create(800,600, impt)

		self.vertices = graphics.raster()

		self.worldimage = world.map.image()


	def on_draw(self):
		self.bg.blit(0,0)
		self.label.draw()

		self.worldimage.draw()
		self.clock.draw()

		self.vertices.draw(GL_LINE_STRIP)

		self.batch.draw()
		self.jaja.x += rnd(0, 2)
		self.jaja.y += rnd(0, 2)


