import numpy as np

def shareMap(robot1,robot2,dir1):
    item=2 # Location of the other robot

    #arr1=robot1().localMap
    #arr2=robot2().localMap
    #if (dir1==2 and dir2==0) or (dir1==0 and dir2==2):

    # Assigns arrays according to relative locations of robot
    if dir1[0]==1 and dir1[1]==0:
        arr1=robot1
        arr2=robot2


    elif dir1[0]==-1 and dir1[1]==0:
        arr1=robot2
        arr2=robot1

    elif dir1[0]==0 and dir1[1]==1:
        arr1=np.transpose(robot1)
        arr2=np.transpose(robot2)

    elif dir1[0]==0 and dir1[1]==-1:
        arr1=np.transpose(robot2)
        arr2=np.transpose(robot1)


    index1=np.where(arr1==2)
    index2=np.where(arr2==2)
    arr1[index1[0][0]][index1[1][0]]=0
    arr1[index1[0][0]+1][index1[1][0]]=2
    arr2[index2[0][0]][index2[1][0]]=0
    arr2[index2[0][0]-1][index2[1][0]]=2
    # 1 Ignore this comment
    #print("Adjusted 2 Array1\n",arr1)
    #print("Adjusted 2 Array2\n",arr2)
    size1=arr1.shape
    size2=arr2.shape
    # 2 Ignore this comment
    sizcol=abs(size1[1]-size2[1])
    #print(size1[1])
    # 3 Ignore this comment

    # Reshaping matrices for convenience
    itemindex1=np.where(arr1==item)
    itemindex2=np.where(arr2==item)
    if size2[1]>size1[1]:
        for n in range(itemindex2[1][0]-itemindex1[1][0]):
            arr1 = np.insert(arr1,0,3,1)
        for n in range((size2[1]-(itemindex2[1][0]+1))-(size1[1]-(itemindex1[1][0]+1))):
            arr1 = np.insert(arr1,size1[1],3,1)
    #print("Array1 col adjusted\n",arr1)
    if size1[1]>size2[1]:
        for n in range(itemindex1[1][0]-itemindex2[1][0]):
            arr2 = np.insert(arr2,0,3,1)
        #print("check",(size1[1]-(itemindex1[1][0]+1))-(size2[1]-(itemindex2[1][0]+1)))
        for n in range((size1[1]-(itemindex1[1][0]+1))-(size2[1]-(itemindex2[1][0]+1))):
            arr2 = np.insert(arr2,size2[1],3,1)
    #print("Array2 col adjusted\n",arr2)
    itemindex1=np.where(arr1==item)
    itemindex2=np.where(arr2==item)
    #print((itemindex1[0][0],itemindex1[1][0]),(itemindex2[0][0],itemindex2[1][0]))
    nsize1=arr1.shape
    #print(nsize1[1])
    nsize2=arr2.shape
    #print(nsize1,nsize2)
    #print(itemindex2[0][0])

    # Sharing Information Part1
    for i in range((itemindex2[0][0]+2) if (itemindex2[0][0]>itemindex1[0][0]) else (itemindex1[0][0]+1)):
        for j in range(nsize1[1]):
            #print(i)
            if (itemindex1[0][0]-i)<0:
                arr1=np.insert(arr1,0,arr2[itemindex2[0][0]+(1-i)],0)
                itemindex1[0][0]+=1
                #print("1",i,j)
                break
            elif (itemindex2[0][0]+(1-i))<0:
                arr2=np.insert(arr2,0,arr1[itemindex1[0][0]-i],0)
                itemindex2[0][0]+=1
                #print("2",i,j)
                #print("arrays at break",arr1,arr2)
                break
            elif arr1[itemindex1[0][0]-i][j]==3 and (itemindex1[0][0]-i)>=0:
                arr1[itemindex1[0][0]-i][j]=arr2[itemindex2[0][0]+(1-i)][j]
                #print("arr1",i,j,arr1)
            elif arr2[itemindex2[0][0]+(1-i)][j]==3 and (itemindex2[0][0]+(1-i))>=0:
                arr2[itemindex2[0][0]+(1-i)][j]=arr1[itemindex1[0][0]-i][j]
                #print("arr2",i,j,arr2)
    # Sharing Information Part2
    itemindex1=np.where(arr1==item)
    itemindex2=np.where(arr2==item)
    nsize1=arr1.shape
    nsize2=arr2.shape
    sizdiff1=nsize1[0]-(itemindex1[0][0]+1)
    sizdiff2=nsize2[0]-(itemindex2[0][0]+2)
    #print("nsize",nsize2[0])
    itemindex1=np.where(arr1==item)
    itemindex2=np.where(arr2==item)
    #print(sizdiff1,sizdiff2)
    sizdiff=sizdiff1 if sizdiff1>=sizdiff2 else sizdiff2
    #print("arrays entering part2",arr1,arr2)
    #print(itemindex1[0][0],itemindex2[0][0])
    for i in range(sizdiff):
        for j in range(nsize1[1]):
            if i>(sizdiff1-1):
                arr1=np.insert(arr1,(itemindex1[0][0]+1+i),arr2[itemindex2[0][0]+2+i],0)
                #print("arr at break",i,j,arr1,arr2)
                break
            elif i>(sizdiff2-1):
                arr2=np.insert(arr2,(itemindex2[0][0]+2+i),arr1[itemindex1[0][0]+1+i],0)
                #print("arr at break",i,j,arr1,arr2)
                break
            elif arr1[itemindex1[0][0]+1+i][j]==3:
                arr1[itemindex1[0][0]+1+i][j]=arr2[itemindex2[0][0]+2+i][j]
                #print("arr at break",i,j,arr1)
            elif arr2[itemindex2[0][0]+2+i][j]==3:
                arr2[itemindex2[0][0]+2+i][j] = arr1[itemindex1[0][0]+1+i][j]
                #print("arr at break",i,j,arr2)
    #print("Share info part2 Array1\n",arr1)
    #print("Share info part2 Array2\n",arr2)
    loc1=np.where(arr1==item)
    loc2=np.where(arr2==item)
    # Return Values
    if dir1[0]==1 and dir1[1]==0:
        return arr2,arr1,[loc2[0][0],loc2[1][0]],[loc1[0][0],loc1[1][0]]
    elif dir1[0]==-1 and dir1[1]==0:
        return arr1,arr2,[loc1[0][0],loc1[1][0]],[loc2[0][0],loc2[1][0]]
    elif dir1[0]==0 and dir1[1]==1:
        return np.transpose(arr2),np.transpose(arr1),[loc2[1][0],loc2[0][0]],[loc1[1][0],loc1[0][0]]
    elif dir1[0]==0 and dir1[1]==-1:
        return np.transpose(arr1),np.transpose(arr2),[loc1[1][0],loc1[0][0]],[loc2[1][0],loc2[0][0]]
    # 4 Ignore this comment

