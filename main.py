from enum import Enum
from Stack import Stack
import os
import time

class RType(Enum):
    ROUTE = 2
    CROSSROAD = 4
    FORKEDROAD = 3
    DEADEND = 0
    GOAL = 100
    NONE = -1
    SEEN = -2

GOAL = "◉"
ROUTES = '╔═╗║╚╝'
CROSSROADS = '╬'
FORKEDROADS = '╠╩╦╣'
DEADENDS = '╨╞╥'
SEEN = '░'
ICON = '◆'

isreturning = False
navhistory = []
count_back = 0
lastDecision = 0
record = False

with open("maze.txt") as mazefile:
    mazemap = mazefile.readlines()

position = (0,3)
lastWays = Stack()

def routeTypeByR(route):
    if route in ROUTES:
        return RType.ROUTE
    if route == CROSSROADS:
        return RType.CROSSROAD
    if route in FORKEDROADS:
        return RType.FORKEDROAD
    if route in DEADENDS:
        return RType.DEADEND
    if route == GOAL:
        return RType.GOAL
    if route == SEEN:
        return RType.SEEN

    return RType.NONE

def routeType(i,j):
    route = mazemap[i][j]
    return routeTypeByR(route)

def replace_char(text,index,char):
    return '%s%s%s'%(text[:index],char,text[index+1:])

def setIcon():
    mazemap[position[1]] = replace_char(mazemap[position[1]],position[0],ICON)
def setSeen():
    mazemap[position[1]] = replace_char(mazemap[position[1]],position[0],SEEN)

def canPassThru(Route):
    if Route == RType.ROUTE or Route == RType.CROSSROAD or Route == RType.FORKEDROAD or Route == RType.GOAL:
        return True
    return False

def go():
    global position
    (x , y) = position
    if canPassThru(routeType(y,x+1)): #Go Right
        # print('right')
        position = (x+1,y)
    elif canPassThru(routeType(y,x-1)): #Go Left
        # print('left')
        position = (x-1,y)
    elif canPassThru(routeType(y+1,x)): #Go Down
        # print('down')
        position = (x,y+1)
    elif canPassThru(routeType(y-1,x)): #Go Up
        # print('up')
        position = (x,y-1)

def decide(navtype):
    global position,record,navhistory
    (x , y) = position

    routeList = []

    if canPassThru(routeType(y+1,x)):
        routeList.append((x,y+1))
    if canPassThru(routeType(y-1,x)):
        routeList.append((x,y-1))
    if canPassThru(routeType(y,x+1)):
        routeList.append((x+1,y))
    if canPassThru(routeType(y,x-1)):
        routeList.append((x-1,y))

    for x,y in routeList:
        if routeType(y,x) == RType.GOAL:
            position = x,y
            return

    if (len(routeList) > 1):
        record = True
        navhistory = []
        navhistory.append(routeList[0])
    for _ in range(len(routeList) - 1):
        lastWays.push(tuple(routeList[0])) # struct for (x,y)
        routeList.pop(0)

    position = routeList[0]


#Program:
while (True):
    lastRoute = mazemap[position[1]][position[0]]
    setIcon()
    print("".join(mazemap))
    setSeen()
    navtype = routeTypeByR(lastRoute)
    # print(navtype)
    # print(position)
    if isreturning:
        position = navhistory[0]
        if len(navhistory) < 2:
            position = tuple(lastWays.peek())
            isreturning = False
        navhistory.pop(0)
        # print(navhistory)


    elif navtype == RType.ROUTE:
        go()
        if record:
            navhistory.append(position)
    elif navtype == RType.CROSSROAD:
        decide(navtype)
        if record:
            navhistory.append(position)
    elif navtype == RType.FORKEDROAD:
        decide(navtype)
        if record:
            navhistory.append(position)
    elif navtype == RType.DEADEND or navtype == RType.SEEN:
        isreturning = True
        record = False
        navhistory = navhistory[::-1]
        # print(navhistory)
    elif navtype == RType.GOAL:
        break

    time.sleep(0.05)
    os.system('cls' if os.name == 'nt' else 'clear')

print("Maze Finished Succesfully!")
