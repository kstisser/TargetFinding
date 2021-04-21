import numpy as np
from scipy.ndimage import laplace, gaussian_filter
from PIL import Image as im
import visualizer
from sklearn.cluster import DBSCAN

class PeakFinder:
    def __init__(self, mergedPlane):
        self.mergedPlane = mergedPlane
        self.viz = visualizer.Visualizer()
        self.peakThresholdToKeep = 0.015

    def getSecondDerivative(self):
        self.secondDer = laplace(self.mergedPlane)
        self.firstDer = gaussian_filter(self.mergedPlane, sigma=3)
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
        peaks = np.where((combinedForPeaks) < -1e-5)
        X = np.arange(0,100,1)
        Y = X
        #print(combinedForPeaks.shape)
        #self.viz.plotPlane(X, Y, combinedForPeaks)
        self.peaks = np.transpose(peaks)
        self.mergePeaks()
        return self.peaks

    def mergePeaks(self):
        #eliminate any peaks that are too low to be worth clustering
        newPeaks = []
        for peak in self.peaks:
            if self.mergedPlane[peak[0],peak[1]] >= self.peakThresholdToKeep:
                newPeaks.append(peak)
        self.peaks = np.array(newPeaks)

        if (len(self.peaks) > 0):
            #use DBSCAN to cluster
            maximumDistanceBetweenPoints = 10
            minNumPoints = 5
            clustering = DBSCAN(eps=maximumDistanceBetweenPoints, min_samples=minNumPoints).fit(self.peaks)
            #average to find end peaks results
            labeledSet = set(clustering.labels_)
            print("Labeled cluster set: ", labeledSet)
            clusteredPeaks = []
            for l in labeledSet:
                if l != -1:
                    points = []
                    for i in range(len(clustering.labels_)):
                        if clustering.labels_[i] == l:
                            points.append(self.peaks[i])
                    #average all points within the label to get one peak
                    if len(points) > 0:
                        columnVals = np.transpose(np.array(points))
                        col1Mean = int(np.mean(columnVals[0]))
                        col2Mean = int(np.mean(columnVals[1]))
                        clusteredPeaks.append((col1Mean, col2Mean))
                    else:
                        print("Error! No points found in label: ", l)
            print(len(clusteredPeaks), " Peaks found: ", clusteredPeaks)
            self.peaks = clusteredPeaks
            
                

            


        