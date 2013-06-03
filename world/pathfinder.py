import pyglet.graphics as gfx
import pyglet.gl
import pyglet.clock

diagonal_cost=1.5


class OpenList:
	def __init__(self, startnode):
		self.nodes = {startnode.ID:(0,0,0,None)}
		self.costs = {0:[startnode.ID]}
		
	def best(self):
		cheapest = min(self.costs.keys())
		cheapest_nodes = self.costs.get(cheapest)
		node = cheapest_nodes[0]
		#TODO
	
	def put(self, (node, f, g, h, pred)):
		#TODO
		pass
		
		

class AStar:

	running = []

	def __init__(self, startnode, endnode):
		self.orig = startnode
		self.dest = endnode
		# key: node pos/id, value: (node, f, g, h, predecessor)
		self.closed = {}
		# same here
		self.open = {startnode.ID:(startnode,0, 0, 0, None)}
		self.steps=0
		self.path=None
		# rendering for debugging
		self.batch=None
		AStar.running.append(self)
		print 'Number of active path searches:', len(AStar.running)
	
	# perform one iteration in each currently active search
	@staticmethod
	def perform(self):
		for search in AStar.running:
			if len(search.open)>0:
				search.search()
	
	def isRunning(self):
		return len(self.open)>0 and self.path==None
	
	def result(self):
		# TODO: save cost in path itself?
		if self.path:
			return self.path
		#if len(self.open)>0:
			#self.search()
		return None
	
	def draw(self):
		if self.path:
			if not self.batch:
				self.batch = gfx.Batch()
				coords = []
				for n in self.path:
					coords += n.pos
				self.batch.add_indexed(len(self.path), pyglet.gl.GL_LINES, None,
					[j for i in range(len(self.path)-1) for j in range(i,i+2)],
					('v2i', tuple(coords)),
					('c3B', (255,0,0)*len(self.path)))
				print coords
			self.batch.draw()
	
	# performs termination stuff, like rebuilding the resulting
	# shortest path, ending at destination point and map tile
	# around which destination has been discovered, and removing
	# this pathfinder instance from list of running searches
	def terminate(self, tile):
		print 'Found path! (after', self.steps, 'steps). length:',
		# remove from list of running searches
		AStar.running.remove(self)
		# rebuild path from behind
		path=[self.dest]
		n = self.closed[tile.ID]
		while n:
			path.append(n[0])
			n = n[4]
		# turn path around
		path.reverse()
		self.path=path
		print len(self.path)
		print AStar.running
					
	# perform one step of search (handle best tile from openen list)
	def search(self):
		self.steps+=1
		# retrieve tile with best estimated cost from open list
		# TODO: can this be optimized?
		node = sorted(self.open.values(), key=lambda x:x[1])[0]
		tile=node[0]
		del self.open[tile.ID]
		self.closed[tile.ID] = node
		# for all neighbours of that tile
		for direction, neighbour in tile.neighbours.items():
			# arrival?
			if neighbour == self.dest:
				self.terminate(tile)
				return
			# unless destination is reached, go on
			dist = [20,20*diagonal_cost][len(direction)-1]
			g = self.cost_between(tile, neighbour, dist=dist)
			g = max(20,g)+node[2]
			h = self.est_h(neighbour)
			if neighbour.ID in self.closed:
				if self.closed[neighbour.ID][2] > g:
					self.closed[neighbour.ID] = (neighbour, g+h, g, h, node)
			elif neighbour.ID in self.open:
				if self.open[neighbour.ID][2] > g:
					self.open[neighbour.ID] = (neighbour, g+h, g, h, node)
			else:
				self.open[neighbour.ID] = (neighbour, g+h, g, h, node)
	
	# estimate cost for shortest possible path from a node to the target node
	def est_h(self, tile):
		return self.cost_between(tile, self.dest)

	# calculates the cost of getting from a to b
	# on basis of an optionally given distance
	def cost_between(self, a, b, dist=None):
		if not dist:
			# calculate number of steps diagonally and along remaining axis
			axes = sorted([abs(b.x-a.x), abs(b.y-a.y)])
			diag = axes[0]
			straight = axes[1]-axes[0]
			dist = straight + diag*diagonal_cost
		# consider average walkability of test node and destination
		walkability = 1+2/(a.walkability+b.walkability)
		# consider elevation gap between test node and destination
		slope = b.elevation - a.elevation
		return 20*dist * walkability + slope*10
	

def find_path(startnode, endnode):
	"""Returns a fresh instance of the AStar class, which
	continues to search for the best path between the given
	nodes on every call of result()"""
	return AStar(startnode, endnode)

pyglet.clock.schedule_interval(AStar.perform, .1)
