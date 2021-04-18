import numpy as np
import quadratureCalculator as qc
import planeMerger
import matplotlib.pyplot as plt
import peakFinder

if __name__ == "__main__":
    #establish one target in the center
    plane = np.zeros((100,100))
    plane[50,50] = 1
    peakThreshold = 5e-50

    #make the gaussian distribution for one target at one time step
    merger = planeMerger.PlaneMerger([plane], [1])
    mergedPlanes = merger.mergePlanes()
    pf = peakFinder.PeakFinder(mergedPlanes)
    secondDerivImage = pf.getSecondDerivative()   
    peaks = pf.getPeaks(peakThreshold)
    areas = None
    print(peaks)
    if len(peaks) > 0:
        quadrature = qc.QuadratureCalculator([plane], mergedPlanes, peaks, 16)
        size = 50
        ns = [4, 8, 12, 16, 32]
        expectedArea = 1
        cubicArea = []
        newCotesArea = []
        gaussianQuadratureArea = []

        for N in ns:
            areas = quadrature.getAreas(size, N)  
            cubicArea.append(areas.cubesSum)
            newCotesArea.append(areas.newCotesSum)
            gaussianQuadratureArea.append(areas.gaussianQuadratureSum)

        plt.plot(ns, cubicArea, 'g')
        plt.plot(ns, newCotesArea, 'b')
        plt.plot(ns, gaussianQuadratureArea, 'r') 
        plt.show()  


    
