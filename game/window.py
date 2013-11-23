import pyglet
from pyglet.gl import *
from pyglet.window import mouse, key
from random import randrange as rnd
from time import time

import media
import graphics
import world
from game import view
from world import inhabitants
from world.inhabitants import jaja



# only pass inhabitants!
#TODO: we can't do this in here!
def map_pos(i):
	if isinstance(i, inhabitants.Inhabitant):
		return world.surface.ground_position(i.x, i.y)


# game window
class Window(pyglet.window.Window):

	def __init__(self):
		# double_buffer = True, depth_size = 24
		# window flip() is invoked after every on_draw() event
		config = Config(double_buffer=True)
		super(Window, self).__init__(resizable=True, config=config)
		glClearColor(0.1,0.2,0,1)
		glEnable(GL_TEXTURE_2D)
		#glShadeModel(GL_SMOOTH) # TODO: what does this do?

		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		# some kind of event history
		self.history={}

		#self.label = pyglet.text.Label('Gebrauchswert')

		#self.batch = pyglet.graphics.Batch()
		#self.jaja = pyglet.sprite.Sprite(
			#media.inhabitant('jaja01'), batch=self.batch)

		self.clock = pyglet.clock.ClockDisplay()
		#pyglet.clock.schedule_interval(self.update, 1./24)
		pyglet.clock.set_fps_limit(36)

		#impt = pyglet.image.SolidColorImagePattern((100,180,90,200))
		#self.bg = pyglet.image.create(800,600, impt)

		self.viewport = view.create(self, self.width/2,self.height/2)

		#TODO: get this out of here!
		j = jaja.create(world.surface.width/2,world.surface.height/2)
		self.viewport.goto(map_pos(j))
		self.viewport.zoom = 1.2
		for i in range(25):
			jaja.create(rnd(world.surface.width),rnd(world.surface.height))






	def on_resize(self, width, height):
		self.viewport.update()
		return pyglet.event.EVENT_HANDLED


	def on_mouse_press(self, x, y, button, modifiers):
		if button & mouse.LEFT:
			# double click:
			if time() - self.history.get('left_click',0) < .5:
				#TODO: delegate this where it belongs...
				self.viewport.zoom = 4.25-self.viewport.zoom
				# TODO: and take care of mouse pointer position translation
				self.viewport.update()
			self.history['left_click']=time()



	def on_mouse_scroll(self,x, y, scroll_x, scroll_y):
		self.viewport.update_zoom((x,y), scroll_y)
		# viewport updates itself

	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if buttons & mouse.LEFT:
			self.viewport.move(-dx,-dy)
			# updates itself


	def on_key_press(self, symbol, modifiers):
		print symbol, modifiers
		if symbol == key.LEFT:
			self.viewport.move(-10,0)
		elif symbol == key.RIGHT:
			self.viewport.move(10,0)
		elif symbol == key.S:
			if modifiers & key.MOD_CTRL:
				media.screenshot()


	def keyhandler(self):
		if self.keys[key.LEFT]:
			self.viewport.move(-10,0)
		elif self.keys[key.UP]:
			self.viewport.move(0,10)
		elif self.keys[key.DOWN]:
			self.viewport.move(0,-10)
		elif self.keys[key.RIGHT]:
			self.viewport.move(10,0)


	def on_draw(self):
		self.keyhandler()
		glClear(GL_COLOR_BUFFER_BIT)
		pyglet.clock.tick() # force framerate set above
		#self.label.draw()

		world.draw()

		self.clock.draw() # clock

		inhabitants.draw()
		inhabitants.update()


instance = None

def create():
	global instance
	instance = Window()
	return instance

def get():
	global instance
	if not instance:
		instance = create()
	return instance
