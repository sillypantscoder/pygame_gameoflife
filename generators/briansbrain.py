STATES = [
	lambda s, b: (s.eightDirections(b).count(1) == 2) * 1,
	lambda s, b: 2,
    lambda s, b: 0
]
COLORS = [
	(255, 255, 255),
	(0, 0, 0),
    (0, 0, 255)
]