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
	
	# perform one step of search (handle best tile from openen list)
	def seek(self):
		# retrieve tile with best estimated cost from open list
		node = sorted(self.open.values(), key=lambda x:x[1])[-1]
		tile=node[0]
		del self.open[tile.ID]
		# for all neighbours of that tile
		for dir, neighbour in tile.neighbours.items():
			g = node[2]+[1,diagonal_cost][len(dir)-1]
			g *= 1+2/(neighbour.walkability+tile.walkability)
			g += neighbour.elevation-tile.elevation #TODO
			g=max(0,g)
			h=est_h(neighbour)
			if neighbour.ID in self.closed:
				if self.closed[neighbour.ID][2] > g:
					self.closed[neighbour.ID] = (neighbour, g+h, g, h, tile)
			elif neighbour.ID in self.open:
				if self.open[neighbour.ID][2] > g:
					self.open[neighbour.ID] = (neighbour, g+h, g, h, tile)
			else:
				self.open[neighbour.ID] = (neighbour, g+h, g, h, tile)
	
	
	# estimate cost for shortest possible path from a node to the target node
	def est_h(self, tile):
		# calculate number of steps diagonally and along remaining axis
		axes=sorted([abs(self.endnode.x-tile.x), abs(self.endnode.y-tile.y])
		diag=axes[0]
		straight=axes[1]-axes[0]
		walkability=(tile.walkability+self.endnode.walkability)/2
		slope=self.endnode.elevation-tile.elevation
		return (diag*diagonal_cost+straight)*(1+1/walkability)+slope
