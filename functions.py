# Adapted from https://github.com/jpittma1

import timeit
from queue import PriorityQueue
import numpy as np
import cv2
import math
from obstacles import *
from Node import *

def getInitialStates():
    print("Enter initial node, separated by spaces: ")
    initial=[int(x) for x in input().split()]
    print("Enter goal node, separated by spaces: ")
    final=[int(x) for x in input().split()]
    return initial, final

#To fix the origin from top left to bottom right
def updateNodesOnMap(map, nodeState, color):
    x,y, _ = map.shape
    transY = nodeState[0]  
    transX = x - nodeState[1] - 1
    map[transX,transY, :] = color
    
    return map

#Equation of line for Hexagon, Rectangles, and Triangle
def lineEquation(p1,p2,x,y):
    func = ((p2[1] - p1[1]) * (x - p1[0])) / ( p2[0] - p1[0]) + p1[1] - y
    
    return func

def addObstaclesToMap(map):

    for i in range(map.shape[1]):
       for j in range(map.shape[0]):

            #-----HEXAGON--------------------------
            if (i < hexRightX and i > hexLeftX and \
                lineEquation((hexLeftX  , hexUpperY)  ,(hexTopX   , hexTopY),i,j) > 0 and \
                lineEquation((hexTopX   , hexTopY)    ,(hexRightX , hexUpperY),i,j) > 0 and \
                lineEquation((hexLeftX  , hexLowerY)  ,(hexBottomX, hexBottomY),i,j) < 0 and \
                lineEquation((hexBottomX, hexBottomY) ,(hexRightX , hexLowerY),i,j) < 0):
                updateNodesOnMap(map, [i, j], [255,0,0])
            
            #----Top Rectangle--------
            if(i > boxLeftX and i < boxRightX and j < upperTopY and j > upperBottomY):
                updateNodesOnMap(map, [i, j], [255,0,0])

            #----Bottom Rectangle--------
            if(i > boxLeftX and i < boxRightX and j < lowerTopY and j > lowerBottomY):
                updateNodesOnMap(map, [i, j], [255,0,0])

            if(i > triLeftX and i < triRightX and \
                lineEquation((triRightX,triMiddleY),(triLeftX,triLowerY),i,j) < 0 and \
                lineEquation((triLeftX,triUpperY),(triRightX,triMiddleY),i,j) > 0):
                updateNodesOnMap(map, [i, j], [255,0,0])

    return map

# Return 1 if within an obstacle or outside of map 

def inObstacleSpace(x,y):
    x_max=600-1
    y_max=250-1
    '''
    positive = inside 
    negative = outside
    zero = on an edge 
    '''
    
    #Check if within Map
    if (x > x_max or int(x) < 0 or int(y) < 0 or int(y) > y_max):
        return 1

    #check if within Hexagon
    inHexagon = cv2.pointPolygonTest(hexagon, (x,y), False)
    if inHexagon > 0:
        return 1
  
    #check if within boomerang
    
    inUpperRect = cv2.pointPolygonTest(upperRect, (x,y), False)
    if inUpperRect > 0:
        return 1
    
    inLowerRect = cv2.pointPolygonTest(lowerRect, (x,y), False)
    if inLowerRect > 0:
        return 1

    inTriangle = cv2.pointPolygonTest(triangle, (x,y), False)
    if inTriangle > 0:
        return 1
    
    return 0

def possibleMoves(current_node):
    # i = int(current_node[0])
    # j=  int(current_node[1])
    i,j=current_node.getState()

    moves = ['N','NE', 'E', 'SE', 'S', 'SW','W', 'NW']
    possibleMoves = ['N','NE', 'E', 'SE', 'S', 'SW','W', 'NW']
    moveX = [i, i+1, i+1, i+1, i, i-1, i-1, i-1]
    moveY = [j+1, j+1, j, j-1, j-1, j-1, j, j+1]

    for move in range(len(moves)):
        if (inObstacleSpace(moveX[move], moveY[move]) or \
            current_node.getParentState() == [moveX[move], moveY[move]]):
            possibleMoves.remove(moves[move])
    
    return possibleMoves

def MoveLeft(x,y):
    newNode = [x-1 , y]
    
    return newNode

def MoveRight(x,y):
    newNode = [x+1 , y]
    
    return newNode

def MoveUp(x,y):
    newNode = [x , y+1]
    
    return newNode

def MoveDown(x,y):
    newNode = [x , y-1]
    
    return newNode

def MoveUpRight(x,y):
    newNode = [x+1 , y+1]
    
    return newNode

def MoveDownRight(x,y):
    newNode = [x+2 , y-1]
    
    return newNode

def MoveDownLeft(x,y):
    newNode = [x-1 , y-1]
    
    return newNode

def MoveUpLeft(x,y):
    newNode = [x-1 , y+1]
    
    return newNode

# Check for Goal Node
def equalToGoal(now,goal):
    if np.array_equal(now, goal) or now==goal:
        return 1
    else:
        return 0

def makeFiles(visited, last, path, pIndex, nIndex):
    
    # nodePath.txt for storing path
    f = open("NodePath.txt",'w')
    
    #convert list to String
    f.writelines("%s\n" % str(move) for move in path)
    f.close()
    
    # NodesInfo.txt for storing parents and children
    f2=open('NodesInfo.txt','w')
    f2.write("Node_index\tParent_Node_index\n")
    
    for row in range(len(path)):
        f2.write(str(nIndex[row]))
        f2.write("\t\t\t")
        f2.write(str(pIndex[row]))
        f2.write("\n")
    f2.close()
    
    # Nodes.txt for storing all explored states/nodes
    f3=open('Nodes.txt','w')
    
    for visit in range(len(visited)):
        f3.write(str(visited[visit]))
        f3.write("\n")
    f3.close()