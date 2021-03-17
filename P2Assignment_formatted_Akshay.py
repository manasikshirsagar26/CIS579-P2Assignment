#######################################################
# CIS 579: Artificial Intelligence
# Name: Manasi Kshirsagar
# UMID- 05494807
# Instructor: Prof. Shengquan Wang
# Semester: Winter 2021 
# P2 assignment: Hidden Markov Models
#######################################################

# Import required packages
import os
import numpy as np
import copy
from operator import itemgetter

# ####################################################



# ### To find the allowed possitions

def allowedPos(row,col):
    #originalPath=[]
    allowedPosition=[]
    #allowedPath=[]
    '''
    ## Westwards
    if ((y == 0 and x >=0) or \
        (x == 1 and y == 2) or \
        (x == 1 and y == 5) or \
        (x == 3 and y == 2) or \
        (x == 3 and y == 5)):
        allowedPath.append(1)
    else:
        allowedPath.append(0)
    
    ## Northwards
    if ((x==0 and y >=0) or \
        (x==2 and y== 1) or \
        (x == 2 and y == 4) or \
        (x == 4 and y == 1) or \
        (x == 4 and y == 4)):
        allowedPath.append(1)
    else:
        allowedPath.append(0)

    ## Eastwards
    if ((x == 1 and y == 0) or \
        (x == 1 and y == 3) or \
        (x>=0 and y == 6) or \
        (x == 3 and y == 0) or \
        (x == 3 and y == 3) ):
        allowedPath.append(1)
    else:
        allowedPath.append(0)
    
    ## Southwards
    if ((x == 0 and y == 1) or \
        (x == 0 and y == 4) or \
        (x == 2 and y == 1) or \
        (x == 2 and y== 4) or \
        (x== 5 and y>=0)):
        allowedPath.append(1)
    else:
        allowedPath.append(0)
    print("Allowed Path:", allowedPath)
    '''
    if(row in [0,2,4,5] and col >=1) or (row in [1,3] and col in [3,6]):
        allowedPosition.append(0)
    else:
        allowedPosition.append(1)

    #Northwards
    if(row in (1,2,3,4) and col in (0,2,3,5,6)) or (row == 5 and col >=0):
        allowedPosition.append(0)
    else:
        allowedPosition.append(1)

    #Eastwards
    if(row in (0,2,4,5) and col <6) or (row in (1,3) and col in(2,5)):
        allowedPosition.append(0)
    else:
        allowedPosition.append(1)


    #Southwards
    if(row in (0,1,2,3) and col in (0,2,3,5,6)) or (row == 4 and col <=6):
        allowedPosition.append(0)
    else:
        allowedPosition.append(1)
   
    #return allowedPath
    return allowedPosition

### To find the location based on given evidence

def sensorEvidence(pathEvidence,moveMatrix):
    detectObstacle= 0.8
    notdetectObstacle = 1.0 - detectObstacle
    errorOpenSq_Obstacle = 0.15
    detectOpenSq = 1- errorOpenSq_Obstacle

    perCellProbability =[]
    alldirectionsum=[]
    nextPath=pathEvidence

    row=[0,1,2,3,4,5]
    cols=[0,1,2,3,4,5,6]

    for x in [0,1,2,3,4,5]:
        for y in [0,1,2,3,4,5,6]:
            currentPath=allowedPos(x,y)

            perCellProbAllDirection=[]
            totalProbAllDirection=[]

            if((x==1 and y==1) or (x==1 and y==4) or \
                (x==3 and y==1 ) and (x==3 and y==4)):
                perCellProbAllDirection.append(0)
            else:
                for k in [0,1,2,3]:
                    if(currentPath[k]==1 and nextPath[k]==1):
                        perCellProbAllDirection.append(detectObstacle)
                    if(currentPath[k]==0 and nextPath[k]==0):
                        perCellProbAllDirection.append(detectOpenSq)
                    if(currentPath[k]==0 and nextPath[k]==1):
                        perCellProbAllDirection.append(errorOpenSq_Obstacle)
                    if(currentPath[k]==1 and nextPath[k]==0):
                        perCellProbAllDirection.append(notdetectObstacle)
            print("perCellProbAllDirection:", perCellProbAllDirection)
            print("move matrix X, Y: ",moveMatrix[x,y] )
            totalProbAllDirection=((np.prod(perCellProbAllDirection)*moveMatrix[x,y]).round(4))
            print("haha:",totalProbAllDirection)

            alldirectionsum.append(totalProbAllDirection)

    sensor_probability = []
    for v in alldirectionsum:
        sensor_probability.append(float(((v*100)/np.sum(alldirectionsum)).round(2)))

    evidenceProb = sensor_probability

    evidenceMatrix=np.matrix(evidenceProb).reshape(6,7)
    return evidenceMatrix


