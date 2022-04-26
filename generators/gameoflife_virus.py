def state0(cell, board):
   e = cell.eightDirections(board)
   if e.count(3) > 0: return 2
   if e.count(2) > 0 and e.count(1) > 0: return 3
   return (e.count(1) == 3) * 1

def state1(cell, board):
   e = cell.eightDirections(board)
   if e.count(2) > 0: return 2
   if e.count(1) == 8: return 2
   return (e.count(1) == 3 or e.count(1) == 2) * 1

STATES = [
	lambda s, b: state0(s, b),
	lambda s, b: state1(s, b),
	lambda s, b: 0,
	lambda s, b: 0
]
COLORS = [
	(255, 255, 255),
	(0, 0, 0),
	(255, 0, 0),
	(255, 165, 0)
]