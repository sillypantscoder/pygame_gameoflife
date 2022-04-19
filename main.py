import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Cell:
	def __init__(self):
		self.state: int = random.choice([0, 1])
	def up(self):
		pos = findCellIndex(self)
		print(pos)
		try:
			return BOARD[pos[0]][pos[1] - 1]
		except: return NullCell()

class NullCell:
	def __init__(self): self.state: int = 0
	def up(self): return NullCell()

def findCellIndex(c: Cell) -> "tuple[int, int]":
	for x in range(BOARDSIZE[0]):
		try:
			return (x, BOARD[x].index(c))
		except ValueError: pass

SCREENSIZE = [500, 500]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
BOARDSIZE = (80, 80)
BOARD = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
CELLSIZE = 10

def next_frame():
	global BOARD
	newBoard = [[Cell() for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			newBoard[x][y].state = BOARD[x][y].up().state
			print(BOARD[x][y].up, BOARD[x][y].up())
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