## To find Prediction for next step
def move(previousStep,evidenceMatrix,moveDirection):
    row=[1,2,3,4,5,6]
    cols=[1,2,3,4,5,6,7]
    motionProb=[]

    if(moveDirection=='North'):
        
        for x in [0,1,2,3,4,5]:
            for y in [0,1,2,3,4,5,6]:
                if((x==1 and y==1) or (x==1 and y==4) or \
                    (x==3 and y==1 ) and (x==3 and y==4)):
                    motionProbPerCell=0
                    motionProb.append(motionProbPerCell)
                    continue
                else:
                    probCalc=[]
                    nextPath=[]
                    nextmove=()

                    ## get the target position
                    ## from west
                    # If boundary
                    if (x in range(0,7) and y-1<0) or \
                        (x==1 and y-1 ==1) or (x==1 and y-1==4) or \
                        (x==3 and y-1==1) or (x==3 and y-1==4):
                        nextmove=(x,y)
                    elif(x in range (0,7) and y-1>=0):
                        nextmove=(x,y-1)
                    nextPath.append(nextmove)

                    ## from North
                    if ( x in range (0,6) and y in range(0,7)):
                        nextmove=(x,y)
                    nextPath.append(nextmove)

                    ## from east
                    if (x in range (0,7) and y+1>=7) or \
                        (x==1 and y+1==1) or (x==1 and y+1==4) or \
                        (x==3 and y+1==1) or (x==3 and y+1==4):
                        nextmove=(x,y)
                    elif(x in range(0,7) and y+1<=6):
                        nextmove=(x,y+1)
                    nextPath.append(nextmove)

                    ## from south
                    if (x+1>=6 and y in range(0,7)) or \
                        (x+1==3 and  y==4) or (x+1==3 and y==1) or \
                        (x+1==1 and y==1) or (x+1==1 and y==4):
                        nextmove=(x,y)
                    elif(x+1<6 and y in range(0,7)) or (x<=5 and y in range(0,7)):
                        nextmove=(x+1,y)

                    nextPath.append(nextmove)
                    print(nextPath)
                    ### get the target values
                    targetProb=[]

                    #from west
                    if (x in range(0,7)):
                        targetProb.append(0.1)
                    
                    ## from North
                    if (x==0 and y in range(0,7)) or \
                        (x-1==1 and y ==1) or (x-1==1 and y==4) or \
                        (x-1==3 and y==1) or (x-1==3 and y==4):
                        targetProb.append(0.8)
                    else:
                        targetProb.append(0)

                    ## from east
                    if(x in range(0,7)):
                        targetProb.append(0.1)

                    ## from south
                    if(x==5 and y in range(0,7)) or \
                        (x+1==3 and y==4) or (x+1==3 and y==1) or \
                        (x+1==1 and y==1) or (x+1==1 and y==4):
                        targetProb.append(0)
                    else:
                        targetProb.append(0.8)

                    evidenceMatrix[nextPath[0][0],nextPath[0][1]]
                    motionProbPerCell=0
                    print("Target Probability:" , targetProb)
                for k in  [0,1,2,3]:
                    #print("NextPath[k][0]: ", nextPath[k][0])
                    #print("NextPath[k][1]: ", nextPath[k][1])
                    print("NextPathcurrentmaze: ",evidenceMatrix[nextPath[k][0],nextPath[k][1]])
                    motionProbPerCell=float((motionProbPerCell+evidenceMatrix[nextPath[k][0],nextPath[k][1]]*targetProb[k]).round(3))
                
                motionProb.append(motionProbPerCell)
                print("Motion Probability:",motionProb) 
    elif(moveDirection=='West'):

        for x in [0,1,2,3,4,5]:
            for y in [0,1,2,3,4,5,6]:
                if((x==1 and y==1) or (x==1 and y==4) or \
                    (x==3 and y==1 ) and (x==3 and y==4)):
                    motionProbPerCell=0
                    motionProb.append(motionProbPerCell)
                    continue
                else:
                    probCalc=[]
                    nextPath=[]
                    nextmove=()

                    ## get the target position
                    ## from west
                    # If boundary
                    if (x in range(0,7) and y in range(0,7)):
                        nextmove=(x,y)
                    nextPath.append(nextmove)

                    ## from North
                    if (x-1<0 and y in range (0,7)) or \
                        (x-1==1 and y==1) or (x-1==1 and y==4) or \
                        (x-1==3 and y==1) or (x-1==3 and y==4):
                        nextmove=(x,y)
                    elif(x-1>=0 and y in range(0,7)):
                        nextmove=(x-1,y)
                    nextPath.append(nextmove)

                    ## from east
                    if (x in range(0,7) and y+1>6) or \
                        (x==1 and y+1==1) or (x==1 and y+1==4) or \
                        (x==3 and y+1==1) or(x==3 and y+1==4):
                        nextmove=(x,y)
                    else:
                        nextmove=(x,y+1)
                    nextPath.append(nextmove)

                    ## from south
                    if(x+1>5 and y in range(0,7)) or(x+1==1 and y==1)or \
                        (x+1==1 and y==4)or(x+1==3 and y==1)or(x+1==3 and y==4):
                        nextmove=(x,y)
                    else:
                        nextmove=(x+1,y)

                    nextPath.append(nextmove)

                    ### get the target values
                    targetProb=[]

                    ## from west
                    if (x in range(0,7) and y-1<0) or (y-1==1 and x ==1) or \
                        (y-1==4 and x==4) or(x==3 and y-1==1) or (x==3 and y-1==4):
                        targetProb.append(0.8)
                    else:
                        targetProb.append(0)

                    #from North
                    if (x in range(0,7)):
                        targetProb.append(0.1)
                    else:
                        targetProb.append(0)
                    
                    ## from east
                    if (x in range(0,7) and y+1>6) or(x==1 and y+1 ==1) or \
                        (x==1 and y+1==4) or(x==3 and y+1==1) or(x==3 and y+1==4):
                        targetProb.append(0)
                    else:
                        targetProb.append(0.8)

                    ## from south
                    if(x in range(0,7)):
                        targetProb.append(0.1)

                    evidenceMatrix[nextPath[0][0],nextPath[0][1]]
                    motionProbPerCell=0
                for k in  [0,1,2,3]:
                    motionProbPerCell = (motionProbPerCell+evidenceMatrix[nextPath[k][0],nextPath[k][1]]*targetProb[k])#.round(3))
                motionProb.append(motionProbPerCell)

    else:
        print('Unexpected move direction')
        print('Exiting program')
        exit()
    
    motionProbMatrix= np.matrix(motionProb).reshape(6,7)
    initialMatrix=motionProbMatrix
    return initialMatrix

