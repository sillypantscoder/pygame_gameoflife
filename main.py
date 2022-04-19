import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREENSIZE = [500, 500]
screen = pygame.display.set_mode(SCREENSIZE)
BOARDSIZE = (80, 80)
BOARD = [[random.choice([0, 1]) for x in range(BOARDSIZE[0])] for y in range(BOARDSIZE[1])]
CELLSIZE = 10

c = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	screen.fill(WHITE)
	for x in range(BOARDSIZE[0]):
		for y in range(BOARDSIZE[1]):
			cellrect = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
			cell = BOARD[x][y]
			if cell == 1:
				pygame.draw.rect(screen, BLACK, cellrect)
	pygame.display.flip()
	c.tick(60)
