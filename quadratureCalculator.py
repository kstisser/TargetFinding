import numpy as np
import defs
import gaussianQuadratureLookup
import gaussianEquation
import math

class QuadratureSums:
    def __init__(self, cube, gaussianQuadrature, newCotes):
        self.cubeSum = cube
        self.newCotesSum = newCotes
        self.gaussianQuadratureSum = gaussianQuadrature

class QuadratureCalculator:
    def __init__(self, separatedPlanes, mergedPlanes, peaks, N, weights):
        self.mergedPlanes = mergedPlanes
        self.peaks = peaks
        self.peaksQuadratureDic = {}
        #print("dic type: ", type(self.peaksQuadratureDic))
        self.separatedPlanes = separatedPlanes
        self.decayWeights = weights
        self.N = N
        #print("starting with merged planes size: ", self.mergedPlanes.shape)

    def initializeDicToZero(self):
        self.cubicSum = 0
        self.gaussianQuadratureSum  = 0
        self.newCodesSum = 0

    def getAreas(self, size, N, computeCubic=True, computeGaussianQuadrature=True, computeNewCotes=True):
        self.initializeDicToZero()
        self.N = N
        #self.peaks = map(tuple, self.peaks)
        for p in self.peaks:
            upperLeft, lowerRight = self.getCorners(p, size)
            cubicSum = self.getCubicArea(upperLeft, lowerRight) if computeCubic else 0
            ncSum = self.getNewCotesArea(upperLeft, lowerRight) if computeNewCotes else 0
            gqSum = self.getGaussianQuadratureArea(upperLeft, lowerRight) if computeGaussianQuadrature else 0
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
        gqlookup = gaussianQuadratureLookup.GaussianQuadratureLookup(self.N)
        weights, xs = gqlookup.getWeightsAndVariables()
        stddev = 2

        sum = 0
        #we need i and j to move between the domain given, so we'll adjust to make this applicable
        xRange = float(lowerRight[1] - upperLeft[1] + 1)
        yRange = float(lowerRight[0] - upperLeft[0] + 1)
        xMin = upperLeft[1]
        xMax = lowerRight[1]
        yMin = upperLeft[0]
        yMax = lowerRight[0]
        Xincrement = xRange/self.N
        Yincrement = yRange/self.N

        for peak in self.peaks:
            #peak gives the mean of the gaussian distribution, check if it's within the domain we're adding
            if self.isWithinDomain(peak, upperLeft, lowerRight):
                weightSum = 0
                for w in range(len(self.separatedPlanes)):
                    if self.hasPointNearThis(w, peak):
                        weightSum = weightSum + self.decayWeights[w]
                    for i in range(len(weights)):
                        xConverted = xMin + (((xs[i] + 1)/2.0)*xRange)
                        for j in range(len(weights)):
                            yConverted = yMin + (((xs[j] + 1)/2.0)*yRange)
                            #print("X converted: ", xConverted, ", Y Converted: ", yConverted, "X init: ", xs[i], ", Y init: ", xs[j])
                            newVal = gaussianEquation.getGaussianDistributionValue(peak, xConverted, yConverted, stddev)
                            sum = sum + newVal
        sum = sum * (2/xRange) * (2/yRange)
        totalWeights = np.sum(self.decayWeights)
        currentWeight = self.decayWeights[-1]
        #we want to give the weight of the rest of the frames that had a point near it
        sum = weightSum/currentWeight
        print("Got Gaussian Quadrature area of: ", sum)
        return sum

    def hasPointNearThis(self, planeIndex, point):
        if planeIndex >= len(self.separatedPlanes):
            return False
        nearThreshold = 10
        plane = self.separatedPlanes[planeIndex]
        points = np.transpose(np.where(plane == 1))
        for p in points:
            distance = math.sqrt((p[0] - point[0])**2 + (p[1] - point[1])**2)
            if distance < nearThreshold:
                return True
        return False

    def isWithinDomain(self, point, upperLeft, lowerRight):
        if point[0] < upperLeft[0] or point[0] > lowerRight[0]:
            return False
        if point[1] < upperLeft[1] or point[1] > lowerRight[1]:
            return False
        return True

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
                        runningCount = runningCount + self.mergedPlanes[y,x-1]
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
        #print("Found upper left: ", upperLeft, ", lower right corner: ", lowerRight)
        return upperLeft, lowerRight
        