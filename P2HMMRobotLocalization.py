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
    
    def printMaze(self):
        # Calculate shape and ensure correct maze 
        #print("Maze probabilities:")
        for row in range(0,self.nRows):
            for col in range(0,self.nCols):
                print(round(self.currentMazeProb[row,col],3),"\t", end =" ")
            print("")

    def move(self):
        print("\nMoving robot")

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

                print("Prob cell: ", probCell)
                probCurrentCell = np.prod(probCell)*self.currentPosition[row,col]
                #print("Current Cell: row:", row, " col:",col, " prob:", round(probCurrentCell,3))

                probForEachCellInMaze.append(probCurrentCell)
                self.currentMazeProb[row,col] = probCurrentCell
        print(self.currentMazeProb)
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
    #sensorReading = [1,2,3,4]
    sensorReading = [0,0,0,0]
    Romba.sense(sensorReading)
    print("\nStep 1 Sensor Output: Filtering after Evidence [0,0,0,0]:")
    Romba.printMaze()
    '''
    # Step-2: Move      # Moving:N
    Romba.move()

    # Step-3: Sense     # Sensing:[1, 0, 0, 0]
    sensorReading = [1,0,0,0]
    Romba.sense(sensorReading)

    # Step-4: Move      # Moving:N
    Romba.move()

    # Step-5: Sense     # Sensing:[0, 0, 0, 0]
    sensorReading = [0,0,0,0]
    Romba.sense(sensorReading)

    # Step-6: Move      # Moving:W
    Romba.move()

    # Step-7: Sense     # Sensing:[0, 1, 0, 1]
    sensorReading = [0,1,0,1]
    Romba.sense(sensorReading)

    # Step-8: Move      # Moving:W
    Romba.move()

    # Step-9: Sense     # Sensing:[1, 0, 0, 0]
    sensorReading = [1,0,0,0]
    Romba.sense(sensorReading)
    '''
    # End of program
    print("\t\t\t End of program\n")
    print("########################################")


if __name__=='__main__':
    main()

