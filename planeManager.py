import numpy as np
import matplotlib.pyplot as plt 
import planeMerger as pm
import peakFinder
import quadratureCalculator as qc
import visualizer

class PlaneManager:
    def __init__(self, movers, domainSize, singlePoint = True, display=False):
        self.viz = visualizer.Visualizer()
        self.movers = movers
        self.domainSize = domainSize
        self.singlePoint = singlePoint
        self.peakThreshold = 1
        self.planeQueue = []
        self.decayWeights = np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
        self.decayWeights = self.decayWeights/np.sum(self.decayWeights)
        self.timeStep = 0
        print("Decay weight sum: ", np.sum(self.decayWeights))
        print("Decay weights: ", self.decayWeights)
        if display:
            plt.plot(range(0,len(self.decayWeights),1), self.decayWeights, 'go')
            plt.title("Decay weights")
            plt.show()

    #add a plane to the queue, though ensure the queue does not exceed 10 planes
    def addPlane(self, plane):
        self.planeQueue.append(plane)
        while(len(self.planeQueue) > 10):
            self.planeQueue.pop(0)

    def plotMoversWithNewTimestep(self):
        self.timeStep = self.timeStep + 1
        newPlane = np.zeros(self.domainSize)
        for mov in self.movers:
            newPlane[mov.lastPoint] = 1
            #TODO if using multiple points for a moving object, add those based on their direction
        self.addPlane(newPlane)

    #establish a weighting scheme to ensure there is a decay to the weights of the oldest
    def mergePlanesAndDisplay(self):
        merger = pm.PlaneMerger(self.planeQueue, self.decayWeights)
        mergedPlanes = merger.mergePlanes()
        pf = peakFinder.PeakFinder(mergedPlanes)
        secondDerivImage = pf.getSecondDerivative()
        peaks = pf.getPeaks(self.peakthreshold)
        quadrature = qc.QuadratureCalculator(mergedPlanes, peaks)
        cubicAreaPerson = quadrature.getCubicArea(defs.ObjectType.PERSON)
        cubicAreaCar = quadrature.getCubicArea(defs.ObjectType.CAR)
        triangularAreaPerson = quadrature.getTriangularArea(defs.ObjectType.PERSON)
        triangularAreaCar = quadrature.getTriangularArea(defs.ObjectType.CAR)
        quadratureAreaPerson = quadrature.getQuadratureArea(objectType)(defs.ObjectType.PERSON)
        quadratureAreaPerson = quadrature.getQuadratureArea(defs.ObjectType.CAR)