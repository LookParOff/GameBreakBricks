import numpy as np
import random
import time
import math
from Objects import *
from Structures import Tree2D
pygame.init()
timer = pygame.time.Clock()
WIDTH = 450
HEIGHT = 600


class WrongAngleWhichWeDidNotExpected(Exception):
    def __init__(self, angle):
        self.angle = angle

    def __str__(self):
        return "Check angle " + str(round(self.angle * 57.2958, 2))


def distanceBetweenPointAndPoint(aPoint, bPoint):
    ax, ay, bx, by = aPoint[0], aPoint[1], bPoint[0], bPoint[1]
    A = abs(ax - bx)
    B = abs(ay - by)
    return math.sqrt(A**2 + B**2)


def distanceBetweenPointAndLine(point, line):
    a = distanceBetweenPointAndPoint(line[0], point)
    b = distanceBetweenPointAndPoint(line[1], point)
    c = distanceBetweenPointAndPoint(line[0], line[1])

    # gamma = math.acos((a**2 + b**2 - c**2) / (2*a*b))
    beta = math.acos((a**2 + c**2 - b**2) / (2*a*c))
    alfa = math.acos((b**2 + c**2 - a**2) / (2*c*b))

    if alfa >= math.pi / 2 or beta >= math.pi / 2:
        # height is not correct, because doesnt fall to line
        return min(a, b)
    p = (a + b + c) / 2
    S = math.sqrt(p * (p - a) * (p - b) * (p - c))
    h = 2 * S / c
    return h


def isCollisionOfArea(a: Ball):
    if (not (0 <= a.pos[0] + a.radius <= WIDTH) or not (0 <= a.pos[0] - a.radius <= WIDTH)) and \
       (not (0 <= a.pos[1] + a.radius <= HEIGHT) or not (0 <= a.pos[1] - a.radius <= HEIGHT)):
        return "xy"
    if not (0 <= a.pos[0] + a.radius <= WIDTH) or not (0 <= a.pos[0] - a.radius <= WIDTH):
        return "x"
    if not (0 <= a.pos[1] + a.radius <= HEIGHT) or not (0 <= a.pos[1] - a.radius <= HEIGHT):
        return "y"
    return ""


