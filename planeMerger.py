import visualizer
import numpy as np
from PIL import Image as im
from scipy.stats import multivariate_normal
import math
import gaussianEquation

class PlaneMerger:
    def __init__(self, planes, weights):
        self.referencePlanes = np.array(planes)
        print("Plane shape: ", self.referencePlanes.shape)
        self.weights = np.array(weights)
        self.viz = visualizer.Visualizer()
        self.baseResolution = 9

        #meshgrid used for gaussian calculations
        numGrids, xlength, ylength = self.referencePlanes.shape
        X = np.arange(0,xlength,1)
        Y = np.arange(0,ylength,1)
        self.X = X
        self.Y = Y
        self.X, self.Y = np.meshgrid(self.X, self.Y)

    def mergePlanes(self, resolution, simpleVersion=False):
        #self.resolutionRatio = resolution/self.baseResolution
        self.res = resolution
        self.gaussianMixturePlanes = np.zeros(self.referencePlanes.shape)
        print("Gaussian mixture plane shape: ", self.gaussianMixturePlanes.shape)
        for planeIdx in range(len(self.referencePlanes)):
            targetPoints = np.transpose(np.where(self.referencePlanes[planeIdx] != 0))
            print("Found target points: ", targetPoints)
            for point in targetPoints:
                print("Adding gaussian distribution for point: ", point)
                self.addGaussianDistributionForPoint(point, planeIdx, simpleVersion)
            self.gaussianMixturePlanes[planeIdx] = self.gaussianMixturePlanes[planeIdx]
        print("Nonzero values in reference Plane: ", np.count_nonzero(self.referencePlanes)) 
        self.mergePlanesByWeights()
        #self.viz.plotPlane(self.X, self.Y, self.mergedPlane)
        return self.mergedPlane

    #reference for gaussian distribution equation: 
    # https://towardsdatascience.com/a-python-tutorial-on-generating-and-plotting-a-3d-guassian-distribution-8c6ec6c41d03
    def addGaussianDistributionForPoint(self, point, planeIdx, simpleVersion=False):
        #Note- the mean is at the point given, and the variance is fixed above
        xmin = point[1]
        xmax = point[1]
        ymin = point[0]
        ymax = point[0]
        threshold = 0.03
        stddev = 2

        print("Adding for plane: ", planeIdx)
        if simpleVersion:
            xmin = max(point[1]-4,0)
            ymin = max(point[0]-4,0)
            xmax = min(point[1]+4,self.gaussianMixturePlanes[planeIdx].shape[1] - 1)
            ymax = min(point[0]+4,self.gaussianMixturePlanes[planeIdx].shape[0] - 1)
        else:
            firstVal = gaussianEquation.getGaussianDistributionValue(point, point[1], point[0], stddev)
            currentVal = firstVal
            #extend left until value is small enough not to keep going
            while currentVal > threshold and ymin > 0:
                ymin = max(0, ymin - 1)
                currentVal = gaussianEquation.getGaussianDistributionValue(point, point[1], ymin, stddev)

            #extend up until value is small enough not to keep going
            currentVal = firstVal
            while currentVal > threshold and xmin > 0:
                xmin = max(0, xmin - 1)
                currentVal = gaussianEquation.getGaussianDistributionValue(point, xmin, point[0], stddev)

            #extend right until value is small engouh not to keep going
            currentVal = firstVal
            while currentVal > threshold and ymax < (self.gaussianMixturePlanes[planeIdx].shape[0] - 1):
                ymax = min(self.gaussianMixturePlanes[planeIdx].shape[0] - 1, ymax + 1)
                currentVal = gaussianEquation.getGaussianDistributionValue(point, point[1], ymax, stddev)

            #extend down until value is small enough not to keep going
            currentVal = firstVal
            while currentVal > threshold and xmax < (self.gaussianMixturePlanes[planeIdx].shape[1] - 1):
                xmax = min(self.gaussianMixturePlanes[planeIdx].shape[1] - 1, xmax + 1)
                currentVal = gaussianEquation.getGaussianDistributionValue(point, xmax, point[0], stddev)

        count = 0
        gSum = 0
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                if self.res == 3:
                    #fill in 1/3 as many values for lower resolution
                    if (point[1]-x)%3 != 0 or (point[0]-y)%3 != 0:
                        continue
                    else:
                        xmod = int(point[1] + (point[1]-x)/3)
                        ymod = int(point[0] + (point[0]-y)/3)
                        val = 1 if simpleVersion else gaussianEquation.getGaussianDistributionValue(point, x, y, stddev)/4.0
                        self.gaussianMixturePlanes[planeIdx,ymod,xmod] = val
                elif self.res == 9:
                    #regular resolution
                    val = 1 if simpleVersion else gaussianEquation.getGaussianDistributionValue(point, x, y, stddev)/4.0
                    self.gaussianMixturePlanes[planeIdx,y,x] = val
                elif self.res == 18:
                    #fill in twice as many values for higher resolution (added together as we're not changing dimensions)
                    xmod1 = int(point[1] + (point[1] - x - 1)*2 + 1)
                    ymod1 = int(point[0] + (point[0] - y - 1)*2 + 1)
                    val1 = 0.5 if simpleVersion else gaussianEquation.getGaussianDistributionValue(point, x, y, stddev)/8.0
                    self.gaussianMixturePlanes[planeIdx,ymod1,xmod1] = val1

                    xmod2 = int(point[1] + (point[1] - x - 1)*2 + 2)
                    ymod2 = int(point[0] + (point[0] - y - 1)*2 + 2)
                    val2 = 0.5 if simpleVersion else gaussianEquation.getGaussianDistributionValue(point, (x+0.5), (y+0.5), stddev)/8.0
                    val = (val1 + val2)
                    self.gaussianMixturePlanes[planeIdx,ymod2,xmod2] = val2
                else:
                    print("Error! don't recognize res value!", self.res)

                
                #print("Computed value: ", self.gaussianMixturePlanes[planeIdx,y,x], " for x: ", x, " y: ", y) 
                gSum = gSum + val
                count = count + 1

        print("total sum: ", gSum)
        print("Calculated between points: X:", xmin, ", ", xmax, ", Y:", ymin, ", ", ymax, " for count: ", count )
        print("Sum of merged plane ", planeIdx, ": ", np.sum(self.gaussianMixturePlanes[planeIdx]))
                #print("Next calculated value for point x: ", x, ", y: ", y, " : ", gaussianEquation.getGaussianDistributionValue(point, x, y, stddev))
        #print("Max val in gaussian mixture planes: ", np.max(self.gaussianMixturePlanes[planeIdx]))

    #This function both mulitplies the planes by their weights, 
    # and sums the Z direction to collapse all into one 2D array of heights
    def mergePlanesByWeights(self):
        self.mergedPlane = np.zeros((self.referencePlanes.shape[1], self.referencePlanes.shape[2]), dtype=np.float32)
        for i in range(len(self.gaussianMixturePlanes)):
            weightedPlane = np.array(np.multiply(self.gaussianMixturePlanes[i], self.weights[i]))   
            self.mergedPlane = np.add(self.mergedPlane, weightedPlane)
