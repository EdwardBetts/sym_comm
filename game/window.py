import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from random import randint as rnd
import media
import graphics
import world
import world.pathfinder
from game import view
from world import inhabitants
from world.inhabitants import jaja


class Window(pyglet.window.Window):

	def __init__(self):
		# double_buffer = True, depth_size = 24
		# window flip() is invoked after every on_draw() event
		config = Config(double_buffer=True)
		super(Window, self).__init__(resizable=True, config=config)
		glClearColor(0.1,0.2,0,1)
		glEnable(GL_TEXTURE_2D)
		glShadeModel(GL_SMOOTH)


		#self.label = pyglet.text.Label('Gebrauchswert')

		#self.batch = pyglet.graphics.Batch()
		#self.jaja = pyglet.sprite.Sprite(
			#media.inhabitant('jaja01'), batch=self.batch)

		self.clock = pyglet.clock.ClockDisplay()
		#pyglet.clock.schedule_interval(self.update, 1./24)
		pyglet.clock.set_fps_limit(36)

		#impt = pyglet.image.SolidColorImagePattern((100,180,90,200))
		#self.bg = pyglet.image.create(800,600, impt)

		self.worldimage = world.get().image()
		self.viewport = view.create(self, self.width/2,self.height/2)

		world.inhabitants.jaja.create(6,5)
		world.inhabitants.jaja.create(10,6)
		world.inhabitants.jaja.create(4,8)

		#self.pathfinder = world.pathfinder.find_path(
			#world.get().tile(5,25),
			#world.get().tile(55,25))


	def on_resize(self, width, height):
		self.viewport.update()
		return pyglet.event.EVENT_HANDLED


	def on_mouse_scroll(self,x, y, scroll_x, scroll_y):
		self.viewport.update_zoom((x,y), scroll_y)
		# viewport updates itself
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if buttons & mouse.LEFT:
			self.viewport.move(dx,dy)
			# updates itself


	def on_draw(self):
		glClear(GL_COLOR_BUFFER_BIT)
		pyglet.clock.tick() # force framerate set above
		#self.label.draw()

		glEnable(GL_TEXTURE_2D)
		self.worldimage.draw() # map
		glDisable(GL_TEXTURE_2D)

		self.clock.draw() # clock

		#if self.pathfinder:
			#if self.pathfinder.result():
				#self.pathfinder.draw()
				#j = world.inhabitants.registry[-1]
				#if len(j.path)<1:
					#j.path = self.pathfinder.result()

		inhabitants.draw()
		inhabitants.update()


window = None

def create():
	global window
	window = Window()
	return window

def get():
	return window
