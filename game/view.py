from pyglet.gl import *


class Camera:

	def __init__(self, window, pos):
		self.x, self.y = pos
		self.zoom = 1.
		self.width=window.width
		self.height=window.height
		self.window = window
		self.ortho = [] # area to be mapped into game window

	def update(self):
		self.resize()
		glViewport(0, 0, self.width, self.height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		cns = self.ortho
		glOrtho(cns[0], cns[2], cns[1], cns[3], -1, 1)
		glMatrixMode(gl.GL_MODELVIEW)
	
	def resize(self):
		width, height = (self.window.width, self.window.height)
		corners = [-width/2, -height/2, width/2, height/2]
		self.ortho=map(lambda x:x[0]+x[1]*self.zoom, 
			zip([self.x,self.y]*2, corners))
		self.width, self.height = (width, height)
	
	# handles zoom. 1=normal, <1 smaller area visible, 
	# >1 larger area visible
	def update_zoom(self, pos, steps):
		self.zoom *= .95**steps
		if self.zoom > 4:
			self.zoom = 4
		elif self.zoom < .25:
			self.zoom = .25
		self.move(-(pos[0]-self.width/2)*steps/10,
			-(pos[1]-self.height/2)*steps/10)
		self.update()
		
	def move(self, dx, dy):
		self.x -= dx*self.zoom
		self.y -= dy*self.zoom
		self.update()

cam=None
def create(window, width, height):
	global cam
	cam = Camera(window, (width, height))
	return cam

def get():
	return cam
