import visualizer
import numpy as np
from PIL import Image as im

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
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**2)
        Z = ((1./np.sqrt(2. * np.pi)) * np.exp(-0.5 * R**2))
        print(Z)

        #Fixed gaussian distribution parameters
        self.variance = 0.25

    def mergePlanes(self):
        self.gaussianMixturePlanes = np.zeros(self.referencePlanes.shape)
        print("Gaussian mixture plane shape: ", self.gaussianMixturePlanes.shape)
        targetPoints = np.nonzero(self.referencePlanes)
        for point in targetPoints:
            self.addGaussianDistributionForPoint(point)
        print("New plane with gaussian added")
        print("Nonzero values in reference Plane: ", np.count_nonzero(self.referencePlanes)) 
        img = im.fromarray(self.referencePlanes, 'RGB')
        img.show()
        self.mergePlanesByWeights()
        self.viz.plotPlane(self.X, self.Y, self.mergedPlane)

    #reference for gaussian distribution equation: 
    # https://towardsdatascience.com/a-python-tutorial-on-generating-and-plotting-a-3d-guassian-distribution-8c6ec6c41d03
    def addGaussianDistributionForPoint(self, point):
        #Note- the mean is at the point given, and the variance is fixed above
        #TODO
        pass

    #This function both mulitplies the planes by their weights, 
    # and sums the Z direction to collapse all into one 2D array of heights
    def mergePlanesByWeights(self):
        self.mergedPlane = np.zeros((self.referencePlanes.shape[1], self.referencePlanes.shape[2]), dtype=np.float32)
        print("Merge planes")
        #img = im.fromarray(self.mergePlanes, 'RGB')
        #img.show()
        for i in range(len(self.gaussianMixturePlanes)):
            weightedPlane = np.array(np.multiply(self.gaussianMixturePlanes[i], self.weights[i]))
            print("Weighted Plane")
            #img = im.fromarray(weightedPlane, 'RGB')
            #img.show()        
            print("Nonzero values in weighted Plane: ", np.count_nonzero(weightedPlane))    
            print(weightedPlane.shape)
            print(type(weightedPlane))
            print(self.mergedPlane.shape)
            print(type(self.mergedPlane))
            print(self.mergedPlane)
            #self.viz.plotPlane(self.X, self.Y, weightedPlane)
            self.mergedPlane = np.add(self.mergedPlane, weightedPlane)
            print("Merged planes")
            #img = im.fromarray(self.mergedPlane, 'RGB')
            #img.show()
