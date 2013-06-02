import world

diagonal_cost=1.5

	

class AStar:

	def __init__(self, startnode, endnode):
		self.orig = startnode
		self.dest = endnode
		# key: node pos/id, value: (node, f, g, h, predecessor)
		self.closed = {}
		# same here
		self.open = {startnode.ID:(startnode,0, 0, 0, None)}
		self.path=None
	
	def result(self):
		if self.path:
			return self.path
		if len(self.open)>0:
			self.search()
		return self.path
	
	# perform one step of search (handle best tile from openen list)
	def search(self):
		# retrieve tile with best estimated cost from open list
		node = sorted(self.open.values(), key=lambda x:x[1])[0]
		tile=node[0]
		del self.open[tile.ID]
		self.closed[tile.ID] = node
		# arrival?
		if tile == self.dest:
			path=[]
			n = self.closed[tile.ID]
			while n:
				path.append(n[0])
				n = n[4]
			self.path = reversed(path)
			return
		# if not yet arrived at destination, proceed:
		# for all neighbours of that tile
		for dir, neighbour in tile.neighbours.items():
			g = node[2]+[1,diagonal_cost][len(dir)-1]
			g *= 1+2/(neighbour.walkability+tile.walkability)
			g += neighbour.elevation-tile.elevation #TODO
			g=max(0,g)
			h=self.est_h(neighbour)
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
		# calculate number of steps diagonally and along remaining axis
		axes=sorted([abs(self.dest.x-tile.x), abs(self.dest.y-tile.y)])
		diag=axes[0]
		straight=axes[1]-axes[0]
		walkability=(tile.walkability+self.dest.walkability)/2
		slope=self.dest.elevation-tile.elevation
		return (diag*diagonal_cost+straight)*(1+1/walkability)+slope


def find_path(startnode, endnode):
	"""Returns a fresh instance of the AStar class, which
	continues to search for the best path between the given
	nodes on every call of result()"""
	return AStar(startnode, endnode)
