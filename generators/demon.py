"""
Demon - Implements the XScreenSaver "Demon".
Each frame, each cell "eats" a cell of
the previous color.
"""

import colorsys

NUMSTATES = 12

def hsv2rgb(h,s,v):
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def statefunc(s, b):
	to = (s.state + 1) % NUMSTATES
	if s.fourDirections(b).count(to) > 0:
		return to
	else:
		return s.state

STATES = [
	statefunc for x in range(NUMSTATES)
]
COLORS = [
	hsv2rgb(i / 360, 1, 1) for i in range(0, 360, 360 // len(STATES))
]
RANDSTATES = [*range(NUMSTATES)]
