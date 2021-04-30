import pygame
import math


class ObjectsOfGame:
    def __init__(self, area, pos: tuple, color=(255, 0, 0), typeOfObj="Object"):
        self.area = area
        self.pos = [pos[0], pos[1]]
        self.color = color
        self.type = typeOfObj

    def __str__(self):
        return self.type + ", pos: " + str(self.pos)


class Ball(ObjectsOfGame):
    def __init__(self, area, pos: tuple, angle=math.pi / 3, radius=10, color=(255, 150, 90)):
        self.velocity = 7
        self.radius = radius
        self.angle = angle
        super().__init__(area, pos, color, "Ball")

    def draw(self):
        pygame.draw.circle(self.area, self.color, self.pos, self.radius, self.radius)
        pygame.draw.circle(self.area, (255, 0, 0), self.pos, 1, 1)

    def move(self, angle):
        self.angle = angle
        self.pos[0] += round(math.sin(angle + math.pi / 2) * self.velocity)
        self.pos[1] += round(math.cos(angle + math.pi / 2) * self.velocity)
        self.draw()


class Square(ObjectsOfGame):
    def __init__(self, area, pos: tuple, side=60, color=(0, 0, 200)):
        self.side = side
        super().__init__(area, pos, color, "Square")
        self.pointList = [self.pos[0], self.pos[1]], [self.pos[0] + self.side, self.pos[1]], \
            [self.pos[0] + self.side, self.pos[1] + self.side], [self.pos[0], self.pos[1] + self.side]

    def draw(self):
        pygame.draw.polygon(self.area, self.color, self.pointList)


class PointOfCollision(ObjectsOfGame):
    # this point is approximate the border of object
    def __init__(self, area, pos):
        super().__init__(area, pos, typeOfObj="Collision Point")

    def draw(self):
        pygame.draw.circle(self.area, self.color, self.pos, 3, 3)
