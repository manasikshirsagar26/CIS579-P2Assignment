#######################################################
# CIS 579: Artificial Intelligence
# Name: Manasi Kshirsagar
# UMID- 05494807
# Instructor: Prof. Shengquan Wang
# Semester: Winter 2021 
# P2 assignment: Hidden Markov Models -- To locate Robot in Windy Maze
#######################################################

# Import required packages
import os
import numpy as np
import copy
from operator import itemgetter

# ####################################################

class MazeCell():
    def __init__(self):
        self.x = 0
        self.y = 0

class Robot():

    currentRow = 0
    currentCol = 0
    nRows = 6
    nCols = 7
    #detectCorrectObstacle = 0.8
    #errorDetectObstacle = 1.0 - detectCorrectObstacle
    #errorOpenCellAsObstacle = 0.15
    #detectOpenCell = 1.0 - errorOpenCellAsObstacle

    currentMazeProb = np.full(shape=(nRows,nCols), fill_value=0.0, dtype=np.float)
    
    def __init__(self, name,currentMatrix):
        self.name = 'Romba'
        self.detectCorrectObstacle = 0.8
        self.errorDetectObstacle = 1.0 - self.detectCorrectObstacle
        self.errorOpenCellAsObstacle = 0.15
        self.detectOpenCell = 1.0 - self.errorOpenCellAsObstacle
        self.currentPosition = currentMatrix
        self.currentMazeProb = currentMatrix
    
    def printMaze(self):
        # Calculate shape and ensure correct maze 
        print("Maze probabilities:")
        for row in range(0,self.nRows):
            for col in range(0,self.nCols):
                print(round(self.currentMazeProb[row,col],2),"\t", end =" ")
            print("")

    def move(self,moveDirection):
        print("\nMoving robot..")
        motionProb=[]

        if(moveDirection=='North'):
        
            for row in range(0,self.nRows):
                for col in range(0,self.nCols):
                    if((row==1 and col==1) or (row==1 and col==4) or \
                        (row==3 and col==1 ) or (row==3 and col==4)):
                        motionProbPerCell = 0.0
                        motionProb.append(motionProbPerCell)
                        continue
                    else:
                        probCalc=[]
                        nextPath=[]
                        nextmove=()

                        ## get the target position
                        ## from west
                        # If boundary
                        if (row in range(0,7) and col-1<0) or \
                            (row==1 and col-1 ==1) or (row==1 and col-1==4) or \
                            (row==3 and col-1==1) or (row==3 and col-1==4):
                            nextmove=(row,col)
                        elif(row in range (0,7) and col-1>=0):
                            nextmove=(row,col-1)
                        nextPath.append(nextmove)

                        ## from North
                        if ( row in range (0,6) and col in range(0,7)):
                            nextmove=(row,col)
                        nextPath.append(nextmove)

                        ## from east
                        if (row in range (0,7) and col+1>=7) or \
                            (row==1 and col+1==1) or (row==1 and col+1==4) or \
                            (row==3 and col+1==1) or (row==3 and col+1==4):
                            nextmove=(row,col)
                        elif(row in range(0,7) and col+1<=6):
                            nextmove=(row,col+1)
                        nextPath.append(nextmove)

                        ## from south
                        if (row+1>=6 and col in range(0,7)) or \
                            (row+1==3 and  col==4) or (row+1==3 and col==1) or \
                            (row+1==1 and col==1) or (row+1==1 and col==4):
                            nextmove=(row,col)
                        elif(row+1<6 and col in range(0,7)) or (row<=5 and col in range(0,7)):
                            nextmove=(row+1,col)

                        nextPath.append(nextmove)
                        #print(nextPath)
                        ### get the target values
                        targetProb=[]

                        #from west
                        if (row in range(0,7)):
                            targetProb.append(0.1)
                        
                        ## from North
                        if (row==0 and col in range(0,7)) or \
                            (row-1==1 and col ==1) or (row-1==1 and col==4) or \
                            (row-1==3 and col==1) or (row-1==3 and col==4):
                            targetProb.append(0.8)
                        else:
                            targetProb.append(0)

                        ## from east
                        if(row in range(0,7)):
                            targetProb.append(0.1)

                        ## from south
                        if(row==5 and col in range(0,7)) or \
                            (row+1==3 and col==4) or (row+1==3 and col==1) or \
                            (row+1==1 and col==1) or (row+1==1 and col==4):
                            targetProb.append(0)
                        else:
                            targetProb.append(0.8)

                        self.currentMazeProb[nextPath[0][0],nextPath[0][1]]
                        motionProbPerCell = 0.0
                        #print("Target Probability:",targetProb)

                    for k in  [0,1,2,3]:
                        #print("NextPath[k][0]: ", nextPath[k][0])
                        #print("NextPath[k][1]: ", nextPath[k][1])
                        #print("NextPathcurrentmaze: ",self.currentMazeProb[nextPath[k][0],nextPath[k][1]])
                        motionProbPerCell=float(motionProbPerCell + \
                            self.currentMazeProb[nextPath[k][0],nextPath[k][1]]*targetProb[k])
                    
                    # Append probability
                    motionProb.append(motionProbPerCell)

        elif(moveDirection=='West'):

            for row in range(0,self.nRows):
                for col in range(0,self.nCols):
                    if((row==1 and col==1) or (row==1 and col==4) or \
                        (row==3 and col==1) or (row==3 and col==4)):
                        motionProbPerCell = 0
                        motionProb.append(motionProbPerCell)
                        continue
                    else:
                        probCalc=[]
                        nextPath=[]
                        nextmove=()

                        ## get the target position
                        ## from west
                        # If boundary
                        if (row in range(0,7) and col in range(0,7)):
                            nextmove=(row,col)
                        nextPath.append(nextmove)

                        ## from North
                        if (row-1<0 and col in range (0,7)) or \
                            (row-1==1 and col==1) or (row-1==1 and col==4) or \
                            (row-1==3 and col==1) or (row-1==3 and col==4):
                            nextmove=(row,col)
                        elif(row-1>=0 and col in range(0,7)):
                            nextmove=(row-1,col)
                        nextPath.append(nextmove)

                        ## from east
                        if (row in range(0,7) and col+1>6) or \
                            (row==1 and col+1==1) or (row==1 and col+1==4) or \
                            (row==3 and col+1==1) or(row==3 and col+1==4):
                            nextmove=(row,col)
                        else:
                            nextmove=(row,col+1)
                        nextPath.append(nextmove)

                        ## from south
                        if(row+1>5 and col in range(0,7)) or(row+1==1 and col==1)or \
                            (row+1==1 and col==4)or(row+1==3 and col==1)or(row+1==3 and col==4):
                            nextmove=(row,col)
                        else:
                            nextmove=(row+1,col)

                        nextPath.append(nextmove)

                        ### get the target values
                        targetProb=[]

                        ## from west
                        if (row in range(0,7) and col-1<0) or (col-1==1 and row ==1) or \
                            (col-1==4 and row==4) or(row==3 and col-1==1) or (row==3 and col-1==4):
                            targetProb.append(0.8)
                        else:
                            targetProb.append(0)

                        #from North
                        if (row in range(0,7)):
                            targetProb.append(0.1)
                        else:
                            targetProb.append(0)
                        
                        ## from east
                        if (row in range(0,7) and col+1>6) or(row==1 and col+1 ==1) or \
                            (row==1 and col+1==4) or(row==3 and col+1==1) or(row==3 and col+1==4):
                            targetProb.append(0)
                        else:
                            targetProb.append(0.8)

                        ## from south
                        if(row in range(0,7)):
                            targetProb.append(0.1)

                        self.currentMazeProb[nextPath[0][0],nextPath[0][1]]
                        motionProbPerCell=0
                    for k in  [0,1,2,3]:
                        motionProbPerCell = (motionProbPerCell + \
                            self.currentMazeProb[nextPath[k][0],nextPath[k][1]]*targetProb[k])#.round(3))
                    motionProb.append(motionProbPerCell)

        # Reshape obtained probabilities and store obtained probabilities 
        # in maze cells
        motionProbMatrix= np.matrix(motionProb).reshape(6,7)
        #print(motionProbMatrix)
        for row in range(0,self.nRows):
            for col in range(0,self.nCols):
                self.currentMazeProb[row,col] = motionProbMatrix[row,col]
                


    def isCurrentCellObstacle(self, row, col):
        isObstacle = False
        if(row==1 and col==1):
            isObstacle = True
        elif(row==1 and col==4):
            isObstacle = True
        elif(row==3 and col==1):
            isObstacle = True
        elif(row==3 and col==4):
            isObstacle = True

        return isObstacle

    def sense(self,sensorReading):
        print("\nSense obstacles")
        print("Sensor reading is: ", sensorReading)
        sensorReadingWest   = sensorReading[0]
        sensorReadingNorth  = sensorReading[1]
        sensorReadingEast   = sensorReading[2]  
        sensorReadingSouth  = sensorReading[3]
        print("Sensor Reading West: ", sensorReadingWest)
        print("Sensor Reading North: ", sensorReadingNorth)
        print("Sensor Reading East: ", sensorReadingEast)
        print("Sensor Reading South: ", sensorReadingSouth)
        
        probForEachCellInMaze = []

        # Iterate over each cell in maze
        for row in range(0,self.nRows):
            for col in range(0,self.nCols):
                currentCell = [row,col]
                probCell = []
                totalProb = []

                surroundingCell = isPositionAllowed(row,col)

                if(self.isCurrentCellObstacle(row, col)):
                    probCell.append(0.0)
                else:
                    for i in range(0,4):
                        if (surroundingCell[i]==0 and sensorReading[i]==0):
                            probCell.append(self.detectOpenCell)
                        if (surroundingCell[i]==1 and sensorReading[i]==0):
                            probCell.append(self.errorDetectObstacle)
                        if(surroundingCell[i]==0 and sensorReading[i]==1):
                            probCell.append(self.errorOpenCellAsObstacle)
                        if(surroundingCell[i]==1 and sensorReading[i]==1):
                            probCell.append(self.detectCorrectObstacle)

                #for i in len(probCell):
                #    probCell[i] = round(probCell[i],3)

                #print("Prob cell: ", probCell)
                probCurrentCell = np.prod(probCell)*self.currentPosition[row,col]
                #print("Current Cell: row:", row, " col:",col, " prob:", round(probCurrentCell,3))

                probForEachCellInMaze.append(probCurrentCell)
                self.currentMazeProb[row,col] = probCurrentCell
        #print(self.currentMazeProb)
        for row in range(0,self.nRows):
            for col in range(0,self.nCols):
                self.currentMazeProb[row,col] = (self.currentMazeProb[row,col]* 100) \
                    /np.sum(probForEachCellInMaze)

        filterEvidence = []
        for v in probForEachCellInMaze:
            filterEvidence.append(float(((v*100)/np.sum(probForEachCellInMaze)).round(2)))

                
