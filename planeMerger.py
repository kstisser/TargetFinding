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

        #meshgrid used for gaussian calculations
        numGrids, xlength, ylength = self.referencePlanes.shape
        X = np.arange(0,xlength,1)
        Y = np.arange(0,ylength,1)
        self.X = X
        self.Y = Y
        self.X, self.Y = np.meshgrid(self.X, self.Y)

    def mergePlanes(self):
        self.gaussianMixturePlanes = np.zeros(self.referencePlanes.shape)
        print("Gaussian mixture plane shape: ", self.gaussianMixturePlanes.shape)
        for planeIdx in range(len(self.referencePlanes)):
            targetPoints = np.transpose(np.nonzero(self.referencePlanes[planeIdx]))
            for point in targetPoints:
                self.addGaussianDistributionForPoint(point, planeIdx)
            self.gaussianMixturePlanes[planeIdx] = self.gaussianMixturePlanes[planeIdx]
        print("Nonzero values in reference Plane: ", np.count_nonzero(self.referencePlanes)) 
        self.mergePlanesByWeights()
        #self.viz.plotPlane(self.X, self.Y, self.mergedPlane)
        return self.mergedPlane

    #reference for gaussian distribution equation: 
    # https://towardsdatascience.com/a-python-tutorial-on-generating-and-plotting-a-3d-guassian-distribution-8c6ec6c41d03
    def addGaussianDistributionForPoint(self, point, planeIdx):
        #Note- the mean is at the point given, and the variance is fixed above
        xmin = point[1]
        xmax = point[1]
        ymin = point[0]
        ymax = point[0]
        threshold = 0.01
        stddev = 2
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

        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self.gaussianMixturePlanes[planeIdx,y,x] = gaussianEquation.getGaussianDistributionValue(point, x, y, stddev)
                #print("Next calculated value for point x: ", x, ", y: ", y, " : ", gaussianEquation.getGaussianDistributionValue(point, x, y, stddev))
        #print("Max val in gaussian mixture planes: ", np.max(self.gaussianMixturePlanes[planeIdx]))

    #This function both mulitplies the planes by their weights, 
    # and sums the Z direction to collapse all into one 2D array of heights
    def mergePlanesByWeights(self):
        self.mergedPlane = np.zeros((self.referencePlanes.shape[1], self.referencePlanes.shape[2]), dtype=np.float32)
        for i in range(len(self.gaussianMixturePlanes)):
            weightedPlane = np.array(np.multiply(self.gaussianMixturePlanes[i], self.weights[i]))   
            self.mergedPlane = np.add(self.mergedPlane, weightedPlane)
