import numpy as np
import defs

class QuadratureSums:
    def __init__(self, cube, gaussianQuadrature, newCotes):
        self.cubeSum = cube
        self.newCotesSum = newCotes
        self.gaussianQuadratureSum = gaussianQuadrature

class QuadratureCalculator:
    def __init__(self, separatedPlanes, mergedPlanes, peaks, N):
        self.mergedPlanes = mergedPlanes
        self.peaks = peaks
        self.peaksQuadratureDic = {}
        print("dic type: ", type(self.peaksQuadratureDic))
        self.separatedPlanes = separatedPlanes
        self.N = N
        print("starting with merged planes size: ", self.mergedPlanes.shape)

    def initializeDicToZero(self):
        self.cubicSum = 0
        self.gaussianQuadratureSum  = 0
        self.newCodesSum = 0

    def getAreas(self, size, N, computeCubic=True, computeGaussianQuadrature=True, computeNewCotes=True):
        self.initializeDicToZero()
        self.N = N
        self.peaks = map(tuple, self.peaks)
        for p in self.peaks:
            print("Peak type: ", type(p))
            upperLeft, lowerRight = self.getCorners(p, size)
            cubicSum = self.getCubicArea(upperLeft, lowerRight) if computeCubic else 0
            gqSum = self.getGaussianQuadratureArea(upperLeft, lowerRight) if computeGaussianQuadrature else 0
            ncSum = self.getNewCotesArea(upperLeft, lowerRight) if computeNewCotes else 0
            self.peaksQuadratureDic[p] = QuadratureSums(cubicSum, gqSum, ncSum)
        return self.peaksQuadratureDic

    def getCubicArea(self, upperLeft, lowerRight):
        sum = 0
        for y in range(upperLeft[0], lowerRight[0] + 1):
            for x in range(upperLeft[1], lowerRight[1] + 1):
                if self.isInRange(y,0) and self.isInRange(x,1):
                    sum = sum + self.mergedPlanes[y,x]
                else:
                    print("Trying to get area outside bounds!")
        print("Got cubic area of: ", sum)
        return sum

    def getGaussianQuadratureArea(self, upperLeft, lowerRight):
        #TODO
        return 10

    #Simpson's rule over one subinterval
    def getNewCotesArea(self, upperLeft, lowerRight):
        sum = 0
        for y in range(upperLeft[0], lowerRight[0] + 1):
            for x in range(upperLeft[1], lowerRight[1] + 1):
                if self.isInRange(y,0) and self.isInRange(x,1):
                    #clear out and start new addition for the cell
                    runningCount = self.mergedPlanes[y,x] * 4
                    countAdded = 1
                    if self.isInRange(x-1,1):
                        runningCount = runningCount + self.mergedPlanes[y,x-1]
                        countAdded = countAdded + 1
                    if self.isInRange(x+1,1):
                        runningCount = runningCount + self.mergedPlanes[y,x+1]
                        countAdded = countAdded + 1
                    runningCount = runningCount/countAdded
                    sum = sum + runningCount
                else:
                    print("Trying to get area outside bounds!")
        print("Got new cotes area of: ", sum)
        return sum

    def isInRange(self, point, axis):
        if (point >= 0) and (point <= self.mergedPlanes.shape[axis]):
            return True
        return False

    def getCorners(self, peakPoint, size):
        upperLeft = (max((peakPoint[0] - size), 0), max((peakPoint[1] - size), 0))
        lowerRight = (min((peakPoint[0] + size), (len(self.mergedPlanes)-1)), min((peakPoint[1] + size), (self.mergedPlanes.shape[1]-1)))
        print("Found upper left: ", upperLeft, ", lower right corner: ", lowerRight)
        return upperLeft, lowerRight
        