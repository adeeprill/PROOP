import pygame, sys
pygame.init()

WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

playerRect = pygame.Rect(32, 32, 32, 32)
right, left, up, down = False, False, False, False
playerVelX = 0
playerVelY = 0

wallRect = pygame.Rect(200, 100, 32, 96)

while True:
	screen.fill((0, 0, 0))

	pygame.draw.rect(screen, (255, 0, 0), wallRect)
	pygame.draw.rect(screen, (255, 255, 255), playerRect)

	if playerRect.colliderect(wallRect):
		if playerVelX > 0:
			playerRect.right = wallRect.left
		if playerVelX < 0:
			playerRect.left = wallRect.right
		if playerVelY < 0:
			playerRect.top = wallRect.bottom 
		if playerVelY > 0:
			playerRect.bottom = wallRect.top

	if right:
		playerVelX = 3
	elif left:
		playerVelX = -3
	else:
		playerVelX = 0

	if up:
		playerVelY = -3
	elif down:
		playerVelY = 3
	else:
		playerVelY = 0

	playerRect.x += playerVelX
	playerRect.y += playerVelY

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				right = True
			if event.key == pygame.K_LEFT:
				left = True
			if event.key == pygame.K_UP:
				up = True
			if event.key == pygame.K_DOWN:
				down = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				right = False
			if event.key == pygame.K_LEFT:
				left = False
			if event.key == pygame.K_UP:
				up = False
			if event.key == pygame.K_DOWN:
				down = False

	pygame.display.update()
	clock.tick(60)