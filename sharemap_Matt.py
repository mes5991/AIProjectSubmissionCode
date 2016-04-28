import numpy as np

def shareMap(botA_Map, botB_Map, direction):
    # print("botA_Map\n", botA_Map)
    # print("botB_Map\n", botB_Map)
    """Get robots local locations. Note frame references"""
    botA_wrtA = [np.where(botA_Map==2)[0], np.where(botA_Map==2)[1]]
    botB_wrtA = [botA_wrtA[0] + direction[0], botA_wrtA[1] + direction[1]]
    botB_wrtB = [np.where(botB_Map==2)[0], np.where(botB_Map==2)[1]]

    """Use frame difference to insert rows or columns into the respective map"""
    frameDifference = [botB_wrtA[0] - botB_wrtB[0], botB_wrtA[1] - botB_wrtB[1]]
    if frameDifference[0] > 0: #Insert row(s) into bot B
        for i in range(abs(int(frameDifference[0]))):
            botB_Map = np.insert(botB_Map, 0, 3, axis = 0)
    elif frameDifference[0] < 0: #Insert row(s) into bot A
        for i in range(abs(int(frameDifference[0]))):
            botA_Map = np.insert(botA_Map, 0, 3, axis = 0)
    if frameDifference[1] > 0: #Insert column(s) into bot B
        for i in range(abs(int(frameDifference[1]))):
            botB_Map = np.insert(botB_Map, 0, 3, axis = 1)
    elif frameDifference[1] < 0: #Insert column(s) into bot A
        for i in range(abs(int(frameDifference[1]))):
            botA_Map = np.insert(botA_Map, 0, 3, axis = 1)

    # print("botA_Map\n", botA_Map)
    # print("botB_Map\n", botB_Map)
    # input("waiting")

    """Get map sizes and size difference"""
    botA_size = botA_Map.shape
    botB_size = botB_Map.shape
    sizeDifference = [botA_size[0] - botB_size[0], botA_size[1] - botB_size[1]]

    """Use size difference to append rows or columns into the respective map"""
    if sizeDifference[0] > 0: #Append row(s) onto bot B
        for i in range(abs(int(sizeDifference[0]))):
            botB_Map = np.insert(botB_Map, botB_Map.shape[0], 3, axis = 0)
    elif sizeDifference[0] < 0: #Append row(s) onto bot A
        for i in range(abs(int(sizeDifference[0]))):
            botA_Map = np.insert(botA_Map, botA_Map.shape[0], 3, axis = 0)
    if sizeDifference[1] > 0: #Append col(s) onto bot B
        for i in range(abs(int(sizeDifference[1]))):
            botB_Map = np.insert(botB_Map, botB_Map.shape[1], 3, axis = 1)
    if sizeDifference[1] < 0: #Append col(s) onto bot A
        for i in range(abs(int(sizeDifference[1]))):
            botA_Map = np.insert(botA_Map, botA_Map.shape[1], 3, axis = 1)

    """Maps are now the same size. They now need to merge together"""
    for i in range(botA_Map.shape[0]):
        for j in range(botA_Map.shape[1]):
            botA_bool = botA_Map[i][j] == 3
            botB_bool = botB_Map[i][j] == 3
            if (botA_bool) and (not botB_bool):
                botA_Map[i][j] = botB_Map[i][j]
            elif (not botA_bool) and (botB_bool):
                botB_Map[i][j] = botA_Map[i][j]

    botA_location = [np.where(botA_Map==2)[0][0], np.where(botA_Map==2)[1][0]]
    botB_location = [np.where(botB_Map==2)[0][0], np.where(botB_Map==2)[1][0]]
    return(botA_Map, botB_Map, botA_location, botB_location)