# Test the code
# Uncomment to test the following case
'''robot1=np.array([[0,1,3,3],[0,0,0,0],[1,1,0,3],[3,3,2,3],[0,0,0,0],[3,3,3,1],[3,3,3,3],[0,0,0,1]])
robot2=np.array([[0,0,0,0],[0,0,2,0],[1,1,0,3],[1,1,1,1]])
(array1,array2,loc1,loc2)=shareMap(robot1,robot2,[1,0])
print("Array1\n",array1,loc1)
print("Array2\n",array2,loc2)'''

# Uncomment to test the following case
'''robot1=np.array([[0,1,3,3],[0,0,0,0],[1,1,2,0],[3,1,0,3],[0,0,1,0]])
robot2=np.array([[1,3,0,0],[0,3,0,0],[1,0,2,0],[1,0,1,0]])
#print(robot1,robot2)
(array1,array2,loc1,loc2)=shareMap(robot1,robot2,[0,1])
print("Array1\n",array1,loc1)
print("Array2\n",array2,loc2)'''

# Uncomment to test the following case
'''robot1=np.array([[3,3,3,3,3],[3,3,0,3,3],[3,0,2,0,3],[3,0,0,0,3],[3,3,0,3,3],[3,3,3,3,3]])
robot2=np.array([[3,3,1,1,1,3,3],[3,0,0,0,2,0,3],[3,3,0,0,0,3,3],[3,3,3,3,3,3,3]])
print("Robot1\n",robot1)
print("Robot2\n",robot2)
(array1,array2,loc1,loc2)=shareMap(robot1,robot2,[-1,0])
print("Array1\n",array1,loc1)
print("Array2\n",array2,loc2)'''

# Uncomment to test the following case
'''robot1=np.array([[3,3,1,1,3,3],[3,0,0,2,0,3],[3,0,0,0,3,3],[3,0,0,0,3,3],[3,0,0,0,3,3],[3,0,0,0,3,3],[3,3,0,3,3,3],[3,3,3,3,3,3]])
robot2=np.array([[3,3,1,1,1,3,],[3,0,2,0,0,1],[3,3,0,0,0,1],[3,3,3,0,0,1],[3,3,3,3,0,3],[3,3,3,3,3,3]])
#robot1=np.transpose(robot1)
#robot2=np.transpose(robot2)
print("Robot1\n",robot1)
print("Robot2\n",robot2)
(array1,array2,loc1,loc2)=shareMap(robot1,robot2,[0,1])
print("Array1\n",array1,loc1)
print("Array2\n",array2,loc2)'''

