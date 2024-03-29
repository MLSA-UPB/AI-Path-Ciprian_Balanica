import pygame
import math

class Car:
    maxAcceleration = 7
    minAcceleration = -3
    def __init__(self, x, y, scale = 1, initAngle = 0, maxView = 300):
        self.x = x
        self.y = y
        self.scale = scale
        self.acc = 0
        self.angle = initAngle
        self.isAccelerating = False
        self.maxView = maxView

        self.sprite = pygame.image.load('Resources/car.png')
        self.spriteRect = self.sprite.get_rect()
        self.width = self.spriteRect.width * scale
        self.height = self.spriteRect.height * scale
        self.sprite = pygame.transform.scale(self.sprite, ((int)(self.width), (int)(self.height)))

        self.corners = calcCorners(self.x, self.y, self.width, self.height, self.angle)
        self.visions = [
            [(self.x, self.y), point(self.x, self.y, self.angle, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle + 30, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle - 30, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle + 60, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle - 60, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle + 90, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle - 90, self.maxView)]
        ]

    def draw(self, screen):
        #screen.blit(self.sprite, (self.x, self.y))
        #blitRotateCenter(screen, self.sprite, self.sprite.get_rect(center = (self.x, self.y)).topleft, self.angle)
        rotated_image = pygame.transform.rotate(self.sprite, self.angle)
        new_rect = rotated_image.get_rect(center = (self.x, self.y))


        screen.blit(rotated_image, new_rect.topleft)
        
    def updatePos(self):
        self.y = self.y - self.acc * math.sin(calcTrigAngle(self.angle))
        self.x = self.x + self.acc * math.cos(calcTrigAngle(self.angle))
        self.corners = calcCorners(self.x, self.y, self.width, self.height, calcTrigAngle(self.angle))
        self.visions = [
            [(self.x, self.y), point(self.x, self.y, self.angle - 90, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle - 60, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle - 30, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle + 30, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle + 60, self.maxView)],
            [(self.x, self.y), point(self.x, self.y, self.angle + 90, self.maxView)]
        ]

    def accelerate(self, value):
        self.acc += value
        if self.acc > self.maxAcceleration:
            self.acc = self.maxAcceleration
        if self.acc < self.minAcceleration:
            self.acc = self.minAcceleration
    
    def slowDown(self, value):
        if self.acc > value:
            self.acc -= value
        elif self.acc < -value:
            self.acc += value
        else:
            self.acc = 0

    def turn(self, value):
        self.angle += value

    def vision(self, walls, screen):
        distances = [301] * len(self.visions)
        for wall in walls:
            for i in range(len(self.visions)):
                if(intersect(self.visions[i][0], self.visions[i][1],(wall.x1, wall.y1), (wall.x2, wall.y2))):
                    pos = line_intersection((self.visions[i][0], self.visions[i][1]),((wall.x1, wall.y1), (wall.x2, wall.y2)))
                    # pygame.draw.circle(screen, (0,0,0), pos, 5)
                    distance = math.sqrt((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2)
                    if distance < distances[i]:
                        distances[i] = distance
        return distances


    def visionDraw(self, screen):
        for i in range(len(self.visions)):
            pygame.draw.line(screen, (0,0,0), self.visions[i][0], self.visions[i][1])

def calcTrigAngle(angle):
    return angle / 180 * math.pi + math.pi / 2

    
def calcDiff(x, y, dx, dy, a):
    return (
        x + dx * math.cos(math.pi/2.0 - a) + dy * math.sin(math.pi/2.0 - a),
        y + dx * math.sin(math.pi/2.0 - a) - dy * math.cos(math.pi/2.0 - a)
    )

def calcCorners(x, y, w, h, a):
    corners = []
    #topleft = (x - (w / 2) * math.sin(calcTrigAngle(a)), y - (h / 2) * math.cos(calcTrigAngle(a)))
    #topleft = (x - (w/2)*math.cos(calcTrigAngle(a - 45)), y - (h/2)*math.sin(calcTrigAngle(a -45)))
    topleft = calcDiff(x,y, -w/2.0, h/2.0, a)
    topright = calcDiff(x,y, w/2.0, h/2.0, a)
    bottomright = calcDiff(x,y, w/2.0, -h/2.0, a)
    bottomleft = calcDiff(x,y, -w/2.0, -h/2.0, a)
    corners.append(topleft)
    corners.append(topright)
    corners.append(bottomright)
    corners.append(bottomleft)
    return corners

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

def drawLine(x, y, angle, dist, screen):
    pygame.draw.line(screen, 
        (0,0,0), 
        (x, y), 
            (x + dist * math.cos(calcTrigAngle(angle)),
            y - dist * math.sin(calcTrigAngle(angle))),
        2)

def point(x, y, angle, dist):
    return (x + dist * math.cos(calcTrigAngle(angle)), y - dist * math.sin(calcTrigAngle(angle)))