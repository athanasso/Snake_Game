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
backgroundColour = 165, 204, 73
foregroundColour = 85, 110, 27

screen = pygame.display.set_mode(size)

snakeParts = []
apples = []

x = 150
y = 150
lastTicks = 0

totalDelta = 0

direction = 'right'

speed = 0.5
maxSpeed = 0.1
speedIncrement = 0.02

maxLength = 5

totalAppleDelta = 0
appleThreshold = 4
maxNumberOfApples = 3

score = 0

bestScore = 0

f = open("snake.txt", "r")
fileContents = f.read()
if (fileContents):
    bestScore = int(fileContents)

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                    
        screen.fill(backgroundColour)
        messageToScreen("Welcome to Slither",
                          green,
                          -100,
                          "medium")
        messageToScreen("The objective of the game is to eat red apples",
                          black,
                          -30,
                          "small")
        messageToScreen("The more apples you eat, the longer you get",
                          black,
                          10,
                          "small")
        messageToScreen("If you run into yourself, or the edges, you die!",
                          black,
                          50,
                          "small")
        messageToScreen("Press Space to play, or ESC to quit.",
                          black,
                          180,
                          "small")
        pygame.display.update()

def textObjects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
        
    return textSurface, textSurface.get_rect()

def messageToScreen(msg, color, yDisplace=0, size = "small"):
    textSurf,textRect = textObjects(msg,color, size)
    textRect.center = (width/2), (height/2)+yDisplace
    screen.blit(textSurf, textRect)

def pause():
    paused = True
    while paused:
        backgroundMusic.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_SPACE:
                    paused = False
                    backgroundMusic.play(-1)

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill(backgroundColour)
        messageToScreen("Game Over!", black, -100, size="large")
        messageToScreen("Press space to continue or ESC to Quit", black, 25)
        pygame.display.update()

def resetGame():
    global snakeParts, apples, x, y, score, maxLength, lastTicks, totalDelta, direction, bestScore, speed
    snakeParts = []
    apples = []
    score = 0
    x, y = 150, 150
    maxLength = 5
    lastTicks = 0
    totalDelta = 0
    direction = 'right'
    speed = 0.5
    f = open("snake.txt", "w")
    f.write(str(bestScore))
    f.close()

backgroundMusic = pygame.mixer.Sound('Sounds/pokemon_route.mp3')
backgroundMusic.set_volume(0.2)
backgroundMusic.play(-1)

eatSoundEffect = pygame.mixer.Sound('Sounds/eat.wav')
eatSoundEffect.set_volume(4)

crashSoundEffect = pygame.mixer.Sound('Sounds/crash.wav')
crashSoundEffect.set_volume(4)

gameIntro()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT : sys.ext()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

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

        if currentY < headerHeight or currentY >= height or currentX < 0 or currentX > width:
            resetGame()
            crashSoundEffect.play()
            pause()
            print("You're dead from wall!")

        # Check for collision with yourself

        if len(snakeParts) > 0:
            snakePartsExcludingLast = snakeParts.copy()
            snakePartsExcludingLast.pop()
            for snakePart in snakePartsExcludingLast:
                if snakePart[0] == currentX and snakePart[1] == currentY:
                    resetGame()
                    crashSoundEffect.play()
                    pause()
                    print ("You are dead from yourself!")

        for apple in apples:
            if apple[0] == snakeParts[len(snakeParts) - 1][0] and apple[1] == snakeParts[len(snakeParts) - 1][1]:
                apples.remove(apple)
                if speed > maxSpeed:
                    speed -= speedIncrement
                score += 1
                eatSoundEffect.play()
                maxLength +=1
                if score > bestScore:
                    bestScore = score

        if len(snakeParts) > maxLength:
            snakeParts.pop(0)
        totalDelta = 0

    if totalAppleDelta > appleThreshold and len(apples) <= maxNumberOfApples:
        apples.append((randrange(int((width- snakeSize) / snakeSize)) * snakeSize, headerHeight + (randrange(int((height - snakeSize)) / snakeSize) * snakeSize), snakeSize, snakeSize))
        totalAppleDelta = 0
        
    screen.fill(backgroundColour)

    pygame.draw.rect(screen, foregroundColour, (0, 0, width, headerHeight))

    scoreImage = font.render('score: ' + str(score), True, backgroundColour)
    bestScoreImage = font.render('best score: ' + str(bestScore), True, backgroundColour)

    screen.blit(scoreImage, (10, 8))
    screen.blit(bestScoreImage, (100, 8))

    for snakePart in snakeParts:
        pygame.draw.rect(screen, foregroundColour, snakePart)

    for apple in apples:
        pygame.draw.rect(screen, red, apple)

    pygame.display.flip()