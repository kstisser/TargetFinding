import numpy as np
from scipy.ndimage import laplace
from PIL import Image as im
import visualizer

class PeakFinder:
    def __init__(self, mergedPlane):
        self.mergedPlane = mergedPlane
        self.viz = visualizer.Visualizer()

    def getSecondDerivative(self):
        self.secondDer = laplace(self.mergedPlane)
        #print("Second deriv max: ", np.max(self.secondDer))     
        return self.secondDer

    def getPeaks(self, threshold):
        #make sure we're only looking at peaks, and not looking where there was nothing originally
        whereZero = np.transpose(np.where(self.mergedPlane == 0))
        noTargetPlane = np.zeros(self.mergedPlane.shape)
        for i in whereZero:
            noTargetPlane[i[0],i[1]] = 100
        #print("Checking this aligns, pairs: ", len(whereZero), " nonzero plane: ", np.count_nonzero(noTargetPlane))
        combinedForPeaks = np.add(noTargetPlane, self.secondDer)
        print("Min val: ", np.min(combinedForPeaks))
        thresh = 1e-5
        peaks = np.where(np.abs(combinedForPeaks) <= thresh)
        X = np.arange(0,100,1)
        Y = X
        #print(combinedForPeaks.shape)
        #self.viz.plotPlane(X, Y, combinedForPeaks)
        print("Peaks found:")
        print(np.count_nonzero(peaks))
        #TODO merge peaks
        return np.transpose(peaks)

    def mergePeaks(self, peaks):
        #TODO
        pass