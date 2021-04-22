import numpy as np
import defs
import gaussianQuadratureLookup
import gaussianEquation
import math
import time

class QuadratureSums:
    def __init__(self, cube, newCotes, gaussianQuadrature, cubeTime, newCotesTime, gaussianTime):
        self.cubeSum = cube
        self.newCotesSum = newCotes
        self.gaussianQuadratureSum = gaussianQuadrature
        self.cubeTime = cubeTime
        self.newCotesTime = newCotesTime
        self.gaussianQuadratureTime = gaussianTime

class QuadratureCalculator:
    def __init__(self, separatedPlanes, mergedPlanes, peaks, N, weights):
        self.mergedPlanes = mergedPlanes
        self.peaks = peaks
        self.peaksQuadratureDic = {}
        #print("dic type: ", type(self.peaksQuadratureDic))
        self.separatedPlanes = np.array(separatedPlanes)
        self.decayWeights = weights
        self.N = N
        #print("starting with merged planes size: ", self.mergedPlanes.shape)

    def initializeDicToZero(self):
        self.cubicSum = 0
        self.gaussianQuadratureSum  = 0
        self.newCodesSum = 0

    def getAreas(self, size, N, computeCubic=True, computeGaussianQuadrature=True, computeNewCotes=True, simpleVersion=False):
        self.initializeDicToZero()
        self.N = N
        if N == 3:
            self.dx = 3
            self.dy = 3
        elif N == 9:
            self.dx = 1
            self.dy = 1
        elif N == 18:
            self.dx = 1
            self.dy = 1
        else:
            print("Error, don't recognize N!", N)

        print("Looking for area with size: ", size)
        for p in self.peaks:
            upperLeft, lowerRight = self.getCorners(p, size)
            cubicSum, cubicTime = self.getCubicArea(upperLeft, lowerRight) if computeCubic else 0
            ncSum, ncTime = self.getNewCotesArea(upperLeft, lowerRight) if computeNewCotes else 0
            gqSum, gqTime = self.getGaussianQuadratureArea(upperLeft, lowerRight, simpleVersion) if computeGaussianQuadrature else 0
            self.peaksQuadratureDic[p] = QuadratureSums(cubicSum, ncSum, gqSum, cubicTime, ncTime, gqTime)
        return self.peaksQuadratureDic

    def getCubicArea(self, upperLeft, lowerRight):
        startTime = time.time()
        #can't use this as may not take the full range if at the edge of the image, and N inforced when drawing points
        #h = ((lowerRight[1]-upperLeft[1])/self.N) *((lowerRight[0]-upperLeft[0])/self.N)
        sum = 0
        xRangeCount = 0
        yRangeCount = 0
        for y in range(upperLeft[0], lowerRight[0] + 1):
            if self.isInRange(y,0):
                yRangeCount = yRangeCount + 1
                for x in range(upperLeft[1], lowerRight[1] + 1):
                    if self.isInRange(x,1):
                        sum = sum + self.mergedPlanes[y,x]
                        xRangeCount = xRangeCount + 1
                    else:
                        print("Trying to get area outside bounds!")
        sum = sum * self.dx * self.dy 
        print("Got cubic area of: ", sum)
        timeTook = time.time() - startTime
        return sum, timeTook

    def getGaussianQuadratureArea(self, upperLeft, lowerRight, simpleVersion=False):
        startTime = time.time()
        gqlookup = gaussianQuadratureLookup.GaussianQuadratureLookup(self.N)
        weights, xs = gqlookup.getWeightsAndVariables()
        stddev = 2
        print("Getting number of weights: ", len(weights), " with sum: ", np.sum(np.array(weights)))

        totalSum = 0
        #we need i and j to move between the domain given, so we'll adjust to make this applicable
        xRange = float(lowerRight[1] - upperLeft[1] + 1)
        yRange = float(lowerRight[0] - upperLeft[0] + 1)
        xMin = upperLeft[1]
        xMax = lowerRight[1]
        yMin = upperLeft[0]
        yMax = lowerRight[0]
        Xincrement = xRange/self.N
        Yincrement = yRange/self.N
        gaussianSpan = 4

        #need to add a gaussian for each plane we find a point within this domain space
        for planeIdx in range(len(self.separatedPlanes)):
            planeSum = 0
            for xIdx in range(upperLeft[1],lowerRight[1]+1):
                for yIdx in range(upperLeft[0], lowerRight[0]+1):
                    if self.separatedPlanes[planeIdx, yIdx, xIdx] == 1:
                        peak = (yIdx, xIdx)
                        peakVal = 0
                        #if there is a peak here, find the area of this gaussian, and add it to the sum with the weight of the plane
                        #get new bounds in case it's off center
                        gxMin = max(xMin, xIdx - gaussianSpan)
                        gyMin = max(yMin, yIdx - gaussianSpan)
                        gxMax = min(xMax, xIdx + gaussianSpan)
                        gyMax = min(yMax, yIdx + gaussianSpan)
                        gxRange = float(gxMax - gxMin + 1)
                        gyRange = float(gyMax - gyMin + 1)
                        print("Total weights: ", len(weights))
                        for i in range(len(weights)):
                            xConverted = gxMin + (((xs[i] + 1)/2.0)*gxRange)
                            for j in range(len(weights)):
                                yConverted = gyMin + (((xs[j] + 1)/2.0)*gyRange)
                                #print("X converted: ", xConverted, ", Y Converted: ", yConverted, "X init: ", xs[i], ", Y init: ", xs[j])
                                if simpleVersion:
                                    #print("Doing simple version!")
                                    newVal = 1*weights[i]
                                else:
                                    newVal = weights[i] * gaussianEquation.getGaussianDistributionValue(peak, xConverted, yConverted, stddev)
                                peakVal = newVal + peakVal
                        #print("Peak total: ", peakVal, " xRange: ", gxRange, ", yRange: ", gyRange)
                        peakVal = peakVal * gxRange/2.0 * gyRange/2.0 * self.getChangeInIntegralMultiplier(gxMin, gxMax) * self.getChangeInIntegralMultiplier(gyMin, gyMax) / (self.N*23.855)
                        #print("Updated peak sum: ", peakVal)
                        #add to plane
                        planeSum = planeSum + peakVal
            #multiply plane sum by plane weight
            planeSum = planeSum * self.decayWeights[planeIdx]
            #add to total sum
            totalSum = totalSum + planeSum
            
        #sum = sum/2.0  
        #sum = sum * (xRange*yRange/(2*self.N))
        #sum = sum * Xincrement * Yincrement/2.0
        #sum = sum * (xRange/2.0) * (yRange/2.0)
        #we want to give the weight of the rest of the frames that had a point near it
        #sum = sum * self.dx * self.dy
        print("Got Gaussian Quadrature area of: ", totalSum)
        timeTook = time.time() - startTime
        return totalSum, timeTook

    def getChangeInIntegralMultiplier(self, a, b):
        #val = ( (a*b) - (a*a) - (b*b) + (a*b) )/(a-b)
        #val = (-1/(a-b) + 1/(b-a))
        #val = np.sqrt((math.pi)**self.N)
        val = (b-a)/2
        print("Val: ", val)
        #return val/(1.628*self.N)
        return val

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

    #Simpson's rule over one subinterval, adapted for 2d to cover a 3x3 space
    def getNewCotesArea(self, upperLeft, lowerRight):
        startTime = time.time()
        #h = ((lowerRight[1]-upperLeft[1])/self.N) *((lowerRight[0]-upperLeft[0])/self.N)
        sum = 0
        multiplier = 3 if self.N == 3 else 1
        for y in range(upperLeft[0], lowerRight[0] + 1):
            for x in range(upperLeft[1], lowerRight[1] + 1):
                if self.isInRange(y,0) and self.isInRange(x,1):
                    #clear out and start new addition for the cell
                    runningCount = self.mergedPlanes[y,x] * 4
                    countAdded = 4
                    if self.isInRangeOfDomain(x-1,1, upperLeft, lowerRight):
                        runningCount = runningCount + self.mergedPlanes[y,x-1]
                        countAdded = countAdded + 1
                        if self.isInRangeOfDomain(y+1,0, upperLeft, lowerRight):
                            runningCount = runningCount + self.mergedPlanes[y+1,x-1]
                            countAdded = countAdded + 1
                        if self.isInRangeOfDomain(y-1,0, upperLeft, lowerRight):
                            runningCount = runningCount + self.mergedPlanes[y-1,x-1]
                            countAdded = countAdded + 1                        
                    if self.isInRangeOfDomain(x+1,1, upperLeft, lowerRight):
                        runningCount = runningCount + self.mergedPlanes[y,x+1]
                        countAdded = countAdded + 1
                        if self.isInRangeOfDomain(y+1,0, upperLeft, lowerRight):
                            runningCount = runningCount + self.mergedPlanes[y+1,x+1]
                            countAdded = countAdded + 1
                        if self.isInRangeOfDomain(y-1,0, upperLeft, lowerRight):
                            runningCount = runningCount + self.mergedPlanes[y-1,x+1]
                            countAdded = countAdded + 1
                    if self.isInRangeOfDomain(y+1,0, upperLeft, lowerRight):
                        runningCount = runningCount + self.mergedPlanes[y+1,x]
                        countAdded = countAdded + 1
                    if self.isInRangeOfDomain(y-1,0, upperLeft, lowerRight):
                        runningCount = runningCount + self.mergedPlanes[y-1,x]
                        countAdded = countAdded + 1
                    runningCount = runningCount/countAdded
                    sum = sum + runningCount
                    #print("Sum: ", sum, " with running count: ", runningCount, " x: ", x, " y: ", y, " count added: ", countAdded)
                else:
                    print("Trying to get area outside bounds!")
        sum = sum * self.dx * self.dy
        print("Got new cotes area of: ", sum)
        timeTook = time.time() - startTime
        return sum, timeTook

    def isInRangeOfDomain(self, point, axis, upperLeft, lowerRight):
        if (point >= upperLeft[axis]) and (point < lowerRight[axis]):   
            return True
        return False

    def isInRange(self, point, axis):
        if (point >= 0) and (point < self.mergedPlanes.shape[axis]):
            return True
        return False

    def getCorners(self, peakPoint, size):
        upperLeft = (max((peakPoint[0] - size), 0), max((peakPoint[1] - size), 0))
        lowerRight = (min((peakPoint[0] + size), (len(self.mergedPlanes)-1)), min((peakPoint[1] + size), (self.mergedPlanes.shape[1]-1)))
        #print("Found upper left: ", upperLeft, ", lower right corner: ", lowerRight)
        return upperLeft, lowerRight
        