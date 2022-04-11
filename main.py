import sys, pygame
from random import randrange

pygame.init()

size = width, height = 640, 480
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0

screen = pygame.display.set_mode(size)

snakeParts = []
apples = []

x=100
y=100
lastTicks = 0

totalDelta = 0

direction = 'right'

speed = 0.6

maxLength = 5

totalAppleDelta = 0
appleThreshold = 3

score = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.ext()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction !='right':
                direction = 'left'
            if event.key == pygame.K_RIGHT and direction !='left':
                direction = 'right'
            if event.key == pygame.K_UP and direction !='down':
                direction = 'up'
            if event.key == pygame.K_DOWN and direction !='up':
                direction = 'down'

    time = pygame.time.get_ticks()
    delta = (time - lastTicks) / 1000
    totalDelta += delta
    totalAppleDelta += delta
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
        for apple in apples:
            if apple[0] == snakeParts[len(snakeParts) - 1][0] and apple[1] == snakeParts[len(snakeParts) - 1][1]:
                apples.remove(apple)
                score += 1
                print (score)

        if len(snakeParts) > 5:
            snakeParts.pop(0)
        totalDelta = 0

    if totalAppleDelta > appleThreshold:
        apples.append((randrange(63) * 10, randrange(47) * 10, 10, 10))
        totalAppleDelta = 0
        
    screen.fill(black)

    for snakePart in snakeParts:
        pygame.draw.rect(screen, white, snakePart)

    for apple in apples:
        pygame.draw.rect(screen, red, apple)

    pygame.display.flip()

