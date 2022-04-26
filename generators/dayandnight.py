"""
Day & Night - A "symmetrical" cellular
automaton. https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton)
"""

STATES = [
	lambda s, b: (s.eightDirections(b).count(1) in [3, 6, 7, 8]) * 1,
	lambda s, b: (s.eightDirections(b).count(1) in [3, 4, 6, 7, 8]) * 1
]
COLORS = [
	(0, 0, 0),
	(255, 255, 0)
]
RANDSTATES = [0, 1]
