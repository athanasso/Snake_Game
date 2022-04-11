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

bestScore = 0

def resetGame():
    global snakeParts, apples, x, y, score, maxLength, lastTicks, totalDelta, direction, bestScore
    snakeParts = []
    apples = []
    score = 0
    x, y = 150, 150
    maxLength = 5
    lastTicks = 0
    totalDelta = 0
    direction = 'right'

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

        currentX = snakeParts[len(snakeParts) - 1][0]
        currentY = snakeParts[len(snakeParts) - 1][1]

        # Check for Collision with wall

        if currentY < headerHeight or currentY >= height - snakeSize or currentX < 0 or currentX > width:
            resetGame()
            print("You're dead from wall!")

        # Check for collision with yourself

        if len(snakeParts) > 0:
            snakePartsExcludingLast = snakeParts.copy()
            snakePartsExcludingLast.pop()
            for snakePart in snakePartsExcludingLast:
                if snakePart[0] == currentX and snakePart[1] == currentY:
                    resetGame()
                    print ("You are dead from yourself!")

        for apple in apples:
            if apple[0] == snakeParts[len(snakeParts) - 1][0] and apple[1] == snakeParts[len(snakeParts) - 1][1]:
                apples.remove(apple)
                score += 1
                maxLength +=1
                if score > bestScore:
                    bestScore = score

        if len(snakeParts) > maxLength:
            snakeParts.pop(0)
        totalDelta = 0

    if totalAppleDelta > appleThreshold:
        apples.append((randrange(int((width- snakeSize) / snakeSize)) * snakeSize, headerHeight + (randrange(int((height - snakeSize)) / snakeSize) * snakeSize), snakeSize, snakeSize))
        totalAppleDelta = 0
        
    screen.fill(black)

    pygame.draw.rect(screen, blue, (0, 0, width, headerHeight))

    scoreImage = font.render('score: ' + str(score), True, white)
    bestScoreImage = font.render('best score: ' + str(bestScore), True, white)

    screen.blit(scoreImage, (10, 8))
    screen.blit(bestScoreImage, (100, 8))

    for snakePart in snakeParts:
        pygame.draw.rect(screen, green, snakePart)

    for apple in apples:
        pygame.draw.rect(screen, red, apple)

    pygame.display.flip()