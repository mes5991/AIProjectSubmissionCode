import random
import numpy as np
import queue as q

class Robot():

    def __init__(self):
        #Map information:
        #0 = empty space
        #1 = wall or object
        #2 = robot current location
        #3 = unknown value
        self.localMap = np.array([[2]])
        self.location = [0,0]
        self.goal = [0,0]
        self.goalsList = []
        self.currentPath = q.Queue()
        self.botNeighbors = []
        self.distanceTraveled = 0

    def updateRelativeData(self, di, dj):
        self.goal = [self.goal[0] + di, self.goal[1] + dj]
        goalsToBeRemoved = []
        # print("dj", dj)
        # print(self.goalsList)
        # input("goals list")
        for i in range(len(self.goalsList)):
            self.goalsList[i] = [self.goalsList[i][0] + di, self.goalsList[i][1] + dj]
            if self.localMap[self.goalsList[i][0]][self.goalsList[i][1]] != 3:
                goalsToBeRemoved.append(self.goalsList[i])
        for goal in goalsToBeRemoved:
            self.goalsList.remove(goal)
        tempPath = []
        while not self.currentPath.empty():
            tempPath.append(self.currentPath.get())
        for i in tempPath:
            self.currentPath.put([i[0] + di, i[1] + dj])

    def updateMap(self, worldLocation, envMatrix, robNum):
        # print("Robot Number", i)
        # print("Goals List", World.robots[i].goalsList)
        # input("I like turtles")
        self.botNeighbors = []
        worldNeighbors = self.getWorldNeighbors(worldLocation)
        neighborValues = []
        for neighbor in worldNeighbors:
            neighborI = neighbor[0]
            neighborJ = neighbor[1]
            neighborValue = envMatrix[neighborI][neighborJ]
            if neighborValue == 2:
                neighborValue = 0
                self.botNeighbors.append(neighbor)
            neighborValues.append(neighborValue)
        self.updateNorth(neighborValues[0])
        self.updateEast(neighborValues[1])
        self.updateSouth(neighborValues[2])
        self.updateWest(neighborValues[3], robNum)

    def updateNorth(self, neighborValue):
        if self.location[0] == 0: #if local location is at top of matrix
            self.localMap = np.insert(self.localMap, 0, 3, axis = 0) #add a row in above location
            self.location[0] += 1 #Bump robots location down the matrix by 1
            self.goal[0] += 1 #Bump current goal down the matrix by 1
            tempPath = []
            tempGoals = []
            #If the current path to the current goal is not an empty queue,
            #bump each i value up by one
            while not self.currentPath.empty():
                tempPath.append(self.currentPath.get())
            for i in tempPath:
                self.currentPath.put([i[0] + 1, i[1]])
            #Bump the i value up by one for every goal in the list of goals
            for i in range(0, len(self.goalsList)):
                self.goalsList[i][0] += 1
        self.localMap[self.location[0] - 1][self.location[1]] = neighborValue
        #If the cell above the robot is the top of the matrix, and that value is 0
        if (self.location[0] - 1 == 0) and (neighborValue == 0):
            self.localMap = np.insert(self.localMap, 0, 3, axis = 0) #Add a new row on top
            self.goal[0] += 1 #Bump goal
            self.location[0] += 1 #Bump location
            tempPath = []
            #If the current path to the current goal is not an empty queue,
            #bump each i value up by one
            while not self.currentPath.empty():
                tempPath.append(self.currentPath.get())
            tempPath.reverse()
            for i in tempPath:
                self.currentPath.put([i[0] + 1, i[1]])
            #Bump the i value up by one for every goal in the list of goals
            for i in range(0, len(self.goalsList)):
                self.goalsList[i][0] += 1

    def updateEast(self, neighborValue):
        if self.location[1] == self.localMap.shape[1] - 1:
            self.localMap = np.insert(self.localMap, self.localMap.shape[1], 3, axis = 1)
        self.localMap[self.location[0]][self.location[1] + 1] = neighborValue
        if (self.location[1] + 1 == self.localMap.shape[1] - 1) and (neighborValue == 0):
            self.localMap = np.insert(self.localMap, self.localMap.shape[1], 3, axis = 1)

    def updateSouth(self, neighborValue):
        if self.location[0] == self.localMap.shape[0] - 1:
            self.localMap = np.insert(self.localMap, self.localMap.shape[0], 3, axis = 0)
        self.localMap[self.location[0] + 1][self.location[1]] = neighborValue
        if (self.location[0] + 1 == self.localMap.shape[0] - 1) and (neighborValue == 0):
            self.localMap = np.insert(self.localMap, self.localMap.shape[0], 3, axis = 0)

    def updateWest(self, neighborValue, robNum):
        bumpCount = 0
        if self.location[1] == 0:
            self.localMap = np.insert(self.localMap, 0, 3, axis = 1)
            self.location[1] += 1
            self.goal[1] += 1
            tempPath = []
            tempGoals = []
            while not self.currentPath.empty():
                tempPath.append(self.currentPath.get())
            for i in tempPath:
                self.currentPath.put([i[0], i[1] + 1])
            for i in range(0, len(self.goalsList)):
                self.goalsList[i][1] += 1
        self.localMap[self.location[0]][self.location[1] - 1] = neighborValue
        if (self.location[1] - 1 == 0) and (neighborValue == 0):
            self.localMap = np.insert(self.localMap, 0, 3, axis = 1)
            self.location[1] += 1
            self.goal[1] += 1
            tempPath = []
            while not self.currentPath.empty():
                tempPath.append(self.currentPath.get())
            tempPath.reverse()
            for i in tempPath:
                self.currentPath.put([i[0], i[1] + 1])
            # print('goals list:', self.goalsList)
            for i in range(0, len(self.goalsList)):
                self.goalsList[i][1] += 1
            # print('robot number:', robNum)
            # print('goals list:', self.goalsList)
            # input('waiting')

    def getWorldNeighbors(self, worldLocation):
        worldNeighbors = [[worldLocation[0] - 1, worldLocation[1]],
                          [worldLocation[0], worldLocation[1] + 1],
                          [worldLocation[0] + 1, worldLocation[1]],
                          [worldLocation[0], worldLocation[1] - 1]]
        return worldNeighbors

    def move(self, newLocation):
        self.localMap[self.location[0]][self.location[1]] = 0
        self.location = newLocation
        self.localMap[self.location[0]][self.location[1]] = 2
        self.distanceTraveled += 1

    def getGoals(self):
        #Get neighbors of current location
        # print(self.localMap)
        # input("in get goals")
        neighbors = [[self.location[0] - 1, self.location[1]],
                     [self.location[0], self.location[1] + 1],
                     [self.location[0] + 1, self.location[1]],
                     [self.location[0], self.location[1] - 1]]

        for neighbor in neighbors:
            #Check if neighbor is within map range and not in visited cells
            iRange = (neighbor[0] >= 0) and (neighbor[0] <= (self.localMap.shape[0] - 1))
            jRange = (neighbor[1] >= 0) and (neighbor[1] <= (self.localMap.shape[1] - 1))
            if (iRange) and (jRange):
                #Check if neighbor value is 0 which ensures a path to the potential goal
                if (self.localMap[neighbor[0]][neighbor[1]] == 0):
                    #Get neighbors of the current neighbor
                    neighborsOfNeighbors = [[neighbor[0] - 1, neighbor[1]],
                                            [neighbor[0], neighbor[1] + 1],
                                            [neighbor[0] + 1, neighbor[1]],
                                            [neighbor[0], neighbor[1] - 1]]
                    # print(neighborsOfNeighbors)
                    # input('for loop')
                    for neighborNeighbor in neighborsOfNeighbors:

                        #Check if neighbor of neighbor is within map range
                        iRange = (neighborNeighbor[0] >= 0) and (neighborNeighbor[0] <= (self.localMap.shape[0] - 1))
                        jRange = (neighborNeighbor[1] >= 0) and (neighborNeighbor[1] <= (self.localMap.shape[1] - 1))
                        if (iRange) and (jRange):
                            #Check if neighbor of neighbor is of value 3 ensuring that it has not been discovered yet
                            # if (self.localMap[neighborNeighbor[0]][neighborNeighbor[1]] == 3) and (neighborNeighbor not in self.goalsPut):
                            if (self.localMap[neighborNeighbor[0]][neighborNeighbor[1]] == 3) and (neighborNeighbor not in self.goalsList):
                                # print(neighborNeighbor)
                                # input('adding goal')
                                self.goalsList.append(neighborNeighbor)
                                #Add neighbor of neighbor and path to goals queue
                                # self.goalsPut.append(neighborNeighbor)
                                # self.goals.put(neighborNeighbor)
    def getNextGoalGreedyAStar(self):
        currentGoals = []
        currentDiscovery = 0
        for goal in self.goalsList:
            di = abs(self.location[0] - goal[0])
            dj = abs(self.location[1] - goal[1])
            if (di <= 2) and (dj <= 2):
                Search = searchAStar(self.location, goal, self.localMap)
                solution = Search.solve()
                discovery = 0
                if solution != None:
                    for step in solution:
                        neighbors = [[goal[0] - 1, goal[1]],
                                     [goal[0], goal[1] + 1],
                                     [goal[0] + 1, goal[1]],
                                     [goal[0], goal[1] - 1]]
                        for neighbor in neighbors:
                            iRange = (neighbor[0] >= 0) and (neighbor[0] <= (self.localMap.shape[0] - 1))
                            jRange = (neighbor[1] >= 0) and (neighbor[1] <= (self.localMap.shape[1] - 1))
                            if (iRange) and (jRange):
                                if self.localMap[neighbor[0]][neighbor[1]] == 3:
                                    discovery += 1
                    if len(currentGoals) == 0:
                        currentGoals = [goal]
                        currentDiscovery = discovery
                    elif currentDiscovery < discovery:
                        currentGoals = [goal]
                        currentDiscovery = discovery
                    elif currentDiscovery == discovery:
                        currentGoals.append(goal)
                else:
                    return self.getNextGoalManhattan()
        if len(currentGoals) == 0:
            return self.getNextGoalManhattan()
        if len(currentGoals) > 1:
            manhattan = None
            currentGoal = None
            for goal in currentGoals:
                di = abs(goal[0] - self.location[0])
                dj = abs(goal[1] - self.location[1])
                if (manhattan == None) or (di + dj < manhattan):
                    manhattan = di + dj
                    currentGoal = goal
        else:
            currentGoal = currentGoals[0]
        self.goalsList.remove(currentGoal)
        return currentGoal



    def getNextGoalGreedy(self):
        greedyMin = 0
        greedyGoals = []
        for goal in self.goalsList:
            greedyCount = 0
            neighbors = [[goal[0] - 1, goal[1]],
                         [goal[0], goal[1] + 1],
                         [goal[0] + 1, goal[1]],
                         [goal[0], goal[1] - 1]]
            for neighbor in neighbors:
                iRange = (neighbor[0] >= 0) and (neighbor[0] <= (self.localMap.shape[0] - 1))
                jRange = (neighbor[1] >= 0) and (neighbor[1] <= (self.localMap.shape[1] - 1))
                if (iRange) and (jRange):
                    if self.localMap[neighbor[0]][neighbor[1]] == 3:
                        greedyCount += 1
            if len(greedyGoals) == 0:
                greedyGoals.append(goal)
                greedyMin = greedyCount
            elif greedyMin < greedyCount:
                greedyGoals = [goal]
                greedyMin = greedyCount
            elif greedyMin == greedyCount:
                greedyGoals.append(goal)
        if len(greedyGoals) > 1:
            manhattan = None
            currentGoal = None
            for goal in greedyGoals:
                di = abs(goal[0] - self.location[0])
                dj = abs(goal[1] - self.location[1])
                if (manhattan == None) or (di + dj < manhattan):
                    manhattan = di + dj
                    currentGoal = goal
        else:
            currentGoal = greedyGoals[0]
        self.goalsList.remove(currentGoal)
        return currentGoal

    def getNextGoalManhattan(self):
        #Initilize temporary manhattan distance and goal selection
        manhattan = None
        currentGoal = None
        #Use manhattan distance to select the closest goal
        for goal in self.goalsList:
            di = abs(goal[0] - self.location[0])
            dj = abs(goal[1] - self.location[1])
            if (manhattan == None) or (di + dj < manhattan):
                manhattan = di+dj
                currentGoal = goal
        #Remove the selected goal from the goals list
        self.goalsList.remove(currentGoal)
        return currentGoal


