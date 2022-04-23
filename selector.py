import pygame
import math

pygame.font.init()

FONT = pygame.font.SysFont(pygame.font.get_default_font(), 40)
FONTHEIGHT = FONT.render("0", True, (0, 0, 0)).get_height()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def selector(header, items: list):
	global screen
	scrn_height = 500
	scrn_width = 500
	if FONTHEIGHT * (len(items) + 1) > 500:
		scrn_height = FONTHEIGHT * (len(items) + 1)
	for i in items:
		w = FONT.render(i, True, BLACK)
		if w.get_width() > scrn_width:
			scrn_width = w.get_width()
	screen = pygame.display.set_mode([scrn_width, scrn_height])
	running = True
	c = pygame.time.Clock()
	while running:
		pos = pygame.mouse.get_pos()
		screen.fill(WHITE)
		# Header
		pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, scrn_width, FONTHEIGHT))
		w = FONT.render(header, True, WHITE)
		screen.blit(w, (0, 0))
		# Items
		h = 0
		for i in items:
			h += FONTHEIGHT
			w = FONT.render(i, True, BLACK)
			if math.floor(pos[1] / FONTHEIGHT) * FONTHEIGHT == h:
				w = FONT.render(i, True, WHITE)
				pygame.draw.rect(screen, BLACK, pygame.Rect(0, h, scrn_width, FONTHEIGHT))
			screen.blit(w, (0, h))
		# Events
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return -1
					# User clicked close button
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if pos[1] - FONTHEIGHT < len(items) * FONTHEIGHT:
						return math.floor((pos[1] - FONTHEIGHT) / FONTHEIGHT)
		c.tick(60)
		pygame.display.flip()

def progress(text):
	global screen
	rendered = FONT.render(text, True, BLACK)
	scrn_height = rendered.get_height() + 10
	scrn_width = rendered.get_width() + 10
	screen = pygame.display.set_mode([scrn_width, scrn_height], pygame.RESIZABLE)
	running = text
	while running:
		rendered = FONT.render(running, True, BLACK)
		screen.fill(WHITE)
		if scrn_height < rendered.get_height() + 10:
			scrn_height = rendered.get_height() + 10
			screen = pygame.display.set_mode([scrn_width, scrn_height], pygame.RESIZABLE)
		if scrn_width < rendered.get_width() + 10:
			scrn_width = rendered.get_width() + 10
			screen = pygame.display.set_mode([scrn_width, scrn_height], pygame.RESIZABLE)
		# Events
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return;
					# User clicked close button
				elif event.type == pygame.VIDEORESIZE:
					scrn_height = event.h
					scrn_width = event.w
					screen = pygame.display.set_mode([scrn_width, scrn_height], pygame.RESIZABLE)
		# Header
		screen.blit(rendered, ((scrn_width - rendered.get_width()) / 2, (scrn_height - rendered.get_height()) / 2))
		pygame.display.flip()
		running = yield;
