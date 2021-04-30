import random
import time
from Objects import *
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


def isCollision(ball, squareList):
    colSq = isCollisionOfSquare(ball, squareList)
    colAr = isCollisionOfArea(ball)
    if len(colSq) == len(colAr) == 0:
        return ""
    if len(colAr) != 0 and len(colSq) == 0:
        return colAr
    if len(colAr) == 0 and len(colSq) != 0:
        return colSq
    if len(colAr) != 0 and len(colSq) != 0:
        return "xy"


def giveAngleAfterCollision(a: Ball, coordinateOfCollision):
    if coordinateOfCollision == "x":
        if 0 <= a.angle < math.pi / 2:
            return math.pi - a.angle
        if math.pi / 2 < a.angle <= math.pi:
            return abs(math.pi - a.angle)
        if math.pi < a.angle < 3 * math.pi / 2:
            return -(a.angle - math.pi) + 2 * math.pi
        if 3 * math.pi / 2 < a.angle <= 2 * math.pi:
            return 2 * math.pi - a.angle + math.pi
        else:
            print(a)
            raise WrongAngleWhichWeDidNotExpected(a.angle)
    elif coordinateOfCollision == "y":
        if 0 < a.angle <= math.pi / 2:
            return (a.angle - 2 * a.angle) + 2 * math.pi
        if math.pi / 2 < a.angle < math.pi:
            return (math.pi - a.angle) + math.pi
        if math.pi < a.angle <= 3 * math.pi / 2:
            return a.angle - 2 * (a.angle - math.pi)
        if 3 * math.pi / 2 < a.angle < 2 * math.pi:
            return 2 * math.pi - a.angle
        else:
            print(a)
            raise WrongAngleWhichWeDidNotExpected(a.angle)

    elif coordinateOfCollision == "xy":
        if a.angle + math.pi > 2 * math.pi:
            return a.angle - math.pi
        return a.angle + math.pi
    elif coordinateOfCollision == "corner":
        return a.angle
    else:
        return a.angle


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


def mainDraw():
    # TODO we can store points of squares in Tree2d, or points of circle. What will be effective?
    # I think store points of circle will be effective, cos so count of requests to areas(squares) will be less
    FPS = 30
    area = pygame.display.set_mode((WIDTH, HEIGHT))
    areaColor = (65, 50, 75)
    # area.fill(areaColor)

    spawnPlace = (WIDTH // 2, HEIGHT // 2)
    spawnPlace = (167, 364)
    ballsList = []
    squareList = [Square(area, (250, 250))]

    for _ in range(0, 10):
        angle = random.random() * 2 * math.pi
        sp = (int(random.random() * WIDTH/2), int(random.random() * HEIGHT/2.5))
        ball = Ball(area, sp, angle)
        ballsList.append(ball)

    while True:
        area.fill(areaColor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    angle = angleBetweenTwoPoints(spawnPlace, event.pos)
                    print("New ball with angle:", angle)
                    ballsList.append(Ball(area, spawnPlace, angle))
                if event.button == 2:
                    squareList.append(Square(area, event.pos))
                if event.button == 3:
                    spawnPlace = (event.pos[0], event.pos[1])
                    print("New Spawn:", spawnPlace)
        start = time.time()

        for ball in ballsList:
            coordinateOfCollision = isCollision(ball, squareList)
            angle = giveAngleAfterCollision(ball, coordinateOfCollision)
            ball.move(angle)
        for ball, square in zip(ballsList, squareList):
            ball.draw()
            square.draw()

        end = time.time()
        pygame.display.update()
        timer.tick(FPS)
        print(len(ballsList))
        # print("Time of cycle", end - start)


mainDraw()
