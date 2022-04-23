import random

offstates = random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8], weights=[4, 4, 4, 4, 3, 3, 2, 1, 0.5], k=random.choice([1, 2, 3, 4]))
offstates = list(set(offstates)) # Remove duplicates
print("Off states:", offstates)

onstates = random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8], weights=[4, 4, 4, 4, 3, 3, 2, 1, 0.5], k=random.choice([1, 2, 3, 4]))
onstates = list(set(onstates)) # Remove duplicates
print("On states:", onstates)

STATES = [
	lambda s, b: (s.eightDirections(b).count(1) in offstates) * 1,
	lambda s, b: (s.eightDirections(b).count(1) in onstates) * 1
]
COLORS = [
	(255, 255, 255),
	(0, 0, 0)
]