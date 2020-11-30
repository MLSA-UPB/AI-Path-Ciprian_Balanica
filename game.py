import pygame
import math
import car
import wall
import os

pygame.init()

###

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return 0, 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

###

def checkForCollision(obj, wallList):
        for wall in wallList:
            for i in range(4):
                if(intersect(obj.corners[i], obj.corners[(i+1)%4],(wall.x1, wall.y1), (wall.x2, wall.y2))):
                    pos = line_intersection((obj.corners[i], obj.corners[(i+1)%4]),((wall.x1, wall.y1), (wall.x2, wall.y2)))
                    pygame.draw.circle(gameDisplay, (0,0,0), pos, 5)
                    if type(obj) == car.Car:
                        killPlayer()
def killPlayer():
    player.__init__(startPos[0], startPos[1], 0.02)


def checkKeyboardInput():
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.isAccelerating = True
        player.accelerate(0.1)
    if keys[pygame.K_DOWN]:
        player.isAccelerating = True
        player.accelerate(-0.05)
    if keys[pygame.K_RIGHT]:
        if abs(player.acc) > 0.5:
            player.turn(-turnAngle)
    if keys[pygame.K_LEFT]:
        if abs(player.acc) > 0.5:
            player.turn(turnAngle)
    if keys[pygame.K_SPACE]:
        player.slowDown(0.5)
    if keys[pygame.K_r]:
        changeStartPos(pygame.mouse.get_pos())
        player.x, player.y = pygame.mouse.get_pos()

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

def debugMode():
    drawWalls(2)
    for cor in player.corners:
        pygame.draw.circle(gameDisplay, (0,0,0), cor, 3)
    debugBorder()
    checkForCollision(player, walls)

def debugBorder():
    pygame.draw.line(gameDisplay, black, player.corners[0], player.corners[1], 2)
    pygame.draw.line(gameDisplay, black, player.corners[1], player.corners[2], 2)
    pygame.draw.line(gameDisplay, black, player.corners[2], player.corners[3], 2)
    pygame.draw.line(gameDisplay, black, player.corners[3], player.corners[0], 2)

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
        

player = car.Car(startPos[0], startPos[1], 0.02)
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

    player.isAccelerating = False
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
    
    if not player.isAccelerating:
        player.slowDown(0.5)


    player.updatePos()
    debugMode()
    player.draw(gameDisplay)
    

    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()
