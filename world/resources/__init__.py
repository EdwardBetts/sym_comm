

keywords={'resource': {
	'id': True,
	'name': False,
	'image': True,
	'effect': {
		'on': True,
		'size': True, 
		'dependency': False,
		},
	'grow': {
		'vegetation': {
			'min': False,
			'max': False,
		},
		'water': {
			'min': False,
			'max': False,
		},
		'adjacent': {
			'vegetation': {
				'min': False,
				'max': False,
				'number': {
					'min': False,
					'max': False,
				},
			},
			'water': {
				'number': {
					'min': False,
					'max': True
				}
			},
			'resource': {
				'id': True,
				'number': {
					'min': False,
					'max': True						
				}
			}
		}
	}
}}


def load(filename):

	f = open(filename, 'ro')

	resource = []
	context = [('resource', keywords['resource'])]


	for line in f:

		entry = line.split(':')
		keyword = entry[0]
		depth = keyword.count('\t')+1
		keyword = keyword.strip()
		#print context
		print '/'.join([node[0] for node in context]), keyword

		if depth < len(context):
#			print "%d < %d" % (depth, len(context))
			while len(context)>depth:
				context.pop()
			print "going up on level ", len(context), ": "
			resource.append('')
#			print context[-1][0], '.'

#			print '/'.join([node[0] for node in context]), keyword



		if keyword in context[-1][1]:
			keyf = type(context[-1][1].get(keyword, None))
			if keyf is bool:
				resource.append(('.'.join([node[0] 
					for node in context] + [keyword]), 
					entry[1].strip()) 
				)
#				print resource[-1]
						
			elif keyf is dict:
#				print "enter context: ", keyword, context[-1][1][keyword]
				context.append(
					(keyword, context[-1][1][keyword])
				)
			else:
				print "neither attribute nor category?", keyf
		else:
			print "unknown keyword: ", keyword
			print "known: ", context[-1][1].keys()


	for e in resource:
		print e

		# if keyf is bool:
		# 	if depth == len(path):
		# 		if keywords[path[-1]].get(keyword, None):
		# 			context[-1][keyword] = entry[1]
		# elif keyf is dict:
		# 	if keyword in keywords[path[-1]]:
		# 		path.append(keyword)
		# 		context[-1][keyword] = [{}]
		# 		context.append(context[-1][keyword][0])
		# 	elif keyword == path[-1]:
		# 		context[-1][keyword].append({})
		# 		context.append(context[-1][keyword][-1])
		# 	else:
		# 		while len(path)>1:
		# 			up=path.pop()
		# 			if keyword in context.pop()



def test():
	load("world/resources/base")