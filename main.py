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
    # return new dx, dy for ball in case of collision,
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
        v1 = 1  # np.sqrt(ball.deltas[0] ** 2 + ball.deltas[1] ** 2)
        v2 = 0
        x1 = ball.pos
        x2 = point
        fi = angleBetweenTwoPoints(x1, x2)
        if abs(fi - 0) < 0.1 or abs(fi - np.pi) < 0.1:
            # we hit wall Ox
            ball.deltas = -ball.deltas[0], ball.deltas[1]
            return point[2]
        elif abs(fi - np.pi / 2) < 0.1 or abs(fi - 3 * np.pi / 2) < 0.1:
            # we hit wall Oy
            ball.deltas = ball.deltas[0], -ball.deltas[1]
            return point[2]
        else:
            ball.deltas = -ball.deltas[0], -ball.deltas[1]
            return point[2]
    return None
    # https://stackru.com/questions/35517796/2d-uprugaya-sharikovaya-fizika
    # https://williamecraver.wixsite.com/elastic-equations


def angleBetweenTwoPoints(aPoint, bPoint):
    # actually it's angel between line(aPoint, bPoint) and Ox
    ax, ay, bx, by = aPoint[0], aPoint[1], bPoint[0], bPoint[1]
    A = abs(ax - bx)
    B = abs(ay - by)
    C = math.sqrt(A**2 + B**2)
    if C == 0:
        return 0
    angle = math.asin(B / C)
    if bx >= ax and by <= ay:
        return angle
    if bx <= ax and by <= ay:
        return math.pi - angle
    if bx <= ax and by >= ay:
        return math.pi + angle
    if bx >= ax and by >= ay:
        return 2 * math.pi - angle


def insertInTreeOfCollision(tree: Tree2D, newSquare: Square, approx):
    newPoints = []
    for i in range(approx + 1):
        newPoints.append((newSquare.pointList[0][0] + newSquare.side * i // approx, newSquare.pointList[0][1]))
        newPoints.append((newSquare.pointList[1][0], newSquare.pointList[1][1] + newSquare.side * i // approx))
        newPoints.append((newSquare.pointList[2][0] - newSquare.side * i // approx, newSquare.pointList[2][1]))
        newPoints.append((newSquare.pointList[3][0], newSquare.pointList[3][1] - newSquare.side * i // approx))
    tree.insert_list(newPoints, newSquare)


def deleteInTreeOfCollision(tree: Tree2D, square: Square, approx):
    for i in range(approx + 1):
        tree.delete(square.pointList[0][0] + square.side * i // approx, square.pointList[0][1])
        tree.delete(square.pointList[1][0], square.pointList[1][1] + square.side * i // approx)
        tree.delete(square.pointList[2][0] - square.side * i // approx, square.pointList[2][1])
        tree.delete(square.pointList[3][0], square.pointList[3][1] - square.side * i // approx)


def mainDraw():
    # TODO we can store points of squares in Tree2d, or points of circle. What will be effective?
    # I think store points of circle will be effective, cos so count of requests to areas(squares) will be less
    FPS = 30
    approx = 50  # count of collision points on each side
    area = pygame.display.set_mode((WIDTH, HEIGHT))
    areaColor = (150, 150, 150)
    area.fill(areaColor)

    spawnPlace = (WIDTH // 2, HEIGHT // 2)
    spawnPlace = (167, 364)
    ballsList = []
    squareList = [Square(area, (250, 250))]
    treeOfCollision = Tree2D()
    insertInTreeOfCollision(treeOfCollision, squareList[0], approx)

    # border of screen
    treeOfCollision.insert_list([(-1, i) for i in range(HEIGHT)] + [(i, -1) for i in range(WIDTH)])
    treeOfCollision.insert_list([(WIDTH + 1, i) for i in range(HEIGHT)] + [(i, HEIGHT + 1) for i in range(WIDTH)])

    for _ in range(0):
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
        insertInTreeOfCollision(treeOfCollision, sq, approx)

        sq = Square(area, (i * 51, 500))
        squareList.append(sq)
        insertInTreeOfCollision(treeOfCollision, sq, approx)

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
                    print(f"New ball №{len(ballsList)} with angle:", angle)
                    ballsList.append(Ball(area, spawnPlace, dx, dy))
                if event.button == 2:
                    squareList.append(Square(area, event.pos))
                    print(f"New square №{len(squareList)} with pos:", squareList[-1].pos)
                    insertInTreeOfCollision(treeOfCollision, squareList[-1], approx)
                if event.button == 3:
                    spawnPlace = (event.pos[0], event.pos[1])
                    print("New Spawn:", spawnPlace)

        for index, ball in enumerate(ballsList):
            hit = isCollision(ball, treeOfCollision)
            ball.move(ball.deltas[0], ball.deltas[1])
            if ball.pos[0] > WIDTH or ball.pos[0] < 0 or ball.pos[1] > HEIGHT or ball.pos[1] < 0:
                ballsList.pop(index)
            if hit is not None:
                hit.lifePoints -= 1
                if hit.lifePoints <= 0:
                    deleteInTreeOfCollision(treeOfCollision, hit, approx)
        for ball in ballsList:
            ball.draw()
        for index, square in enumerate(squareList):
            if square.lifePoints <= 0:
                squareList[index] = None
            else:
                square.draw()
        for _ in range(squareList.count(None)):
            squareList.remove(None)
        font = pygame.font.Font(None, 20)
        fpsShower = font.render(str(int(timer.get_fps())), True, pygame.Color('white'))
        area.blit(fpsShower, (WIDTH - 20, 7))
        timer.tick(FPS)

        pygame.display.update()


mainDraw()
