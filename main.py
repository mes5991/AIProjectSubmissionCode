from environment import Environment
from robot import searchAStar
import random
import queue as q
import numpy as np
from sharemap_Matt import shareMap
import copy
import pygame
from sys import exit
import csv

"""Code below this line is code for multi-robot search"""
for run in range(10):
    np.set_printoptions(threshold = np.nan, suppress = True, linewidth = 300)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 25, 250)
    RED = (255, 0, 0)
    PURPLE = (160, 32, 240)


    worldSize = (50, 50)
    wallPerc = 0.3
    robotCount = 20
    newInfo = []
    stuck = []
    chosenLocations = False
    done = False
    trace = False
    render = False
    importWorld = False
    loopCount = 0
    shareCount = 0
    firstFinish = 0
    pygame.init()

    if render:
        infoObject = pygame.display.Info()
        screen1 = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        screen1.fill(WHITE)
        pygame.display.set_caption("Simulation")
        z = worldSize[0] / 20  # set the scaling factor based on screen size
        y = worldSize[0] / 20

    if importWorld:
        envFile = 'C:/Users/Matthew/Documents/WPI/Spring 16/AI/Project/AI-Project/map50.csv'
        with open(envFile, 'r') as dest_f:
            data_iter = csv.reader(dest_f, delimiter = ',', quotechar = '"')
            data = [data for data in data_iter]
        env = np.asarray(data)
        env = env.astype(np.int)
        World = Environment(worldSize, wallPerc, robotCount, env)
    else:
        World = Environment(worldSize, wallPerc, robotCount)
    # print("World Map:\n", World.envMatrix)
    for i in range(len(World.robots)):
        World.robots[i].updateMap(World.robotsLocation[i], World.envMatrix, i)
        World.robots[i].getGoals()
        newInfo.append(False)
        stuck.append(False)
        # print("Local Map", i,"\n", World.robots[i].localMap)

    def renderMap(mapMatrix, worldMatrixSize, k=None):
        for i in range(mapMatrix.shape[0]):
            for j in range(mapMatrix.shape[1]):
                m = i * z
                n = j * z
                if k != None:
                    m = i * y
                    n = j * y
                    if k > 2:
                        m += (z * worldMatrixSize[1] * (k - 3))
                        n += (z * worldMatrixSize[0])
                    else:
                        m += (z * worldMatrixSize[1] * (k + 1))
                    if mapMatrix[i, j] == 1.0:
                        pygame.draw.rect(screen1, BLACK, [m, n, y, y])
                    elif mapMatrix[i, j] == 2.0:
                        pygame.draw.rect(screen1, PURPLE, [m, n, y, y])
                    elif mapMatrix[i, j] == 3.0:
                        pygame.draw.rect(screen1, BLUE, [m, n, y, y])
                    else:
                        pygame.draw.rect(screen1, WHITE, [m, n, y, y])
                elif mapMatrix[i, j] == 1.0:
                    pygame.draw.rect(screen1, BLACK, [m, n, z, z])
                elif mapMatrix[i, j] == 2.0:
                    pygame.draw.rect(screen1, PURPLE, [m, n, z, z])
                elif mapMatrix[i, j] == 3.0:
                    pygame.draw.rect(screen1, BLUE, [m, n, z, z])
                else:
                    pygame.draw.rect(screen1, WHITE, [m, n, z, z])
        pygame.display.flip()
        # --- Limit to frames per second
        clock = pygame.time.Clock()
        clock.tick(200000)


    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #Run loop while any robots are not stuck
        while (False in stuck):
            if (firstFinish == 0) and (True in stuck):
                firstFinish = loopCount
            loopCount += 1
            for i in range(len(World.robots)):

                """Goals Update"""
                #If the current goal is no longer unknown, get new goal. Goal initializes as origin.
                if (World.robots[i].localMap[World.robots[i].goal[0]][World.robots[i].goal[1]] != 3) or newInfo[i]:
                    legalGoal = False
                    while not legalGoal and not stuck[i]:
                        #Are there any remaining goals?
                        if len(World.robots[i].goalsList) > 0:
                            #Do we have new info but havnt reached the current goal?
                            if not newInfo[i]:
                                #Get new goal from goals list
                                # World.robots[i].goal = World.robots[i].getNextGoalManhattan()
                                # World.robots[i].goal = World.robots[i].getNextGoalGreedyAStar()
                                World.robots[i].goal = World.robots[i].getNextGoalGreedy()
                            newInfo[i] = False
                            #Is the current goal still unknown?
                            if World.robots[i].localMap[World.robots[i].goal[0]][World.robots[i].goal[1]] == 3:
                                #A* search to get path to goal
                                Search0 = searchAStar(World.robots[i].location, World.robots[i].goal, World.robots[i].localMap)
                                solution = Search0.solve()
                                World.robots[i].currentPath = q.Queue()
                                for step in solution:
                                    World.robots[i].currentPath.put(step)
                                    legalGoal = True
                        else:
                            #If no remaining goals, consider the robot stuck
                            stuck[i] = True

                """Movement update"""
                if not stuck[i]:
                    #Get the next move from the current path
                    nextMove = World.robots[i].currentPath.get()
                    #Only move to the next location if it is empty
                    if World.robots[i].localMap[nextMove[0]][nextMove[1]] == 0:
                        #Get direction of movement [0,1], [0,-1], [1,0], [-1,0]
                        direction = [nextMove[0] - World.robots[i].location[0], nextMove[1] - World.robots[i].location[1]]
                        #Move in local map
                        World.robots[i].move(nextMove)
                        #Move in world map
                        World.updateEnvMatrix(i, direction)
                        #Update local map with new sensor information
                        World.robots[i].updateMap(World.robotsLocation[i], World.envMatrix, i)
                        """Share Map Functions"""
                        for botNeighbor in World.robots[i].botNeighbors:
                            shareCount += 1
                            #get direction of neighbor bot wrt current bot
                            direction = [botNeighbor[0] - World.robotsLocation[i][0], botNeighbor[1] - World.robotsLocation[i][1]]
                            #get neighbor bot index and local map for sharing
                            (neighborMap, neighborIndex) = World.getSharingInfo(i, direction)
                            #Store old relative locations
                            oldBotLocalLocation = World.robots[i].location
                            oldNeighborLocalLocation = World.robots[neighborIndex].location
                            #Share map information. Directly modify robot maps and locations if necessary
                            (World.robots[i].localMap, World.robots[neighborIndex].localMap, World.robots[i].location, World.robots[neighborIndex].location) = shareMap(World.robots[i].localMap, neighborMap, direction)
                            #Get change in location from before map sharing to after map sharing
                            (bot_di, bot_dj) = (abs(oldBotLocalLocation[0] - World.robots[i].location[0]), abs(oldBotLocalLocation[1] - World.robots[i].location[1]))
                            (neighbor_di, neighbor_dj) = (abs(oldNeighborLocalLocation[0] - World.robots[neighborIndex].location[0]), abs(oldNeighborLocalLocation[1] - World.robots[neighborIndex].location[1]))
                            #Update goal, goals list, and current path according to the change in location
                            World.robots[i].updateRelativeData(bot_di, bot_dj)
                            World.robots[neighborIndex].updateRelativeData(neighbor_di, neighbor_dj)
                            #Combine goals list into one mutual goal list
                            mutualGoalList = []
                            for goal in World.robots[i].goalsList:
                                if goal not in mutualGoalList:
                                    mutualGoalList.append(goal)
                            for goal in World.robots[neighborIndex].goalsList:
                                if goal not in mutualGoalList:
                                    mutualGoalList.append(goal)
                            World.robots[i].goalsList = copy.deepcopy(mutualGoalList)
                            World.robots[neighborIndex].goalsList = copy.deepcopy(mutualGoalList)
                        #Get new goals based on the previous movement
                        World.robots[i].getGoals()
                        # if len(World.robots[i].botNeighbors) > 0:
                        #     if len(World.robots[i].goalsList) > 0:
                        #         World.robots[i].goal = random.choice(World.robots[i].goalsList)
                        #     newInfo[i] = True
                        #     World.robots[i].botNeighbors = []
                        if render and i == 0:
                            renderMap(World.robots[i].localMap, World.envMatrix.shape, i)
                    else:
                        #If the next move is not empty, ignore the above code, and run A* again.
                        newInfo[i] = True
            if trace:
                print("World Map:\n", World.envMatrix)
                for i in range(len(World.robots)):
                    print("Local Map", i,"\n", World.robots[i].localMap)
                input('waiting')
            if render:
                renderMap(World.envMatrix, World.envMatrix.shape)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        done = True
    # print("World Map:\n", World.envMatrix)
    # for i in range(len(World.robots)):
    #     print("Local Map", i,"\n", World.robots[i].localMap)
    print("run", run)
    print("robotCount", robotCount)
    print("loopCount", loopCount)
    print("firstFinish", firstFinish)
    print("shareCount", shareCount)
    distanceTraveled = []
    total = 0
    for i in range(len(World.robots)):
        distanceTraveled.append(World.robots[i].distanceTraveled)
        total += distanceTraveled[i]
    print("maxDistanceTraveled", max(distanceTraveled))
    print("aveDistanceTraveled", total/robotCount)
    print()
