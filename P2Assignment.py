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

def allowedPos(i,j):
    orginalPath=[]

    allowedPath=[]

    ## Westwards
    if ((j == 0 and i >=0) or (i == 1 and j == 2) or (i == 1 and j == 5) or (i == 3 and j == 2) or (i == 3 and j == 5)):
        allowedPath.append(1)
    else:
        allowedPath.append(0)
    
    ## Northwards
    if ((i==0 and j >=0) or (i==2 and j== 1) or (i == 2 and j == 4) or (i == 4 and j == 1) or (i == 4 and j == 4)):
        allowedPath.append(1)
    else:
        allowedPath.append(0)

    ## Eastwards
    if ( (i == 1 and j == 0) or (i == 1 and j == 3) or (i>=0 and j == 6) or (i == 3 and j == 0) or (i == 3 and j == 3) ):
        allowedPath.append(1)
    else:
        allowedPath.append(0)
    
    ## Southwards
    if ((i == 0 and j == 1) or (i == 0 and j == 4) or (i == 2 and j == 1) or (i == 2 and j== 4) or (i== 5 and j>=0)):
        allowedPath.append(1)
    else:
        allowedPath.append(0)
    print(allowedPath)

    return allowedPath

### To find the location based on given evidence

def sensorEvidence(pathEvidence,moveMatrix):
    detectObstacle= 0.8
    notdetectObstacle =0.2
    errorOpenSq_Obstacle=0.15
    detectOpenSq= 0.85

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
            if((x==1 and y==1) or (x==1 and y==4) or (x==3 and y==1 ) and (x==3 and y==4)):
                perCellProbAllDirection.append(0)

            else:
                for k in [0,1,2,3]:
                    if (currentPath[k]==0 and nextPath[k]==0):
                        perCellProbAllDirection.append(0.85)
                    if(currentPath[k]==1 and nextPath[k]==1):
                        perCellProbAllDirection.append(0.8)
                    if(currentPath[k]==0 and nextPath[k]==1):
                        perCellProbAllDirection.append(0.15)
                    if(currentPath[k]==1 and nextPath[k]==0):
                        perCellProbAllDirection.append(0.2)

            totalProbAllDirection=((np.prod(perCellProbAllDirection)*moveMatrix[x,y]).round(4))
            print(totalProbAllDirection)

            alldirectionsum.append(totalProbAllDirection)

    sensor_probability = []
    for v in alldirectionsum:
        sensor_probability.append(float(((v*100)/np.sum(alldirectionsum)).round(2)))

    evidenceProb = sensor_probability

    evidenceMatrix=np.matrix(evidenceProb).reshape(6,7)
    return evidenceMatrix


## To find Prediction for next step

def northMove(previousStep,evidenceMatrix):
    row=[1,2,3,4,5,6]
    cols=[1,2,3,4,5,6,7]

    motionProb=[]
    for x in [0,1,2,3,4,5]:
        for y in [0,1,2,3,4,5,6]:
            if((x==1 and y==1) or (x==1 and y==4) or (x==3 and y==1 ) and (x==3 and y==4)):
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
                if (x in range(0,7) and y-1<0) or (x==1 and y-1 ==1) or (x==1 and y-1==4) or (x==3 and y-1==1) or (x==3 and y-1==4):
                    nextmove=(x,y)
                elif(x in range (0,7) and y-1>=0):
                     nextmove=(x,y-1)
                nextPath.append(nextmove)

                ## from North
                if ( x in range (0,6) and y in range(0,7)):
                    nextmove=(x,y)
                nextPath.append(nextmove)

                ## from east
                if (x in range (0,7) and y+1>=7) or (x==1 and y+1==1) or (x==1 and y+1==4) or (x==3 and y+1==1) or (x==3 and y+1==4):
                    nextmove=(x,y)
                elif(x in range(0,7) and y+1<=6):
                    nextmove=(x,y+1)
                nextPath.append(nextmove)

                ## from south
                if (x+1>=6 and y in range(0,7)) or (x+1==3 and  y==4)or (x+1==3 and y==1) or (x+1==1 and y==1) or (x+1==1 and y==4):
                    nextmove=(x,y)
                elif(x+1<6 and y in range(0,7)) or (x<=5 and y in range(0,7)):
                    nextmove=(x+1,y)

                nextPath.append(nextmove)


                ### get the target values
                targetProb=[]

                #from west
                if (x in range(0,7)):
                    targetProb.append(0.1)
                
                ## from North
                if (x==0 and y in range(0,7)) or (x-1==1 and y ==1) or (x-1==1 and y==4) or(x-1==3 and y==1) or (x-1==3 and y==4):
                    targetProb.append(0.8)
                else:
                    targetProb.append(0)


                ## from east
                if(x in range(0,7)):
                    targetProb.append(0.1)

                ## from south
                if(x==5 and y in range(0,7)) or (x+1==3 and y==4) or (x+1==3 and y==1) or (x+1==1 and y==1) or (x+1==1 and y==4):
                    targetProb.append(0)
                else:
                    targetProb.append(0.8)

                evidenceMatrix[nextPath[0][0],nextPath[0][1]]
                motionProbPerCell=0
            for k in  [0,1,2,3]:
                motionProbPerCell=float(motionProbPerCell+evidenceMatrix[nextPath[k][0],nextPath[k][1]]*targetProb[k])#.round(3))
            motionProb.append(motionProbPerCell)

    motionProbMatrix= np.matrix(motionProb).reshape(6,7)
    initialMatrix=motionProbMatrix
    return initialMatrix


