import pygame
import random
import threading

class Cell:
	exists: bool = True
	def __init__(self):
		self.state: int = random.choice([0, 1])
	def up(self, board: "list | None" = None) -> int:
		if board == None: board = BOARD
		pos = findCellIndex(self, board)
		try:
			return board[pos[0]][pos[1] - 1]
		except: return NullCell()
	def down(self, board: "list | None" = None) -> int:
		if board == None: board = BOARD
		pos = findCellIndex(self, board)
		try:
			return board[pos[0]][pos[1] + 1]
		except: return NullCell()
	def left(self, board: "list | None" = None) -> int:
		if board == None: board = BOARD
		pos = findCellIndex(self, board)
		try:
			return board[pos[0] - 1][pos[1]]
		except: return NullCell()
	def right(self, board: "list | None" = None) -> int:
		if board == None: board = BOARD
		pos = findCellIndex(self, board)
		try:
			return board[pos[0] + 1][pos[1]]
		except: return NullCell()
	def fourdirections(self, board: "list | None" = None):
		if board == None: board = BOARD
		r = CellGroup()
		if self.up().exists: r.add(self.up())
		if self.down().exists: r.add(self.down())
		if self.left().exists: r.add(self.left())
		if self.right().exists: r.add(self.right())
		return r
	def eightDirections(self, board: "list | None" = None):
		if board == None: board = BOARD
		r = CellGroup()
		if self.up(board).exists: r.add(self.up(board))
		if self.down(board).exists: r.add(self.down(board))
		if self.left(board).exists: r.add(self.left(board))
		if self.right(board).exists: r.add(self.right(board))
		if self.up(board).left(board).exists: r.add(self.up(board).left(board))
		if self.up(board).right(board).exists: r.add(self.up(board).right(board))
		if self.down(board).left(board).exists: r.add(self.down(board).left(board))
		if self.down(board).right(board).exists: r.add(self.down(board).right(board))
		return r
	def run(self, board: "list | None" = None):
		if board == None: board = BOARD
		return STATES[self.state](self, board)
	def __repr__(self) -> str: return f"Cell ({self.state})"

class CellGroup:
	def __init__(self):
		self.items: list[Cell] = []
	def add(self, c: Cell): self.items.append(c)
	def count(self, state: int):
		count = 0
		for c in self.items:
			if c.state == state: count += 1
		return count
	def __repr__(self) -> str:
		return f"CellGroup ({len(self.items)} items)"

class NullCell:
	exists: bool = False
	def __init__(self): self.state: int = 0
	def up(self, board = None): return NullCell()
	def down(self, board = None): return NullCell()
	def left(self, board = None): return NullCell()
	def right(self, board = None): return NullCell()
	def __repr__(self) -> str: return "NullCell"

def findCellIndex(c: Cell, board: "list | None" = None) -> "tuple[int, int]":
	if board == None: board = BOARD
	for x in range(BOARDSIZE[0]):
		try:
			return (x, board[x].index(c))
		except ValueError: pass

def generate_frame():
	"""Generates the next frame of the game"""
	newBoard = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			newBoard[x][y].state = BOARD[x][y].run()
	return newBoard

def next_frame():
	"""Switches to the next frame of the game"""
	global BOARD
	global BOARDCACHES
	if len(BOARDCACHES) == 0:
		BOARD = generate_frame()
	else:
		BOARD = BOARDCACHES.pop(0)
	preload_frame()

def cache_frame():
	"""Generates and caches the next frame of the game"""
	global BOARDCACHES
	global BOARD
	global preloading
	oldboard = BOARD
	if len(BOARDCACHES) != 0: oldboard = BOARDCACHES[-1]
	newBoard = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			newBoard[x][y].state = oldboard[x][y].run(oldboard)
	BOARDCACHES.append(newBoard)
	preloading = False
	preload_frame() # Start preloading if we aren't already

def preload_frame():
	"""Asyncronously generates and caches the next frame of the game"""
	global preloading
	if preloading: return # Already preloading
	preloading = True
	if not running: preloading = False
	if len(BOARDCACHES) >= 100: preloading = False
	if not preloading: return
	t = threading.Thread(target=cache_frame, name="next_frame", args=[])
	t.start()

# INITIALIZATION -----------------------------------------------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
pygame.font.init()
FONT = pygame.font.SysFont("monospace", 16)

STATES = [
	lambda s, b: (s.eightDirections(b).count(1) == 3) * 1,
	lambda s, b: (s.eightDirections(b).count(1) in [2, 3]) * 1
]
SCREENSIZE = [500, 500]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
BOARDSIZE = (40, 40)
BOARD = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
CELLSIZE = 10
BOARDCACHES = []

running = True
preloading = False
preload_frame()

c = pygame.time.Clock()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.VIDEORESIZE:
			SCREENSIZE = event.size
			screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				next_frame()
	# Draw the board
	keys = pygame.key.get_pressed()
	if keys[pygame.K_z]: next_frame()
	screen.fill(GRAY) # Background
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			cellrect = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
			cell = BOARD[x][y]
			if cell.state == 0:
				pygame.draw.rect(screen, WHITE, cellrect)
			elif cell.state == 1:
				pygame.draw.rect(screen, BLACK, cellrect)
	# Cache text and flip the screen
	cachetext = FONT.render("Cached frames: " + str(len(BOARDCACHES)), True, BLACK)
	screen.blit(cachetext, (0, SCREENSIZE[1] - cachetext.get_height()))
	pygame.display.flip()
	c.tick(60)
