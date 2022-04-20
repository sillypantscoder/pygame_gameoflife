import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Cell:
	exists: bool = True
	def __init__(self):
		self.state: int = random.choice([0, 1])
	def up(self):
		pos = findCellIndex(self)
		try:
			return BOARD[pos[0]][pos[1] - 1]
		except: return NullCell()
	def down(self):
		pos = findCellIndex(self)
		try:
			return BOARD[pos[0]][pos[1] + 1]
		except: return NullCell()
	def left(self):
		pos = findCellIndex(self)
		try:
			return BOARD[pos[0] - 1][pos[1]]
		except: return NullCell()
	def right(self):
		pos = findCellIndex(self)
		try:
			return BOARD[pos[0] + 1][pos[1]]
		except: return NullCell()
	def fourdirections(self):
		r = CellGroup()
		if self.up().exists: r.add(self.up())
		if self.down().exists: r.add(self.down())
		if self.left().exists: r.add(self.left())
		if self.right().exists: r.add(self.right())
		return r
	def eightDirections(self):
		r = CellGroup()
		if self.up().exists: r.add(self.up())
		if self.down().exists: r.add(self.down())
		if self.left().exists: r.add(self.left())
		if self.right().exists: r.add(self.right())
		if self.up().left().exists: r.add(self.up().left())
		if self.up().right().exists: r.add(self.up().right())
		if self.down().left().exists: r.add(self.down().left())
		if self.down().right().exists: r.add(self.down().right())
		return r
	def run(self):
		return STATES[self.state](self)

class CellGroup:
	def __init__(self):
		self.items: list[Cell] = []
	def add(self, c: Cell): self.items.append(c)
	def count(self, state: int):
		count = 0
		for c in self.items:
			if c.state == state: count += 1
		return count

class NullCell:
	exists: bool = False
	def __init__(self): self.state: int = 0
	def up(self): return NullCell()
	def down(self): return NullCell()
	def left(self): return NullCell()
	def right(self): return NullCell()

def findCellIndex(c: Cell) -> "tuple[int, int]":
	for x in range(BOARDSIZE[0]):
		try:
			return (x, BOARD[x].index(c))
		except ValueError: pass

STATES = [
	lambda s: (s.eightDirections().count(1) == 3) * 1,
	lambda s: (s.eightDirections().count(1) in [2, 3]) * 1
]
SCREENSIZE = [500, 500]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
BOARDSIZE = (20, 20)
BOARD = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
CELLSIZE = 10

def next_frame():
	global BOARD
	newBoard = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			newBoard[x][y].state = BOARD[x][y].run()
	BOARD = newBoard

c = pygame.time.Clock()
running = True
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
	screen.fill(WHITE)
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			cellrect = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
			cell = BOARD[x][y]
			if cell.state == 1:
				pygame.draw.rect(screen, BLACK, cellrect)
	pygame.display.flip()
	c.tick(60)