def isPositionAllowed(row,col):
        allowedPosition=[]
        #Westwards
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

        return allowedPosition

def main():

    # Initializations
    print("########################################")
    print("\nProgramming Assignment 2: Hidden Markov Model\n")

    # Define initial given maze as matrix
    initialMatrix = np.full(shape=(6,7), fill_value=0.0, dtype=np.float)
    nRows, nCols = initialMatrix.shape
    print("Size of maze: Rows:", nRows, " Columns:", nCols)
    totalMazeCells = nRows * nCols
    obstacleCells = 4   # Given
    emptyCellsInMaze = totalMazeCells - obstacleCells
    probOfRobotInEmptyCell = round(100/emptyCellsInMaze, 2)
    print("Probability of robot in any empty cell in maze is: ", probOfRobotInEmptyCell)

    # Fill in initial probability for all cells in maze
    initialMatrix[:] = probOfRobotInEmptyCell

    # FIll in probability for obstacle cells
    initialMatrix[1,1] = 0.0
    initialMatrix[1,4] = 0.0
    initialMatrix[3,1] = 0.0
    initialMatrix[3,4] = 0.0

    

    # Initialize robot
    Romba = Robot('Romba',initialMatrix)
    Romba.printMaze()
    

    # Step-1: Sense     # Sensing:[0, 0, 0, 0]
    #sensorReading = [1,2,3,4] Used for debugging
    sensorReading = [0,0,0,0]
    Romba.sense(sensorReading)
    print("\n####################################")
    print("\nStep 1 Sensor Output: Filtering after Evidence [0,0,0,0]:")
    Romba.printMaze()
    
    # Step-2: Move     # Moving:N
    print("####################################")
    print("\nStep 2 Robot is now going to move to North ")
    Romba.move("North")
    print("\nStep 2 After moving in North direction, probabilities looks like:")
    Romba.printMaze()
    
    # Step-3: Sense     # Sensing:[1, 0, 0, 0]
    sensorReading = [1,0,0,0]
    Romba.sense(sensorReading)
    print("\n####################################")
    print("\nStep 3 Sensor Output: Filtering after Evidence [1,0,0,0]:")
    Romba.printMaze()

    
    # Step-4: Move      # Moving:N
    print("####################################")
    print("\nStep 4 Robot is now going to move to North ")
    Romba.move("North")
    print("\nStep 4 After moving in North direction, probabilities looks like:")
    Romba.printMaze()

    # Step-5: Sense     # Sensing:[0, 0, 0, 0]
    sensorReading = [0,0,0,0]
    Romba.sense(sensorReading)
    print("\n####################################")
    print("\nStep 5 Sensor Output: Filtering after Evidence [0,0,0,0]:")
    Romba.printMaze()
    
    # Step-6: Move      # Moving:W
    print("####################################")
    print("\nStep 6 Robot is now going to move to West ")
    Romba.move("West")
    print("\nStep 6 After moving in West direction, probabilities looks like:")
    Romba.printMaze()
    
    # Step-7: Sense     # Sensing:[0, 1, 0, 1]
    sensorReading = [0,1,0,1]
    Romba.sense(sensorReading)
    print("\n####################################")
    print("\nStep 7 Sensor Output: Filtering after Evidence [0,1,0,1]:")
    Romba.printMaze()

    # Step-8: Move      # Moving:W
    print("####################################")
    print("\nStep 8 Robot is now going to move to West ")
    Romba.move("West")
    print("\nStep 8 After moving in West direction, probabilities looks like:")
    Romba.printMaze()

    # Step-9: Sense     # Sensing:[1, 0, 0, 0]
    sensorReading = [1,0,0,0]
    Romba.sense(sensorReading)
    print("\n####################################")
    print("\nStep 9 Sensor Output: Filtering after Evidence [1,0,0,0]:")
    Romba.printMaze()
    
    # End of program
    print("\t\t\t End of program\n")
    print("########################################")


if __name__=='__main__':
    main()

