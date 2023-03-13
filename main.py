# Adapted from https://github.com/jpittma1

from Node import *
from functions import *
from obstacles import *

# User inputs initial and goal state 
Xi, Xg = getInitialStates()

print("Initial State is ", Xi)
print("Goal state is: ", Xg)

# Check for valid values
if inObstacleSpace(Xi[0],Xi[1]):
    print("Initial state is in an obstacle or off the map, please provide new valid initial state")
    exit()
    
if inObstacleSpace(Xg[0],Xg[1]):
    print("Goal state is in an obstacle or off the map, please provide new valid initial state")
    exit()

''' 
Initialize tuple and store in OpenList
   [0,1] = coordinate values (x,y) from user input
   [2]   = index of node; initially set to 0
   [3]   = parent node index; initially set to -1
   [4]   = cost to come; initially set to 0
   [5]   = total cost
'''

# Class object and Priority Queue Initialization
OpenList = PriorityQueue()  
startNode = Node(Xi, None, None, 0)
OpenList.put((startNode.getCost(), startNode))

# Node Object: self, state, parent, move, cost; give each node cost of infinity

ClosedList=np.array([[Node([i,j],None, None, math.inf) for j in range(250)] for i in range(600)])

reachedGoal = 0

movesCost = {'N':1, 'NE':1.4, 'E':1, 'SE':1.4, 'S':1, 'SW':1.4, 'W':1, 'NW':1.4}

print("Initial and Goal points are valid...Generating map...")
'''Visualization Code:
    Map Background  = Black
    Start           = Red
    Path            = Red
    Goal            = Red
    Obstacles       = Blue
    Completed Nodes = Green
'''
mapSize = [250, 600] 
mapY, mapX = mapSize
videoname=('proj2_robert_reiter')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(str(videoname)+".mp4",  fourcc, 3000, (mapX, mapY))

space = np.zeros([mapSize[0], mapSize[1], 3], dtype=np.uint8) 
space = updateNodesOnMap(space, Xi, [255,0,0])
space = updateNodesOnMap(space, Xg, [255,0,0])
space = addObstaclesToMap(space)

cv2.imwrite('Initial_map.jpg', space)
print("Initial map created named 'Initial_map.jpg' ")

cv2.imshow('Initial_map', space)

# Conduct Dijkstra algorithm to find path between initial and goal node avoiding obstacles

start = timeit.default_timer()
print("Commencing Dijkstra Search.......")

while not (OpenList.empty() and reachedGoal):
    
    currentNode = OpenList.get()[1]
    i, j = currentNode.getState()
    
    space = updateNodesOnMap(space, currentNode.getState(), [0, 255, 0])
    video.write(space)
    
    #Save Directional Moves in x and y dictionaries-----

    movesX = {'N':i, 'NE':i+1, 'E':i+1, 'SE':i+1, 'S':i, 'SW':i-1, 'W':i-1, 'NW':i-1}
    movesY = {'N':j+1, 'NE':j+1, 'E':j, 'SE':j-1, 'S':j-1, 'SW':j-1, 'W':j, 'NW':j+1}
    
    reachedGoal = equalToGoal(currentNode.getState(),Xg)

    if reachedGoal:
        
        print("Goal Reached!!")
        print("Total cost of path is ", currentNode.getCost())

        movesPath, path = currentNode.getFullPath()

        for node in path:  # Draw Node pathway on map
                pos = node.getState()
                space = updateNodesOnMap(space, pos, [0, 0, 255]) 
                cv2.imshow('Map',space)
                video.write(space)
    
    else:
        xPrime=possibleMoves(currentNode)
        parentCost=currentNode.getCost()    # Current cost to come
                
        # Iterate through all compass point directions
        for move in xPrime:
            childPos = [movesX.get(move), movesY.get(move)]
            CostToCome = parentCost + movesCost.get(move)
            
            # Verify not visited based on CostToCome set to infinity
            if (ClosedList[childPos[0], childPos[1]].getCost() == math.inf):
                childNode = Node(childPos, currentNode, move, CostToCome)
                ClosedList[childPos[0], childPos[1]] = childNode
                OpenList.put((childNode.getCost(), childNode))
            else:
                # Check if cost is larger than CostToCome + localCost
                if (CostToCome < ClosedList[childPos[0], childPos[1]].getCost()): 
                    childNode = Node(childPos, currentNode, move, CostToCome)
                    ClosedList[childPos[0], childPos[1]] = childNode
                    OpenList.put((childNode.getCost(), childNode))
                
    if reachedGoal: break

stop = timeit.default_timer()
print("That algorithm took ", stop - start, " seconds")

cv2.namedWindow("map", cv2.WINDOW_NORMAL)
cv2.imshow('Final map', space)
cv2.imwrite('Final_map.jpg', space)
print("Final map created, 'final_map.jpg' ")

if cv2.waitKey(1) == ord('q'):
    video.release()

video.release()
cv2.destroyAllWindows()