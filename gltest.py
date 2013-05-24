import pyglet
import game.window
import world

if __name__ == '__main__':

	platform = pyglet.window.get_platform()
	display = platform.get_default_display()
	screen = display.get_default_screen()

	# all configurations with either an auxilliary buffer or an 
	# accumulation buffer are printed:
	for config in screen.get_matching_configs(pyglet.gl.Config()):
		if config.aux_buffers or config.accum_red_size or True:
			print config
	
	for extension in sorted(pyglet.gl.gl_info.get_extensions()):
		print extension

	print pyglet.gl.gl_info.get_version()
	print pyglet.gl.gl_info.get_renderer()


	
	print world.get()
	for tile in world.get().tiles.values():
		if len(tile.get_bounds()) != 8:
			print tile.x, tile.y, tile.get_bounds()

	window = game.window.create()
	pyglet.app.run()
