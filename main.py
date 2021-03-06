import pygame
import random
import threading
import importlib
import ui
import os

gen = []
for g in os.listdir("generators"):
	if g == "__pycache__": continue
	gen.append(g[:-3])

def getDetails(g):
	f = open("generators/" + g + ".py", "r")
	f.readline()
	r = f.readline()
	for i in range(10):
		n = f.readline()
		if n == "\"\"\"\n": break
		r += n
	f.close()
	return r[:-1]

def selectgenerator():
	while True:
		g = ui.menu("Select a generator", gen)
		if g == -1: exit()
		g = gen[g]
		details = getDetails(g)
		#confirm = ui.listmenu(g, ["", *details.split("\n"), "", "Go >", "< Back"]) == len(details.split("\n")) + 2
		confirm = ui.listmenu(lambda x: [ui.Header(g), ui.Text(""), *[ui.Text(t) for t in details.split("\n")], ui.Text(""), ui.Button("Go >").addclick(lambda: x(True)), ui.Button("< Back").addclick(lambda: x(False))])
		if confirm: return g

class Cell:
	exists: bool = True
	def __init__(self):
		self.state: int = random.choice(RANDSTATES)
		self.index = None
	def transform(self, dir: "tuple[int, int]", board: "list | None" = None):
		if board == None: board = BOARD
		pos = [*findCellIndex(self, board)]
		pos[0] += dir[0]
		pos[1] += dir[1]
		if insideBoard(*pos):
			return board[pos[0]][pos[1]]
		else: return NullCell()
	def up(self, board: "list | None" = None) -> int: return self.transform((0, -1), board)
	def down(self, board: "list | None" = None) -> int: return self.transform((0, 1), board)
	def left(self, board: "list | None" = None) -> int: return self.transform((-1, 0), board)
	def right(self, board: "list | None" = None) -> int: return self.transform((1, 0), board)
	def fourDirections(self, board: "list | None" = None):
		if board == None: board = BOARD
		r = CellGroup()
		if self.up(board).exists: r.add(self.up(board))
		if self.down(board).exists: r.add(self.down(board))
		if self.left(board).exists: r.add(self.left(board))
		if self.right(board).exists: r.add(self.right(board))
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
	if c.index: return c.index
	if board == None: board = BOARD
	for x in range(BOARDSIZE[0]):
		try:
			c.index = (x, board[x].index(c))
			return (x, board[x].index(c))
		except ValueError: pass
	raise ValueError("Cell not in board!")

def next_frame():
	"""Switches to the next frame of the game"""
	global BOARD
	global BOARDCACHES
	preload_frame()
	if len(BOARDCACHES) == 0: return
	# Load the next frame from cache
	BOARD = BOARDCACHES.pop(0)

def cache_frame():
	"""Generates and caches the next frame of the game"""
	global BOARDCACHES
	global BOARD
	global preloading
	global board_modified
	oldboard = BOARD
	if len(BOARDCACHES) != 0: oldboard = BOARDCACHES[-1]
	newBoard = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			newBoard[x][y].state = oldboard[x][y].run(oldboard)
	if not board_modified:
		for i in BOARDCACHES:
			if [[c.state for c in row] for row in i] == [[c.state for c in row] for row in newBoard]:
				preloading = False
				return
		BOARDCACHES.append(newBoard)
	board_modified = False
	preloading = False
	preload_frame() # Start preloading if we aren't already

def preload_frame():
	"""Asyncronously generates and caches the next frame of the game"""
	global preloading
	if preloading: return # Already preloading
	preloading = True
	if not running: preloading = False
	if len(BOARDCACHES) >= 200: preloading = False
	if not preloading: return
	t = threading.Thread(target=cache_frame, name="next_frame", args=[])
	t.start()

# INITIALIZATION -----------------------------------------------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
pygame.font.init()
FONT = pygame.font.SysFont("monospace", 16)
FONTHEIGHT = FONT.render("0", True, BLACK).get_height()

CELLSIZE = 15
BOARDSIZE = (49, 49)
def insideBoard(x: int, y: int) -> bool: return x >= 0 and x < BOARDSIZE[0] and y >= 0 and y < BOARDSIZE[1]
SCREENSIZE = [BOARDSIZE[0] * CELLSIZE, (BOARDSIZE[1] * CELLSIZE) + FONTHEIGHT]
screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
ui.init(screen, pygame.font.SysFont(pygame.font.get_default_font(), 30))
v = importlib.import_module("generators." + selectgenerator())
COLORS, STATES, RANDSTATES = v.COLORS, v.STATES, v.RANDSTATES
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
BOARD = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
BOARDCACHES = []
board_modified = False

running = True
preloading = False
preload_frame()
clicknum = None

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
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			x, y = pos[0] // CELLSIZE, pos[1] // CELLSIZE
			if x < BOARDSIZE[0] and y < BOARDSIZE[1]:
				# clicked a cell!
				clicknum = (BOARD[x][y].state + 1) % len(STATES)
				BOARD[x][y].state = clicknum
				BOARDCACHES = []; board_modified = False # Reset the cache
		elif event.type == pygame.MOUSEMOTION:
			pos = pygame.mouse.get_pos()
			x, y = pos[0] // CELLSIZE, pos[1] // CELLSIZE
			if x < BOARDSIZE[0] and y < BOARDSIZE[1]:
				# Hovering over a cell!
				if clicknum:
					BOARD[x][y].state = clicknum
					BOARDCACHES = []; board_modified = False # Reset the cache
		elif event.type == pygame.MOUSEBUTTONUP:
			clicknum = None
	# Draw the board
	keys = pygame.key.get_pressed()
	if keys[pygame.K_z]: next_frame()
	screen.fill(GRAY) # Background
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			cellrect = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
			cell = BOARD[x][y]
			pygame.draw.rect(screen, COLORS[cell.state], cellrect)
			pygame.draw.rect(screen, BLACK, cellrect, 1)
	# Cache text and flip the screen
	cachetext = FONT.render("Cached frames: " + str(len(BOARDCACHES)), True, BLACK)
	screen.blit(cachetext, (0, SCREENSIZE[1] - cachetext.get_height()))
	pygame.display.flip()
	c.tick(60)