class searchAStar():

    def __init__(self, initialState, goalState, localMap):
        self.goalState = goalState
        self.state = initialState
        self.localMap = localMap
        self.pathCostAccumulated = {str(initialState) : 0}
        self.cameFrom = {str(initialState) : 0}
        self.frontier = q.PriorityQueue()

    def solve(self):
        while True:
            if self.state == self.goalState:
                return self.getPath()
            children = self.getLegalMoves()
            self.expandFrontier(children)
            if not self.frontier.empty():
                self.state = self.frontier.get()[1]
            else:
                return None
            self.pathCostAccumulated[str(self.state)] = self.pathCostAccumulated[str(self.cameFrom[str(self.state)])] + 1

    def getPath(self):
        reversePath = []
        path = []
        while self.cameFrom[str(self.state)] != 0:
            reversePath.append(self.state)
            self.state = self.cameFrom[str(self.state)]
        for i in reversed(reversePath):
            path.append(i)
        return path

    def getLegalMoves(self):
        relativeNeighbors = [[self.state[0] - 1, self.state[1]],
                             [self.state[0], self.state[1] + 1],
                             [self.state[0] + 1, self.state[1]],
                             [self.state[0], self.state[1] - 1]]
        legalMoves = []
        for neighbor in relativeNeighbors:
            iCheck = (neighbor[0] >= 0) and (neighbor[0] <= self.localMap.shape[0] - 1)
            jCheck = (neighbor[1] >= 0) and (neighbor[1] <= self.localMap.shape[1] - 1)
            if iCheck and jCheck:
                if (self.localMap[neighbor[0]][neighbor[1]] == 0) or (self.localMap[neighbor[0]][neighbor[1]] == 3):
                    legalMoves.append(neighbor)
        return legalMoves

    def expandFrontier(self, children):
        for i in range(0, len(children)):
            if str(children[i]) not in self.cameFrom:
                self.cameFrom[str(children[i])] = self.state
                h = self.manhattan(children[i])
                g = self.pathCostAccumulated[str(self.state)] + 1
                self.frontier.put((h + g, children[i]))

    def manhattan(self, child):
        di = abs(self.goalState[0] - child[0])
        dj = abs(self.goalState[1] - child[1])
        return di + dj
