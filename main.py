import sys, pygame
from random import randrange

pygame.init()

font = pygame.font.SysFont(None, 24)

headerHeight = 30
snakeSize = 15
size = width, height = 700, 450
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

screen = pygame.display.set_mode(size)

snakeParts = []
apples = []

x = 150
y = 150
lastTicks = 0

totalDelta = 0

direction = 'right'

speed = 0.2

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
            x += snakeSize
        if direction == 'left':
            x -= snakeSize
        if direction == 'up':
            y -= snakeSize
        if direction == 'down':
            y += snakeSize

        snakeParts.append((x, y, snakeSize, snakeSize))

        # Check for Collision with wall
        currentX = snakeParts[len(snakeParts) - 1][0]
        currentY = snakeParts[len(snakeParts) - 1][1]
        if currentY < headerHeight or currentY >= height - snakeSize or currentX < 0 or currentX > width:
            print("You're dead!")

        for apple in apples:
            if apple[0] == snakeParts[len(snakeParts) - 1][0] and apple[1] == snakeParts[len(snakeParts) - 1][1]:
                apples.remove(apple)
                score += 1
                maxLength +=1

        if len(snakeParts) > maxLength:
            snakeParts.pop(0)
        totalDelta = 0

    if totalAppleDelta > appleThreshold:
        apples.append((randrange(int((width- snakeSize) / snakeSize)) * snakeSize, headerHeight + (randrange(int((height - snakeSize)) / snakeSize) * snakeSize), snakeSize, snakeSize))
        totalAppleDelta = 0
        
    screen.fill(black)

    pygame.draw.rect(screen, blue, (0, 0, width, headerHeight))

    img = font.render('score: ' + str(score), True, white)
    screen.blit(img, (10, 8))

    for snakePart in snakeParts:
        pygame.draw.rect(screen, green, snakePart)

    for apple in apples:
        pygame.draw.rect(screen, red, apple)

    pygame.display.flip()