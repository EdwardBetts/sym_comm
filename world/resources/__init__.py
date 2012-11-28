

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


class Resource(object):

	def __init__(self, rid='', name='', image='', effects=[], growOn=[]):
		self.id = rid
		self.name = name
		self.image = image
		self.effects = effects
		self.growOn = []
		
	def add_effect(effect):
		self.effects.append(effect)
		
	def add_grow_condition(condition):
		self.growOn.append(condition)


def createResourceType(conf):
	for line in conf:
		print line
	


def load(filename):

	f = open(filename, 'ro')

	resource = []
	context = [('resource', keywords['resource'])]


	for line in f:

		entry = line.split(':')
		keyword = entry[0]
		depth = keyword.count('\t')+1
		keyword = keyword.strip()

		if depth < len(context):
			while len(context)>depth:
				context.pop()

		if keyword in context[-1][1]:
			keyf = type(context[-1][1].get(keyword, None))
			if keyf is bool:
				resource.append(('.'.join([node[0] 
					for node in context] + [keyword]), 
					entry[1].strip()) 
				)
						
			elif keyf is dict:
				context.append(
					(keyword, context[-1][1][keyword])
				)
				resource.append('.'.join([node[0]
					for node in context]))
			else:
				print "neither attribute nor category?", 
				print keyword, keyf
		elif keyword == '':
			if not resource[-1] == '':
				resource.append('')			
		else:
			print "unknown keyword: ", keyword
			print "known: ", context[-1][1].keys()


	for e in resource:
		print e



def test():
	load("world/resources/base")
