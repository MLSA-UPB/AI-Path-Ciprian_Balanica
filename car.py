import pygame
import math

class Car:
    maxAcceleration = 10
    minAcceleration = -5
    def __init__(self, x, y, scale = 1, initAngle = 0):
        self.x = x
        self.y = y
        self.scale = scale
        self.acc = 0
        self.angle = initAngle
        self.isAccelerating = False

        self.sprite = pygame.image.load('Resources/car.png')
        self.spriteRect = self.sprite.get_rect()
        self.width = (int)(self.spriteRect.width * scale)
        self.height = (int)(self.spriteRect.height * scale)
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

        self.corners = calcCorners(self.x, self.y, self.width, self.height, self.angle)

    def draw(self, screen):
        #screen.blit(self.sprite, (self.x, self.y))
        #blitRotateCenter(screen, self.sprite, self.sprite.get_rect(center = (self.x, self.y)).topleft, self.angle)
        rotated_image = pygame.transform.rotate(self.sprite, self.angle)
        new_rect = rotated_image.get_rect(center = (self.x, self.y))


        screen.blit(rotated_image, new_rect.topleft)
        for cor in self.corners:
            pygame.draw.circle(screen, (0,0,0), cor, 3)
        
    def updatePos(self):
        self.y = self.y - self.acc * math.sin(calcTrigAngle(self.angle))
        self.x = self.x + self.acc * math.cos(calcTrigAngle(self.angle))
        self.corners = calcCorners(self.x, self.y, self.width, self.height, calcTrigAngle(self.angle))

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
        self.angle += value * (abs(self.acc) / self.maxAcceleration)

    def checkForCollision(self, wallList):
        pass

def calcTrigAngle(angle):
    return angle / 180 * math.pi + math.pi / 2

def calcCorners(x, y, w, h, a):
    corners = []
    #topleft = (x - (w / 2) * math.sin(calcTrigAngle(a)), y - (h / 2) * math.cos(calcTrigAngle(a)))
    #topleft = (x - (w/2)*math.cos(calcTrigAngle(a - 45)), y - (h/2)*math.sin(calcTrigAngle(a -45)))
    topleft = (
        x - w/2.0 * math.cos(math.pi/2.0 - a) + h/2.0 * math.sin(math.pi/2.0 - a),
        y - w/2.0 * math.sin(math.pi/2.0 - a) - h/2.0 * math.cos(math.pi/2.0 - a)
    )
    topright = (
        x + w/2.0 * math.cos(math.pi/2.0 - a) + h/2.0 * math.sin(math.pi/2.0 - a),
        y + w/2.0 * math.sin(math.pi/2.0 - a) - h/2.0 * math.cos(math.pi/2.0 - a)
    )
    bottomright = (
        x + w/2.0 * math.cos(math.pi/2.0 - a) - h/2.0 * math.sin(math.pi/2.0 - a),
        y + w/2.0 * math.sin(math.pi/2.0 - a) + h/2.0 * math.cos(math.pi/2.0 - a)
    )
    bottomleft = (
        x - w/2.0 * math.cos(math.pi/2.0 - a) - h/2.0 * math.sin(math.pi/2.0 - a),
        y - w/2.0 * math.sin(math.pi/2.0 - a) + h/2.0 * math.cos(math.pi/2.0 - a)
    )
    corners.append(topleft)
    corners.append(topright)
    corners.append(bottomright)
    corners.append(bottomleft)
    return corners