import sys, pygame
pygame.init()

size = width, height = 640, 480
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

snakeParts = []
x=100
y=100
lastTicks = 0

totalDelta = 0

direction = 'right'

speed = 0.6

maxLength = 5

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.ext()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = 'left'
            if event.key == pygame.K_RIGHT:
                direction = 'right'
            if event.key == pygame.K_UP:
                direction = 'up'
            if event.key == pygame.K_DOWN:
                direction = 'down'

    time = pygame.time.get_ticks()
    delta = (time - lastTicks) / 1000
    totalDelta += delta
    lastTicks = time

    if totalDelta > speed:
        if direction == 'right':
            x += 10
        if direction == 'left':
            x -= 10
        if direction == 'up':
            y -= 10
        if direction == 'down':
            y += 10

        snakeParts.append((x, y, 10, 10))
        if len(snakeParts) > 5:
            snakeParts.pop(0)
        totalDelta = 0
        
    screen.fill(black)

    for snakePart in snakeParts:
        pygame.draw.rect(screen, white, snakePart)

    pygame.display.flip()