if __name__=='__main__':
    
    initialRows = [0,1,2,3,4,5]
    intialCols = [0,1,2,3,4,5,6]
    evidenceMatrix = []
    moveMatrix = []
    initialMatrix = np.array([2.63,2.63,2.63,2.63,2.63,2.63,2.63,
                              2.63,0   ,2.63,2.63,0 ,2.63,2.63,
                              2.63,2.63,2.63,2.63,2.63,2.63,2.63,
                           2.63,0 ,2.63,2.63,0 ,2.63,2.63,
                           2.63,2.63,2.63,2.63,2.63,2.63,2.63,
                           2.63,2.63,2.63,2.63,2.63,2.63,2.63]).reshape(6,7)

    print(initialMatrix)
    evidenceMatrix = sensorEvidence([0,0,0,0],initialMatrix)
    print("\nSensor Evidence Matrix of sensing [0,0,0,0]:\n", sensorEvidence([0,0,0,0],initialMatrix))

    
    print(move([0,0,0,0],evidenceMatrix,'North'))
    moveMatrix=move([0,0,0,0],evidenceMatrix,'North')

    #evidenceMatrix=sensorEvidence([1,0,0,0],moveMatrix)
    #print("\nSensor Evidence Matrix of sensing [0,0,0,0]:\n", sensorEvidence([1,0,0,0],moveMatrix))

    # print(northMove([0,0,0,0],evidenceMatrix))

    # evidenceMatrix=sensorEvidence([0,0,0,0],moveMatrix)
    # print("\nSensor Evidence Matrix of sensing [0,0,0,0]:\n", sensorEvidence([0,0,0,0],moveMatrix))

    # print(westMove([0,0,0,0],evidenceMatrix))




    