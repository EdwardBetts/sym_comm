#/usr/bin/python

from PIL import Image as pil
from random import random as rnd, choice


adj = [(-1,-1),(0,-1),(1,-1),
			 (-1,0),        (1,0),
			 (-1,1), (0,1), (1,1)]

corners = lambda i: [i >> b & 1 for b in range(4)]

neighbours = {}
for x in range(32):
	for y in range(32):
		nn = [(x+nx,y+ny) for nx,ny in adj if
					x+nx in range(32) and y+ny in range(32)]
		neighbours[(x,y)] = nn

# generate bit mask
def mask(i):
	cns = corners(i)
	mask = [[cns[0]]*16 + [cns[1]]*16 
					for i in range(16)]
	mask+= [[cns[3]]*16 + [cns[2]]*16 
					for i in range(16)]
	# noise
	#noise=lambda n: n/(n+6.) + rnd()*11./(n+6)
	noise=lambda n: 1.+(-.45+rnd())/(1+i/10)
	for i in range(3,12):
		copy = [row[:] for row in mask]
		for y in range(32):
			row = mask[y]
			for x in range(32):
				nn = neighbours[(x,y)]
				v = sum([copy[yy][xx] for xx,yy in nn]+[copy[y][x]])
				v /= len(nn)+1
				row[x] = v*noise(i)
	mask = [[min(1.,v**2) for v in row] for row in mask]
	return mask

# text output
def print_mask(mask):
	for row in mask:
		print ' '.join([' .,-:;%'[int(v*5)] for v in row])


# generate and show
def do(i):
	print_mask(mask(i))

# ground = 0,1,2: dirt, grass, water
def col(ground):
	if ground<1: # dirt
		r = 80+rnd()*40
		g = r-30*rnd()
		b = g/2+rnd()*20
	elif ground<2: # grass
		g = 120+rnd()*60
		r = g*(.6+rnd()/4)
		b = g*(.25+rnd()/6)
	else: # water
		b = 80+rnd()*40
		g = b*(.5+rnd()/5)
		r = g*(.3+rnd()/10)
	return (int(r), int(g), int(b))
	
# mix two colors
def blend(c1, c2, pan):
	com = zip(c1, c2)
	col = [t[0]*pan+t[1]*(1-pan) for t in com]
	return tuple([int(col[c]) for c in range(3)])

# pick prepared bit masks for index
def bmask(i):
	return choice(mreg[i])

# draw overlay:
def blitt(i,j):
	#print ''.join(['{}'.format(c) for c in corners(i)]),
	#print ''.join(['{}'.format(c) for c in corners(j)])
	# j = grass, i = water
	for ground, m in enumerate([bmask(j), bmask(i)]):
		for y,row in enumerate(m):
			for x,v in enumerate(row):
				if v > .2:
					xx=i*32+x
					yy=j*32+y
					pix[xx,yy] = blend(col(ground+1), pix[xx,yy], v)

def gettex(grass, water):
	return img.crop((water*32,grass*32,water*32+32,grass*32+32))

# init
img = pil.new('RGB', (1024,1024), 'black')
pix = img.load()
print 'prepare dirt layer'
for x in range(1024):
	for y in range(1024):
		pix[x,y] = col(0)
img = img.resize((512,512), pil.ANTIALIAS)
pix = img.load()

print 'populate bitmask tables..'
mreg = []
for i in range(16):
	print corners(i)
	mreg.append([mask(i) for j in range(5)])

# generate texture:
print 'start generating'
for j in range(16):
	print '{:.2f}%'.format(100.*j/16)
	for i in range(16):
		blitt(i,j)
print

#img.show()
img.save('grounds.png')

bck=pil.new('RGB', (256,256), 'black')

# i, j, grass, water
land = [(2,4,0,1), (3,4,4,0), (4,4,12,0), (5,4,8,0),
				(2,5,4,0), (3,5,14,0),(4,5,11,4), (5,5,1,8),
				(2,6,6,8), (3,6,11,0),(4,6, 5,2), (5,6,8,1),
				(2,7,6,1), (3,7,13,0),(4,7,10,0), (5,7,1,0)
				]

for i, j, g, w in land:
	tex = gettex(g,w)
	bck.paste(tex,(i*32,j*32))

bck.save('land.png')
#bck.show()

