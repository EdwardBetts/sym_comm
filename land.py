#!/usr/bin/python

import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from random import randint as rnd

class Window(pyglet.window.Window):

	def __init__(self):
		# double_buffer = True, depth_size = 24
		# window flip() is invoked after every on_draw() event
		config = Config(double_buffer=True)
		super(Window, self).__init__(resizable=True, config=config)
		glClearColor(0.1,0.2,0,1)
		glEnable(GL_TEXTURE_2D)
		glShadeModel(GL_SMOOTH)

		self.clock = pyglet.clock.ClockDisplay()
		pyglet.clock.set_fps_limit(36)


	def on_resize(self, width, height):
		self.viewport.update()
		return pyglet.event.EVENT_HANDLED


	def on_mouse_scroll(self,x, y, scroll_x, scroll_y):
		self.viewport.update_zoom((x,y), scroll_y)
		# viewport updates itself
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if buttons & mouse.LEFT:
			self.viewport.move(dx,dy)

	def on_draw(self):
		glClear(GL_COLOR_BUFFER_BIT)
		pyglet.clock.tick() # force framerate set above
