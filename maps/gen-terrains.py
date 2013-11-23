#!/usr/bin/python


# generate csv repr for given tile terrain configuration
def tidx(g, w):
	res = [0]*4
	for b in range(4):
		if w >> b & 1:
			res[b] = 2
		elif g >> b & 1:
			res[b] = 1
	res = res[:2] + res[2:][::-1]
	return ','.join(['{0}'.format(b) for b in res])


f=open('ground_terrains.tsx', 'w')

header=['<?xml version="1.0" encoding="UTF-8"?>',
'<tileset name="ground_terrains" tilewidth="32" tileheight="32">',
' <image source="../textures/ground.png" width="512" height="512"/>',
' <terraintypes>',
'  <terrain name="Dirt" tile="0"/>',
'  <terrain name="Grass" tile="240"/>',
'  <terrain name="Water" tile="15"/>',
' </terraintypes>']
 
f.write('\n'.join(header))

for g in range(16):
	for w in range(16):
		f.write(' <tile id="{0}" terrain="{1}"/>\n'.format(
			w+g*16, tidx(g,w)))

f.write('</tileset>\n')

f.close()
