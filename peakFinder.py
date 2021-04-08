import numpy as np
from scipy.ndimage import laplace

class PeakFinder:
    def __init__(self, mergedPlane):
        self.mergedPlane = mergedPlane

    def getSecondDerivative(self):
        self.secondDer = laplace(self.mergedPlane)
        return self.secondDer

    def getPeaks(self, threshold):
        return np.where(self.secondDer >= threshold)