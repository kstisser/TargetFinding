import numpy as np
import matplotlib.pyplot as plt 
import planeMerger as pm
import peakFinder
import quadratureCalculator as qc
import visualizer
from PIL import Image as im
from random import random

class PlaneManager:
    def __init__(self, movers, domainSize, noise, peakThreshold = 1e-2, resolution = 9, singlePoint = True, display=False):
        self.viz = visualizer.Visualizer()
        self.movers = movers
        self.domainSize = domainSize
        self.singlePoint = singlePoint
        self.peakThreshold = peakThreshold
        self.resolution = resolution
        self.planeQueue = []
        w = np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
        self.decayWeights = w/np.sum(w)
        #self.decayWeights = np.array([1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])
        self.timeStep = 0
        self.noise = noise
        print("Decay weight sum: ", np.sum(self.decayWeights))
        print("Decay weights: ", self.decayWeights)
        if display:
            plt.plot(range(0,len(self.decayWeights),1), self.decayWeights, 'go')
            plt.title("Decay weights")
            plt.show()

    def updateThreshold(self, threshold):
        self.peakThreshold = threshold

    def updateResolution(self, res):
        self.resolution = res

    def updateSize(self, size):
        self.size = size

    #add a plane to the queue, though ensure the queue does not exceed 10 planes
    def addPlane(self, plane):
        self.planeQueue.append(plane)
        while(len(self.planeQueue) > 10):
            self.planeQueue.pop(0)

    def plotMoversWithNewTimestep(self):
        self.timeStep = self.timeStep + 1
        newPlane = np.zeros(self.domainSize)
        print('Mover number: ', len(self.movers))
        for mov in self.movers:
            newPosition = mov.getPosition(self.timeStep)
            print("New point: ", newPosition)
            newPlane[newPosition[0], newPosition[1]] = 1
            #TODO if using multiple points for a moving object, add those based on their direction
        #if using noise, add a few other random points
        if self.noise:
            randomNumberOfPoints = int(random() * 100)
            for i in range(randomNumberOfPoints):
                newPlane[int(random() * self.domainSize[0]), int(random() * self.domainSize[1])] = 1
        self.addPlane(newPlane)
        print("Nonzero values in new Plane: ", np.count_nonzero(newPlane)) 

    #establish a weighting scheme to ensure there is a decay to the weights of the oldest
    def mergePlanes(self, N, size, threshold, simpleVersion=False, scenarioName="Name"):
        merger = pm.PlaneMerger(self.planeQueue, self.decayWeights)
        mergedPlanes = merger.mergePlanes(self.resolution, simpleVersion)
        pf = peakFinder.PeakFinder(mergedPlanes)
        secondDerivImage = pf.getSecondDerivative()
        print("Nonzero values in second derivative: ", np.count_nonzero(secondDerivImage)) 
        print(secondDerivImage.shape)
        #img = im.fromarray(secondDerivImage, 'RGB')
        #img.show()        
        peaks = pf.getPeaks(self.peakThreshold)
        areas = None
        print(peaks)
        if len(peaks) > 0:
            quadrature = qc.QuadratureCalculator(self.planeQueue, mergedPlanes, peaks, self.resolution, self.decayWeights)
            areas = quadrature.getAreas(size, N, simpleVersion=simpleVersion, scenarioName=scenarioName)
        return self.planeQueue, mergedPlanes, secondDerivImage, peaks, areas
