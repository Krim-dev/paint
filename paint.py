import pygame
from tkinter import *
from tkinter.filedialog import asksaveasfilename as fileopen

pygame.init()
Tk().withdraw()

WIDTH, HEIGHT = 600, 700
SIDE_MARGIN = 200
screen = pygame.display.set_mode((WIDTH + SIDE_MARGIN, HEIGHT))
pygame.display.set_caption('Akram - Paint')

LOWER_MARGIN = HEIGHT - 100
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 40)
clear_img = pygame.image.load('clear.png').convert_alpha()
save_img = pygame.image.load('save.png').convert_alpha()
all_colors = [
	(0,0,0),
	(128, 128, 128),
	(255, 0, 0),
	(0, 255, 0), 	
	(0, 0, 255), 
	(255, 255, 0)
]

brush_size = 5
current_color = 0
TILE_SIZE = WIDTH // (len(all_colors) + 2)
text_col = (0,0,0)
# clearing - saving
clear_img = pygame.transform.scale(clear_img, (TILE_SIZE - 5, TILE_SIZE - 5))
save_img = pygame.transform.scale(save_img, (TILE_SIZE - 5, TILE_SIZE - 5))

def clear_screen():
	screen.fill((255, 255, 255))

def draw_settings():
	for x,color in enumerate(all_colors):
		pygame.draw.rect(screen, color, (1+x * TILE_SIZE, 
			LOWER_MARGIN + 5, TILE_SIZE - 5, 90))

	screen.blit(clear_img, (len(all_colors) * TILE_SIZE, 
			LOWER_MARGIN + 5))
	screen.blit(save_img, ((len(all_colors) + 1) * TILE_SIZE, 
			LOWER_MARGIN + 5))
	pygame.draw.line(screen, all_colors[0], 
			(WIDTH + 5, 0), 
			(WIDTH + 5, HEIGHT), 6)

cursor = LOWER_MARGIN - 30
def brush_change(y):
	global cursor, brush_size
	if y < 20:
		y = 20
	if y > LOWER_MARGIN:
		y = 0

	cursor = y
	brush_size = (LOWER_MARGIN - 20 - cursor) // 10

	screen.fill((255, 255, 255), 
		(WIDTH, 0, SIDE_MARGIN, HEIGHT))

clear_screen()
def draw_pipe():
	pygame.draw.line(screen, all_colors[1], 
					(WIDTH + SIDE_MARGIN // 2, 20),
					(WIDTH + SIDE_MARGIN // 2, LOWER_MARGIN),
					8
		)
	pygame.draw.rect(screen, all_colors[1], 
					(WIDTH + SIDE_MARGIN // 2 - 10, cursor,
					20, 20
					)
		)

run = True
while run:
	pressed = pygame.mouse.get_pressed()
	if pressed[0]:
		pos = pygame.mouse.get_pos()
		if pos[0] > WIDTH - brush_size:
			brush_change(pos[1])
		elif pos[1] < LOWER_MARGIN:
			pygame.draw.rect(screen, 
				all_colors[current_color],
				(pos[0] - brush_size, pos[1] - brush_size,
				brush_size * 2, brush_size * 2)
				)
		else:
			idx = pos[0] // TILE_SIZE
			if idx < len(all_colors):
				current_color = idx
			else:
				if idx == WIDTH // TILE_SIZE - 2:
					clear_screen()
				else:
					temp = screen.subsurface(0, 0,WIDTH, LOWER_MARGIN)
					path = ''
					try:
						path = fileopen(
							defaultextension='.png', filetypes=[('All Files', '*.*'),("png files", '*.png'), ('Jpeg files', '*.jpg')],
							initialdir='C:/Pictures',
							title="Choose filename")
					except:
						pass
					pygame.image.save(temp, path) # maybe dynamicly store the images

	if pressed[2]:
		pos = pygame.mouse.get_pos()
		if pos[1] < LOWER_MARGIN:
			pygame.draw.rect(screen,
				(255, 255, 255),
				(pos[0] - brush_size, pos[1] - brush_size,
				brush_size * 2, brush_size * 2)
				)
	draw_settings()
	draw_pipe()
	# draw_text()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.flip()