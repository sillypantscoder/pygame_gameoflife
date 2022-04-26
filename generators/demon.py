"""
Demon - Implements the XScreenSaver "Demon".
Each frame, each cell "eats" a cell of
the previous color.
"""

import colorsys

NUMSTATES = 12

def hsv2rgb(h,s,v):
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def getStateFunc(x):
	def func(s, b):
		if s.fourDirections(b).count((x + 1) % NUMSTATES) > 0:
			return ((x + 1) % NUMSTATES)
		else:
			return x
	return func

STATES = [
	getStateFunc(x)
		for x in range(NUMSTATES)
]
COLORS = [
	hsv2rgb(i / 360, 1, 1) for i in range(0, 360, 360 // len(STATES))
]