def westMove(previousStep,evidenceMatrix):
    motionProb=[]
    for x in [0,1,2,3,4,5]:
        for y in [0,1,2,3,4,5,6]:
            if((x==1 and y==1) or (x==1 and y==4) or (x==3 and y==1 ) and (x==3 and y==4)):
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
                if (x-1<0 and y in range (0,7)) or (x-1==1 and y==1) or (x-1==1 and y==4) or (x-1==3 and y==1) or (x-1==3 and y==4):
                    nextmove=(x,y)
                elif(x-1>=0 and y in range(0,7)):
                    nextmove=(x-1,y)
                nextPath.append(nextmove)

                ## from east
                if (x in range(0,7) and y+1>6) or(x==1 and y+1==1) or (x==1 and y+1==4) or(x==3 and y+1==1) or(x==3 and y+1==4):
                    nextmove=(x,y)
                else:
                    nextmove=(x,y+1)
                nextPath.append(nextmove)

                ## from south
                if(x+1>5 and y in range(0,7)) or(x+1==1 and y==1)or(x+1==1 and y==4)or(x+1==3 and y==1)or(x+1==3 and y==4):
                    nextmove=(x,y)
                else:
                    nextmove=(x+1,y)

                nextPath.append(nextmove)


                ### get the target values
                targetProb=[]


                ## from west
                if (x in range(0,7) and y-1<0) or (y-1==1 and x ==1) or (y-1==4 and x==4) or(x==3 and y-1==1) or (x==3 and y-1==4):
                    targetProb.append(0.8)
                else:
                    targetProb.append(0)

                #from North
                if (x in range(0,7)):
                    targetProb.append(0.1)
                else:
                    targetProb.append(0)
                
                ## from east
                if (x in range(0,7) and y+1>6) or(x==1 and y+1 ==1) or(x==1 and y+1==4) or(x==3 and y+1==1) or(x==3 and y+1==4):
                   targetProb.append(0)
                else:
                    targetProb.append(0.8)

                ## from south
                if(x in range(0,7)):
                    targetProb.append(0.1)

               

                evidenceMatrix[nextPath[0][0],nextPath[0][1]]
                motionProbPerCell=0
            for k in  [0,1,2,3]:
                motionProbPerCell =(motionProbPerCell+evidenceMatrix[nextPath[k][0],nextPath[k][1]]*targetProb[k])#.round(3))
            motionProb.append(motionProbPerCell)

    motionProbMatrix= np.matrix(motionProb).reshape(6,7)
    initialMatrix=motionProbMatrix
    return initialMatrix

    
if __name__=='__main__':
    
    initialRows= [0,1,2,3,4,5]
    intialCols= [0,1,2,3,4,5,6]
    evidenceMatrix=[]
    moveMatrix=[]
    initialMatrix = np.array([2.63,2.63,2.63,2.63,2.63,2.63,2.63,
                           2.63,0 ,2.63,2.63,0 ,2.63,2.63,
                           2.63,2.63,2.63,2.63,2.63,2.63,2.63,
                           2.63,0 ,2.63,2.63,0 ,2.63,2.63,
                           2.63,2.63,2.63,2.63,2.63,2.63,2.63,
                           2.63,2.63,2.63,2.63,2.63,2.63,2.63]).reshape(6,7)

    print(initialMatrix)
    evidenceMatrix=sensorEvidence([0,0,0,0],initialMatrix)
    print("\nSensor Evidence Matrix of sensing [0,0,0,0]:\n", sensorEvidence([0,0,0,0],initialMatrix))

    
    print(northMove([0,0,0,0],evidenceMatrix))
    moveMatrix=northMove([0,0,0,0],evidenceMatrix)

    evidenceMatrix=sensorEvidence([1,0,0,0],moveMatrix)
    print("\nSensor Evidence Matrix of sensing [0,0,0,0]:\n", sensorEvidence([1,0,0,0],moveMatrix))

    # print(northMove([0,0,0,0],evidenceMatrix))

    # evidenceMatrix=sensorEvidence([0,0,0,0],moveMatrix)
    # print("\nSensor Evidence Matrix of sensing [0,0,0,0]:\n", sensorEvidence([0,0,0,0],moveMatrix))

    # print(westMove([0,0,0,0],evidenceMatrix))




    