import numpy as np
import quadratureCalculator as qc
import planeMerger
import matplotlib.pyplot as plt
import peakFinder

if __name__ == "__main__":
    #establish one target in the center at different comparable resolutions and Ns
    plane = np.zeros((100,100))
    plane[50,50] = 1
    peakThreshold = 1e-2
    weights = [1]

    #make the gaussian distribution for one target at one time step
    merger = planeMerger.PlaneMerger([plane], weights)
    expectedArea = 1
    size = 50

    cubicArea = []
    newCotesArea = []
    gaussianQuadratureArea = [] 

    cubicError = []
    newCotesError = []
    gaussianQuadratureError = []   

    resolutions = [3, 9, 18]
    for i in range(len(resolutions)):
        mergedPlanes = merger.mergePlanes(resolutions[i])
        pf = peakFinder.PeakFinder(mergedPlanes)
        secondDerivImage = pf.getSecondDerivative()   
        peaks = pf.getPeaks(peakThreshold)
        print(peaks)
        if len(peaks) > 0:       
            areas = None            
            quadrature = qc.QuadratureCalculator([plane], mergedPlanes, peaks, resolutions[i], weights)

            areas = quadrature.getAreas(size, resolutions[i])  
            for p in peaks:
                print("Adding areas for resolution: ", resolutions[i])
                cubicArea.append(areas[p].cubeSum)
                newCotesArea.append(areas[p].newCotesSum)
                gaussianQuadratureArea.append(areas[p].gaussianQuadratureSum)

                cubicError.append(expectedArea - areas[p].cubeSum)
                newCotesError.append(expectedArea - areas[p].newCotesSum)
                gaussianQuadratureError.append(expectedArea - areas[p].gaussianQuadratureSum)

    print("Cube area shape: ", np.array(cubicArea).shape)
    print(cubicArea)
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(resolutions, cubicArea, 'g', label = 'Cubic')
    ax1.plot(resolutions, newCotesArea, 'b', label = 'New Cotes')
    ax1.plot(resolutions, gaussianQuadratureArea, 'r', label = 'Gaussian Quadrature')
    ax1.set_title("Area Calculation of 1 Gaussian") 
    ax1.set_xlabel("Resolution (N)")
    ax1.set_ylabel("Area")
    ax1.legend()

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(resolutions, cubicError, 'g', label = 'Cubic')
    ax2.plot(resolutions, newCotesError, 'b', label = 'New Cotes')
    ax2.plot(resolutions, gaussianQuadratureError, 'r', label = 'Gaussian Quadrature')
    ax2.set_title("Error")
    ax2.set_xlabel("Resolution (N)")
    ax2.set_ylabel("Error difference from expected")   
    ax2.legend()      
    plt.show()  


    
