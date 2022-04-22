STATES = [
	lambda s, b: (s.eightDirections(b).count(1) == 3) * 1,
	lambda s, b: (s.eightDirections(b).count(1) in [2, 3]) * 1
]
COLORS = [
	(255, 255, 255),
	(0, 0, 0)
]