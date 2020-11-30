import pygame
import math
import car
import wall
import os

pygame.init()

def checkKeyboardInput():
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.isAccelerating = True
        car.accelerate(0.1)
    if keys[pygame.K_DOWN]:
        car.isAccelerating = True
        car.accelerate(-0.05)
    if keys[pygame.K_RIGHT]:
        if abs(car.acc) > 0.5:
            car.turn(-turnAngle)
    if keys[pygame.K_LEFT]:
        if abs(car.acc) > 0.5:
            car.turn(turnAngle)
    if keys[pygame.K_SPACE]:
        car.slowDown(0.5)
    if keys[pygame.K_r]:
        changeStartPos(pygame.mouse.get_pos())
        car.x, car.y = pygame.mouse.get_pos()

def changeStartPos(pos):
    with open('start_pos.txt', 'w') as F:
        F.write('%d %d\n' % (pos[0], pos[1]))

def loadWalls(walls):
    
    if os.path.exists('walls.txt'):
        with open('walls.txt', 'r') as F:
            for line in F:
                txt = line[:-1]
                t = txt.split(' ')
                l = []
                for num in t:
                    l.append(int(num))
                w = wall.Wall(l[0], l[1], l[2], l[3])
                walls.append(w)

def drawWalls(wallWidth):
    for w in walls:
        pygame.draw.line(gameDisplay, black, (w.x1, w.y1), (w.x2, w.y2), wallWidth)

display_width = 1600
display_height = 900
turnAngle = 4.5
userInputOn = True

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Game")
 
clock = pygame.time.Clock()
crashed = False

white = (255, 255, 255)
black = (0, 0, 0)

startPos = (display_width / 2, display_height / 2)

if os.path.exists('start_pos.txt'):
    with open('start_pos.txt', 'r') as F:
        for line in F:
            txt = line[:-1]
            t = txt.split(' ')
            l = []
            for num in t:
                l.append(int(num))
            startPos = tuple(l)
        

car = car.Car(startPos[0], startPos[1], 0.02)
walls = []
loadWalls(walls)

move_ticker = 0

x1, y1, x2, y1 = (0, 0, 0, 0)
firstWallPos, secondWallPos = (0,0)

while not crashed:

    if pygame.mouse.get_pressed() == (1,0,0):
        if firstWallPos == 0:
            x1, y1 = pygame.mouse.get_pos()
            #print("SET 1")
            firstWallPos = 1
        elif secondWallPos == 1:
            x2, y2 = pygame.mouse.get_pos()
            #print("SET 2")
            secondWallPos = 2
    
    if pygame.mouse.get_pressed() == (0, 0, 0) and firstWallPos == 1 and secondWallPos == 0:
        secondWallPos = 1

    if secondWallPos == 2:
        #print("CREATED WALL")
        w = wall.Wall(x1,y1,x2,y2)
        walls.append(w)
        with open('walls.txt', 'a') as F:
            F.write('%d %d %d %d\n' % (x1, y1, x2, y2))
        x1, y1 = x2, y2
        secondWallPos = 0

    if pygame.mouse.get_pressed() == (0, 0, 1):
        #print("DELETE SAVED WALL POS")
        x1, y1, x2, y2 = (0,0,0,0)
        firstWallPos = 0
        secondWallPos = 0

    if pygame.mouse.get_pressed() == (0, 1, 0):
        #print("DELETE ALL WALLS")
        x1, y1, x2, y2 = (0,0,0,0)
        firstWallPos = 0
        secondWallPos = 0
        walls = []
        open("walls.txt", "w").close()

    car.isAccelerating = False
    if userInputOn:
        checkKeyboardInput()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                crashed = True
        print(event)

    gameDisplay.fill(white)
    
    if not car.isAccelerating:
        car.slowDown(0.5)


    drawWalls(2)
    car.updatePos()
    car.draw(gameDisplay)
    

    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()
