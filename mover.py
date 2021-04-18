import defs
import math

class Mover:
    def __init__(self, movementType, startPoint, domainSize, pacelength=20, radius=40, movementDirection=defs.MovementDirection.HORIZONTALRIGHT):
        self.movementType = movementType
        self.startPoint = startPoint
        self.domainSize = domainSize
        self.lastPoint = startPoint
        self.paceLength = pacelength
        self.radius = radius
        self.movementDirection = movementDirection
        self.circleCenter = [startPoint[0] + radius, startPoint[1]] if (startPoint[0] + radius) < self.domainSize[0] else startPoint

    def getPosition(self, timeStep):
        if(self.movementType == defs.MovementType.STATIC):
            return self.startPoint
        elif(self.movementType == defs.MovementType.LINEAR):
            #find the next point one step in the direction of the movement
            if(self.movementDirection == defs.MovementDirection.VERTICALUP):
                nextX = (self.lastPoint[0] - 1) if (self.lastPoint[0] - 1) >= 0 else (self.domainSize[0] - 1)
                self.lastPoint = [int(nextX), int(self.lastPoint[1])]
            elif(self.movementDirection == defs.MovementDirection.VERTICALDOWN):
                nextX = (self.lastPoint[0] + 1) if (self.lastPoint[0] + 1) < self.domainSize[0] else 0
                self.lastPoint = [int(nextX), int(self.lastPoint[1])]
            elif(self.movementDirection == defs.MovementDirection.HORIZONTALRIGHT):
                nextY = (self.lastPoint[1] + 1) if (self.lastPoint[1] + 1) < self.domainSize[1] else 0
                self.lastPoint = [int(self.lastPoint[0]), int(nextY)]                
            elif(self.movementDirection == defs.MovementDirection.HORIZONTALLEFT):
                nextY = (self.lastPoint[1] - 1) if (self.lastPoint[1] - 1) >= 0 else (self.domainSize[1] - 1)
                self.lastPoint = [int(self.lastPoint[0]), int(nextY)]
            elif(self.movementDirection == defs.MovementDirection.DIAGUPRIGHT):
                nextX = (self.lastPoint[0] - 1) if (self.lastPoint[0] - 1) >= 0 else (self.domainSize[0] - 1)
                nextY = (self.lastPoint[1] + 1) if (self.lastPoint[1] + 1) < self.domainSize[1] else 0
                self.lastPoint = [int(nextX), int(nextY)]
            elif(self.movementDirection == defs.MovementDirection.DIAGUPLEFT):
                nextX = (self.lastPoint[0] - 1) if (self.lastPoint[0] - 1) >= 0 else (self.domainSize[0] - 1)
                nextY = (self.lastPoint[1] - 1) if (self.lastPoint[1] - 1) >= 0 else (self.domainSize[1] - 1)
                self.lastPoint = [int(nextX), int(nextY)]
            elif(self.movementDirection == defs.MovementDirection.DIAGDOWNRIGHT):
                nextX = (self.lastPoint[0] + 1) if (self.lastPoint[0] + 1) < self.domainSize[0] else 0
                nextY = (self.lastPoint[1] + 1) if (self.lastPoint[1] + 1) < self.domainSize[1] else 0
                self.lastPoint = [int(nextX), int(nextY)]
            elif(self.movementDirection == defs.MovementDirection.DIAGDOWNLEFT):
                nextX = (self.lastPoint[0] + 1) if (self.lastPoint[0] + 1) < self.domainSize[0] else 0
                nextY = (self.lastPoint[1] - 1) if (self.lastPoint[1] - 1) >= 0 else (self.domainSize[1] - 1)
                self.lastPoint = [int(nextX), int(nextY)]
            else:
                print("Movement type not recognized!")
            return self.lastPoint
        elif(self.movementType == defs.MovementType.PACING):
            step = timeStep % (self.paceLength * 2) if self.paceLength != 0 else 0
            #moving towards pacing point
            if step <= self.paceLength:
                nextY = (self.lastPoint[1] + step) if (self.lastPoint[1] + step) < self.domainSize[1] else (self.domainSize[1] - 1)
                self.lastPoint = [int(self.lastPoint[0]), int(nextY)]
            #moving back to starting point
            else:
                nextY = (self.lastPoint[1] + self.paceLength - step) if (self.lastPoint[1] + self.paceLength - step) < self.domainSize[1] else (self.domainSize[1] - 1)
                self.lastPoint = [int(self.lastPoint[0]), int(nextY)]
            return self.lastPoint
        elif(self.movementType == defs.MovementType.CIRCLE):
            #move 30 degrees at a time, so it will take 12 steps to complete a circle
            nextX = (self.circleCenter[0] + (self.radius * math.cos(30))) 
            if nextX < 0 or nextX > self.domainSize[0]:
                nextX = self.lastPoint[0]
            nextY = (self.circleCenter[1] + (self.radius * math.sin(30)))
            if nextY < 0 or nextY > self.domainSize[1]:
                nextY = self.lastPoint[1]
            self.lastPoint = [int(nextX), int(nextY)]
            return self.lastPoint
        else:
            print("Error! Don't recognize Movement Type!")
        return self.lastPoint
    