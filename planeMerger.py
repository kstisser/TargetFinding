import visualizer
import numpy as np
from PIL import Image as im
from scipy.stats import multivariate_normal
import math

class PlaneMerger:
    def __init__(self, planes, weights):
        self.referencePlanes = np.array(planes)
        print("Plane shape: ", self.referencePlanes.shape)
        self.weights = np.array(weights)
        self.viz = visualizer.Visualizer()

        #meshgrid used for gaussian calculations
        numGrids, xlength, ylength = self.referencePlanes.shape
        X = np.arange(0,xlength,1)
        Y = np.arange(0,ylength,1)
        self.X = X
        self.Y = Y
        self.X, self.Y = np.meshgrid(self.X, self.Y)
        '''X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**2)
        Z = ((1./np.sqrt(2. * np.pi)) * np.exp(-0.5 * R**2))
        print(Z)'''

    def mergePlanes(self):
        self.gaussianMixturePlanes = np.zeros(self.referencePlanes.shape)
        print("Gaussian mixture plane shape: ", self.gaussianMixturePlanes.shape)
        for planeIdx in range(len(self.referencePlanes)):
            targetPoints = np.transpose(np.nonzero(self.referencePlanes[planeIdx]))
            print("Nonzero target points: ")
            print(targetPoints)
            for point in targetPoints:
                self.addGaussianDistributionForPoint(point, planeIdx)
            self.gaussianMixturePlanes[planeIdx] = self.gaussianMixturePlanes[planeIdx]
            print("Max after multiplying: ", np.max(self.gaussianMixturePlanes[planeIdx]))
        print("New plane with gaussian added")
        print("Nonzero values in reference Plane: ", np.count_nonzero(self.referencePlanes)) 
        #img = im.fromarray(self.referencePlanes[0], 'RGB')
        #img.show()
        self.mergePlanesByWeights()
        #self.viz.plotPlane(self.X, self.Y, self.mergedPlane)
        return self.mergedPlane

    #reference for gaussian distribution equation: 
    # https://towardsdatascience.com/a-python-tutorial-on-generating-and-plotting-a-3d-guassian-distribution-8c6ec6c41d03
    def addGaussianDistributionForPoint(self, point, planeIdx):
        #Note- the mean is at the point given, and the variance is fixed above
        '''blankPlane = np.zeros(self.referencePlanes.shape)
        densityAdded = multivariate_normal.pdf(blankPlane, mean=2.5, cov=0.5)
        self.gaussianMixturePlanes = np.add(self.gaussianMixturePlanes, densityAdded)'''
        xmin = point[1]
        xmax = point[1]
        ymin = point[0]
        ymax = point[0]
        print("Point: ", point)
        threshold = 0.01
        stddev = 2
        firstVal = self.getGaussianDistributionValue(point, point[1], point[0], stddev)
        currentVal = firstVal
        print("First val: ", currentVal)
        #extend left until value is small enough not to keep going
        while currentVal > threshold and ymin > 0:
            ymin = max(0, ymin - 1)
            currentVal = self.getGaussianDistributionValue(point, point[1], ymin, stddev)
        print("Chosen ymin: ", ymin)

        #extend up until value is small enough not to keep going
        currentVal = firstVal
        while currentVal > threshold and xmin > 0:
            xmin = max(0, xmin - 1)
            currentVal = self.getGaussianDistributionValue(point, xmin, point[0], stddev)
        print("Chosen xmin: ", xmin)

        #extend right until value is small engouh not to keep going
        currentVal = firstVal
        while currentVal > threshold and ymax < (self.gaussianMixturePlanes[planeIdx].shape[0] - 1):
            ymax = min(self.gaussianMixturePlanes[planeIdx].shape[0] - 1, ymax + 1)
            currentVal = self.getGaussianDistributionValue(point, point[1], ymax, stddev)
        print("Chosen ymax: ", ymax)

        #extend down until value is small enough not to keep going
        currentVal = firstVal
        while currentVal > threshold and xmax < (self.gaussianMixturePlanes[planeIdx].shape[1] - 1):
            xmax = min(self.gaussianMixturePlanes[planeIdx].shape[1] - 1, xmax + 1)
            currentVal = self.getGaussianDistributionValue(point, xmax, point[0], stddev)
        print("Chosen xmax: ", xmax)

        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self.gaussianMixturePlanes[planeIdx,y,x] = self.getGaussianDistributionValue(point, x, y, stddev)
                #print("Next calculated value for point x: ", x, ", y: ", y, " : ", self.getGaussianDistributionValue(point, x, y, stddev))
        print("Max val in gaussian mixture planes: ", np.max(self.gaussianMixturePlanes[planeIdx]))

    def getGaussianDistributionValue(self, mean, x, y, stddev):
        return 1.0/(2.0 * math.pi * stddev * stddev) * math.exp(-((x - mean[1])**2 + (y - mean[0])**2)/(2 * stddev * stddev))

    #This function both mulitplies the planes by their weights, 
    # and sums the Z direction to collapse all into one 2D array of heights
    def mergePlanesByWeights(self):
        self.mergedPlane = np.zeros((self.referencePlanes.shape[1], self.referencePlanes.shape[2]), dtype=np.float32)
        #print("Merge planes")
        for i in range(len(self.gaussianMixturePlanes)):
            weightedPlane = np.array(np.multiply(self.gaussianMixturePlanes[i], self.weights[i]))   
            #print("Nonzero values in weighted Plane: ", np.count_nonzero(weightedPlane))    
            #self.viz.plotPlane(self.X, self.Y, weightedPlane)
            #img = im.fromarray(weightedPlane, 'RGB')
            #img.show()
            self.mergedPlane = np.add(self.mergedPlane, weightedPlane)
        #print("Max val in merged planes: ", np.max(self.mergedPlane))