def isCollisionOfSquare(ball: Ball, squareList):
    for square in squareList:

        allDistances = \
        [
            distanceBetweenPointAndLine(ball.pos, [square.pointList[0], square.pointList[3]]),
            distanceBetweenPointAndLine(ball.pos, [square.pointList[1], square.pointList[2]]),
            distanceBetweenPointAndLine(ball.pos, [square.pointList[0], square.pointList[1]]),
            distanceBetweenPointAndLine(ball.pos, [square.pointList[3], square.pointList[2]])
        ]

        #        2
        #        _
        #     0 |_| 1
        #        3
        # check collision with a corner
        minDist = min(allDistances)
        if allDistances[0] == allDistances[3] <= ball.radius + ball.velocity // 2 or allDistances[3] == allDistances[1] <= ball.radius + ball.velocity // 2 or \
           allDistances[1] == allDistances[2] <= ball.radius + ball.velocity // 2 or allDistances[2] == allDistances[0] <= ball.radius + ball.velocity // 2:
            return "xy"
        if (minDist == allDistances[0] <= ball.radius + ball.velocity // 2 or minDist == allDistances[1] <= ball.radius + ball.velocity // 2):
            return "x"
        if (minDist == allDistances[2] <= ball.radius + ball.velocity // 2 or minDist == allDistances[3] <= ball.radius + ball.velocity // 5):
            return "y"
    return ""


def isCollision(ball, tree):
    points = tree.request_of_area(ball.pos[0], ball.pos[1], ball.radius)  # all points, inside ball.
    if len(points) != 0:
        # return ball.angle + np.pi / 2
        m = 2**32
        point = points[0]
        for p in points:
            d = distanceBetweenPointAndPoint(ball.pos, p)
            if d < m:
                m = d
                point = p
        theta = np.arctan(ball.deltas[1] / ball.deltas[0])
        if ball.deltas[1] < 0:
            theta += np.pi
        v1 = np.sqrt(ball.deltas[0] ** 2 + ball.deltas[1] ** 2)
        v2 = 0
        x1 = ball.pos
        # if abs(x1[0] - point[0]) < abs(x1[1] - point[1]):
        #     x2 = (x1[0], point[1])
        # else:
        #     x2 = (point[0], x1[1])
        x2 = point
        fi = angleBetweenTwoPoints(x1, x2)
        m1 = 1
        m2 = 2**32
        # ball collision
        v1_X = v1 * np.cos(theta - fi) * (m1 - m2) * np.cos(fi) / (m1 + m2) + v1 * np.sin(theta - fi) * np.cos(fi + np.pi / 2)
        v1_Y = v1 * np.cos(theta - fi) * (m1 - m2) * np.sin(fi) / (m1 + m2) + v1 * np.sin(theta - fi) * np.sin(fi + np.pi / 2)
        if np.isnan(v1_X):
            return ball.deltas
        print([v1_X, v1_Y], ball.deltas)
        return v1_X, v1_Y
    return ball.deltas
    # https://stackru.com/questions/35517796/2d-uprugaya-sharikovaya-fizika
    # https://williamecraver.wixsite.com/elastic-equations


def angleBetweenTwoPoints(aPoint, bPoint):
    # actually it's angel between line(aPoint, bPoint) and Ox
    ax, ay, bx, by = aPoint[0], aPoint[1], bPoint[0], bPoint[1]
    A = abs(ax - bx)
    B = abs(ay - by)
    C = math.sqrt(A**2 + B**2)
    angle = math.asin(B / C)
    if bx >= ax and by <= ay:
        return angle
    if bx <= ax and by <= ay:
        return math.pi - angle
    if bx <= ax and by >= ay:
        return math.pi + angle
    if bx >= ax and by >= ay:
        return 2 * math.pi - angle


def updateTreeOfCollisionPoints(tree: Tree2D, newSquare: Square, approx):
    newPoints = []
    for i in range(approx + 1):
        newPoints.append((newSquare.pointList[0][0] + newSquare.side * i // approx, newSquare.pointList[0][1]))
        newPoints.append((newSquare.pointList[1][0], newSquare.pointList[1][1] + newSquare.side * i // approx))
        newPoints.append((newSquare.pointList[2][0] - newSquare.side * i // approx, newSquare.pointList[2][1]))
        newPoints.append((newSquare.pointList[3][0], newSquare.pointList[3][1] - newSquare.side * i // approx))
    tree.insert_list(newPoints)


def mainDraw():
    # TODO we can store points of squares in Tree2d, or points of circle. What will be effective?
    # I think store points of circle will be effective, cos so count of requests to areas(squares) will be less
    FPS = 30
    approx = 50  # count of collision points on each side
    area = pygame.display.set_mode((WIDTH, HEIGHT))
    areaColor = (65, 50, 75)
    area.fill(areaColor)

    spawnPlace = (WIDTH // 2, HEIGHT // 2)
    spawnPlace = (167, 364)
    ballsList = []
    squareList = [Square(area, (250, 250))]
    treeOfCollision = Tree2D()
    updateTreeOfCollisionPoints(treeOfCollision, squareList[0], approx)

    for _ in range(0, 0):
        # angle = random.random() * 2 * math.pi
        angle = 0  # 3 * np.pi / 2 + np.pi / 6
        sp = (int(random.random() * WIDTH/3), int(random.random() * HEIGHT/3.5))
        # sp = (260, 100)
        dx, dy = math.sin(angle + math.pi / 2), math.cos(angle + math.pi / 2)
        ball = Ball(area, sp, dx, dy)
        ballsList.append(ball)
    for i in range(10):
        sq = Square(area, (i * 51, 300))
        squareList.append(sq)
        updateTreeOfCollisionPoints(treeOfCollision, sq, approx)

        sq = Square(area, (i * 51, 500))
        squareList.append(sq)
        updateTreeOfCollisionPoints(treeOfCollision, sq, approx)

    while True:
        area.fill(areaColor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    angle = angleBetweenTwoPoints(spawnPlace, event.pos)
                    dx, dy = math.sin(angle + math.pi / 2), math.cos(angle + math.pi / 2)
                    print("New ball with angle:", angle)
                    ballsList.append(Ball(area, spawnPlace, dx, dy))
                if event.button == 2:
                    squareList.append(Square(area, event.pos))
                    updateTreeOfCollisionPoints(treeOfCollision, squareList[-1], approx)
                if event.button == 3:
                    spawnPlace = (event.pos[0], event.pos[1])
                    print("New Spawn:", spawnPlace)
        start = time.time()

        for index, ball in enumerate(ballsList):
            dx, dy = isCollision(ball, treeOfCollision)
            ball.move(dx, dy)
            if ball.pos[0] > WIDTH or ball.pos[0] < 0 or ball.pos[1] > HEIGHT or ball.pos[1] < 0:
                ballsList.pop(index)

        for ball in ballsList:
            ball.draw()
        for square in squareList:
            square.draw()

        end = time.time()
        pygame.display.update()
        timer.tick(FPS)
        # print("Time of cycle", end - start)


mainDraw()
