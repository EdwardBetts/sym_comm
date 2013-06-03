import pyglet.graphics as gfx
import pyglet.gl
import pyglet.clock

diagonal_cost=1.5

# reminder: F, G and H of a node N mean:
# G = cheapest known total cost of walking from startpoint to N
# H = estimated cost of walking from N to destination point
# F = G + H = estimated total cost of complete path via N

class OpenList:
	def __init__(self, startnode):
		# directory of open nodes, storing the node itself,
		# cost values f, g, h and the node's predecessor
		# under the node's ID
		self.nodes = {startnode.ID:(startnode,0,0,0,None)}
		# directory of current cost values (f) and the nodes
		# available at these costs. For fast estimation of
		# the currently cheapest known node
		self.costs = {0:[startnode.ID]} 
		#TODO: single candidate instead of list? 
		# (never more than 1 element anyway)
	
	def best(self):
		# TODO: maintain cheapest f instead of calculating min?
		cheapest = min(self.costs.keys())
		cheapest_nodes = self.costs.get(cheapest)
		if len(cheapest_nodes)>1:
			print cheapest_nodes
		ID = cheapest_nodes.pop(0)
		node = self.nodes.pop(ID)
		if len(cheapest_nodes)<1:
			self.costs.pop(cheapest)
		return node
	
	def put(self, (node, f, g, h, pred)):
		# TODO: cheat a bit by not storing nodes that are ridiculously
		# expensive?
		self.nodes[node.ID] = (node, f, g, h, pred)
		# try to retrieve list of nodes available for cost value f
		nodes_for_cost = self.costs.get(f, None)
		if not nodes_for_cost:
			self.costs[f] = [node.ID]
		else:
			nodes_for_cost.append(node.ID)
	
	def update(self, (node, f, g, h, pred)):
		old_cost = self.nodes.get(node.ID)[1]
		self.nodes[node.ID] = (node, f, g, h, pred)
		self.costs.get(old_cost).remove(node.ID)
		if len(self.costs.get(old_cost))<1:
			self.costs.pop(old_cost)
		nodes_for_cost = self.costs.get(f, None)
		if not nodes_for_cost:
			self.costs[f] = [node.ID]
		else:
			nodes_for_cost.append(node.ID)
	
	def get(self, node):
		return self.nodes.get(node.ID, None)
	
	def isOpen(self, node):
		return node.ID in self.nodes
	
	def __len__(self):
		return len(self.nodes)
		
# class for performing an A* path search between a startnode
# and an endnode. Instances of this class are automatically
# called for a single iteration step multiple times per second.
class AStar:
	running = []
	def __init__(self, startnode, endnode):
		self.orig = startnode
		self.dest = endnode
		# key: node pos/id, value: (node, f, g, h, predecessor)
		self.closed = {}
		# same here
		self.open = OpenList(startnode)
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
		#print AStar.running
					
	# perform one step of search (handle best tile from openen list)
	def search(self):
		self.steps+=1
		# retrieve tile with best estimated cost from open list
		node = self.open.best()
		tile=node[0]
		self.closed[tile.ID] = node
		# arrival?
		if tile == self.dest:
			self.terminate(tile)
			return
		# for all neighbours of that tile
		for direction, neighbour in tile.neighbours.items():
			if not neighbour.ID in self.closed:
				dist = [20,20*diagonal_cost][len(direction)-1]
				g = self.cost_between(tile, neighbour, dist=dist)
				#g = max(20,g)+node[2]
				g += node[2]
				h = self.est_h(neighbour)
				if self.open.isOpen(neighbour):
					if self.open.get(neighbour)[2] > g:
						self.open.update((neighbour, g+h, g, h, node))
				else:
					self.open.put((neighbour, g+h, g, h, node))
	
	# estimate cost for shortest possible path from a node to the target node
	def est_h(self, tile):
		return self.cost_between(tile, self.dest)

	# calculates the cost of getting from a to b
	# on basis of an optionally given distance
	# TODO: move to tile map module?
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
		if dist>0:
			slope /= dist
		# make climbing a hill more hard than going it down is easy
		# to get finder to avoid crossing hills
		if slope>0:
			slope*=10
		return max(20*dist, 20*dist * walkability + slope*10)
	

def find_path(startnode, endnode):
	"""Returns a fresh instance of the AStar class, which
	continues to search for the best path between the given
	nodes on every call of result()"""
	return AStar(startnode, endnode)

pyglet.clock.schedule_interval(AStar.perform, .025)
