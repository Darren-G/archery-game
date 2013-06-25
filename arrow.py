import pygame
import math
import random

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREEN = (50,180,50)
RED = (255,0,0)
BLUE = (0,0,255)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

# Set the width and height of the screen [width, height]
size = [360,600]
width = size[0]
height = size[1]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Archery Game")

# Loop until the user clicks the close button
running = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Variables
target = pygame.image.load('target.png').convert()
target.set_colorkey(target.get_at((0,0)))
target_center = (target.get_size()[0] / 2, target.get_size()[1] / 2)
target_radius = target.get_size()[0] / 2
target_pos = (width / 2 - target_center[0], height / 2 - target_center[1])

arrow = pygame.image.load('arrow.png').convert()
arrow.set_colorkey(arrow.get_at((0,0)))
arrow_num = 4
arrow_pos = (0,0)

hit_sound = pygame.mixer.Sound('hit.wav')
miss_sound = pygame.mixer.Sound('miss.wav')
win_sound = pygame.mixer.Sound('tada.wav')

enemy_pos = (random.randrange(target_radius, width - target.get_size()[0]) - target_center[0], random.randrange(target_radius, height - target.get_size()[1]) - target_center[1])
print enemy_pos
enemy_display = False

hit_list = []

playing = False

# - - - Main Program Loop - - -
while running == True:
	# - - - STEP 1: Event Processing - - -
	for event in pygame.event.get(): # User did something!
		if event.type == pygame.QUIT: # User clicked close
			running = False # End Program Loop
		elif event.type == pygame.MOUSEMOTION:
			if not playing:
				if event.pos[0] > target_center[0] and event.pos[1] > target_center[1]:
					if event.pos[0] < width - target_center[0] and event.pos[1] < height - target_center[1]:
						target_pos = (event.pos[0] - target_center[0], event.pos[1] - target_center[1])
			else:
				arrow_pos = event.pos
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if not playing:
				playing = True
			else:
				dist = math.sqrt((enemy_pos[0] + target_center[0] - event.pos[0])**2 + (enemy_pos[1] + target_center[1] - event.pos[1])**2)
				if dist < target_radius:
					arrow_num = int(dist // (target_radius / 5))
					if arrow_num == 0:
						win_sound.play()
					hit_list.append((event.pos[0], event.pos[1], arrow_num))
					hit_sound.play()
				else:
					miss_sound.play()
	
	# - - - Event Processing - - -
	
	
	# - - - STEP 2: Game Logic - - -
	
	# - - - Game Logic - - -
	if arrow_num == 0:
		enemy_display = True
	
	# - - - STEP 3: Drawing - - -
	
	# Clear the screen and/or draw background
	if playing:
		screen.fill(GREEN)
		target.set_alpha(128)
		screen.blit(target, target_pos)
	else:
		screen.fill(DARKGREEN)
		pygame.draw.rect(screen, GREEN, (target_center[0],target_center[1],width-target.get_size()[0],height-target.get_size()[1]))
		screen.blit(target, target_pos)
	
	# - - - Drawing - - -
	if enemy_display:
		screen.blit(target, enemy_pos)
		
	if playing:
		#screen.blit(arrow, arrow_pos)
		for hit in hit_list:
			arrow_clip = pygame.Rect(arrow.get_width()/5*hit[2],0,arrow.get_width()/5,arrow.get_height())
			arrow.set_clip(arrow_clip)
			arrow_draw = arrow.subsurface(arrow.get_clip())
			screen.blit(arrow_draw,(hit[0]-arrow_clip[2]/2,hit[1]))
	
	#Update the screen with what's been drawn
	pygame.display.flip()
	
	# Limit to 20 frames per second
	clock.tick(20)

# Close the window and quit
pygame.quit()