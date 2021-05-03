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
    def __init__(self, area, pos: tuple, dx, dy, angle=math.pi / 3, radius=10, color=(255, 150, 90)):
        super().__init__(area, pos, color, "Ball")
        self.velocity = 7
        self.radius = radius
        # self.angle = angle
        self.deltas = [dx, dy]

    def draw(self):
        pygame.draw.circle(self.area, self.color, self.pos, self.radius, self.radius)
        pygame.draw.circle(self.area, (255, 0, 0), self.pos, 1, 1)

    def move(self, dx, dy):
        self.deltas = [dx, dy]
        self.pos[0] += int(dx * self.velocity)
        self.pos[1] += int(dy * self.velocity)
        self.draw()


class Square(ObjectsOfGame):
    def __init__(self, area, pos: tuple, side=50, color=(0, 0, 150)):
        super().__init__(area, pos, color, "Square")
        self.side = side
        self.pointList = [self.pos[0], self.pos[1]], [self.pos[0] + self.side, self.pos[1]], \
            [self.pos[0] + self.side, self.pos[1] + self.side], [self.pos[0], self.pos[1] + self.side]
        self.lifePoints = 5
        self.font = pygame.font.Font(None, 23)

    def draw(self):
        pygame.draw.polygon(self.area, self.color, self.pointList)
        lifeText = self.font.render(str(self.lifePoints), True, (0, 179, 200))
        pygame.draw.line(self.area, (0, 0, 255), self.pointList[0], self.pointList[1], 2)
        pygame.draw.line(self.area, (0, 0, 255), self.pointList[1], self.pointList[2], 2)
        pygame.draw.line(self.area, (0, 0, 255), self.pointList[2], self.pointList[3], 2)
        pygame.draw.line(self.area, (0, 0, 255), self.pointList[0], self.pointList[3], 2)
        self.area.blit(lifeText, (self.pos[0] + self.side / 2.7, self.pos[1] + self.side / 2.7))


class PointOfCollision(ObjectsOfGame):
    # this point is approximate the border of object
    def __init__(self, area, pos):
        super().__init__(area, pos, typeOfObj="Collision Point")

    def draw(self):
        pygame.draw.circle(self.area, self.color, self.pos, 3, 3)
