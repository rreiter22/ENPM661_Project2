# Adapted from https://github.com/jpittma1

import numpy as np

mapX = 600 # mm
mapY = 250 # mm
robotRadius = 0
clearance = 5
totalClearance = robotRadius + clearance

hexRadius=int(75 + clearance)
hexCenterX = 300
hexCenterY = 125
hexLeftX   = hexCenterX - hexRadius
hexRightX  = hexCenterX + hexRadius

boxLeftX     = 100 - clearance
boxRightX    = 150 + clearance
lowerBottomY = -1
lowerTopY    = 100 + clearance
upperBottomY = 150 - clearance
upperTopY    = 251

triLeftX     = 460 - clearance
triRightX    = 510 + clearance
triLowerY    = 25 - clearance
triUpperY    = 225 + clearance
triMiddleY   = 125

hexagon_r = 75
hexCorner = int(hexRadius/2)
hexLeftX  = hexCenterX - hexRadius
hexUpperY = hexCenterY + hexCorner
hexLowerY = hexCenterY - hexCorner
hexRightX = hexCenterX + hexRadius
hexTopX   = hexCenterX
hexTopY   = hexCenterY + hexRadius
hexBottomX= hexTopX
hexBottomY= hexCenterY - hexRadius


hexagon = np.array([[hexLeftX,hexUpperY],
                    [hexTopX,hexTopY],
                    [hexRightX,hexUpperY],
                    [hexRightX,hexLowerY],
                    [hexBottomX,hexBottomY],
                    [hexLeftX,hexLowerY]], np.int32)

lowerRect = np.array([[boxLeftX,lowerBottomY],
                    [boxLeftX,lowerTopY],
                    [boxRightX,lowerTopY],
                    [boxRightX,lowerBottomY]], np.int32)

upperRect = np.array([[boxLeftX,upperBottomY],
                    [boxLeftX,upperTopY],
                    [boxRightX,upperTopY],
                    [boxRightX,upperBottomY]], np.int32)

triangle = np.array([[triLeftX,triLowerY],
                    [triLeftX,triUpperY],
                    [triRightX,triMiddleY]], np.int32)