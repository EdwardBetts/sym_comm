#/usr/bin/python

from PIL import Image as pil
from random import random as rnd


adj = [(-1,-1),(0,-1),(1,-1),
			 (-1,0),        (1,0),
			 (-1,1), (0,1), (1,1)]

def neighbours(x,y):
	nn = [(x+nx,y+ny) for nx,ny in adj if
				x+nx in range(32) and y+ny in range(32)]
	return nn

# generate bit mask
def mask(i):
	cns = [float(i >> b & 1) for b in range(4)]
	mask = [[cns[0]*rnd()]*16 + [cns[1]*rnd()]*16 
					for i in range(16)]
	mask+= [[cns[3]*rnd()]*16 + [cns[2]*rnd()]*16 
					for i in range(16)]
	# noise
	for i in range(10):
		copy = [row[:] for row in mask]
		for y in range(32):
			row = mask[y]
			for x in range(32):
				nn = neighbours(x,y)
				v = sum([copy[yy][xx] for xx,yy in nn]+[copy[y][x]])
				v /= len(nn)+1
				row[x] = v*(.5+rnd())
	mask = [[min(1,v) for v in row] for row in mask]
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
		r = 150+rnd()*70
		g = r-30+rnd()*50
		b = 100+rnd()*10
	elif ground<2: # grass
		g = 160+rnd()*80
		r = g*(.8+rnd()/4)
		b = g*(.7+rnd()/5)
	else:
		b = 130+rnd()*70
		g = b*(.6+rnd()/5)
		r = g*(.5+rnd()/10)
	return (int(r), int(g), int(b))
	

# draw overlay:
def blitt(x,y):
	m = mask(y) # grass
	for 

# init
img = pil.new('RGB', (512,512), 'black')
pix = img.load()
for x in range(512):
	for y in range(512):
		pix[x,y] = col(0)

# generate texture:
for y in range(16):
	for x in range(16):
		blitt(x,y)
