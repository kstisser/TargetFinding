import numpy as np
import quadratureCalculator as qc
import planeMerger
import matplotlib.pyplot as plt
import peakFinder

if __name__ == "__main__":
    ###########################################################################################
    #########First test: simple F = 1 plot (error shows 1e-13, so looks big but is small)######
    ###########################################################################################
    #establish one target in the center at different comparable resolutions and Ns
    plane = np.zeros((100,100))
    plane[50,50] = 1
    peakThreshold = 1e-2
    weights = [1]

    #make the gaussian distribution for one target at one time step
    merger = planeMerger.PlaneMerger([plane], weights)
    expectedArea = 81
    size = 4

    cubicArea = []
    newCotesArea = []
    gaussianQuadratureArea = [] 

    cubicError = []
    newCotesError = []
    gaussianQuadratureError = []   

    resolutions = [3, 9, 18]
    for i in range(len(resolutions)):
        #True enforces simple version of f = 1 function
        mergedPlanes = merger.mergePlanes(resolutions[i], simpleVersion=True)
        pf = peakFinder.PeakFinder(mergedPlanes)
        secondDerivImage = pf.getSecondDerivative()   
        peaks = pf.getPeaks(peakThreshold)
        print(peaks)
        if len(peaks) > 0:       
            areas = None            
            quadrature = qc.QuadratureCalculator([plane], mergedPlanes, peaks, resolutions[i], weights)

            areas = quadrature.getAreas(size, resolutions[i], simpleVersion=True)  
            for p in peaks:
                print("Adding areas for resolution: ", resolutions[i])
                print("Results (N): ", resolutions[i], " Cubic: ", areas[p].cubeSum, " NC: ", areas[p].newCotesSum, "GQ: ", areas[p].gaussianQuadratureSum)
                cubicArea.append(areas[p].cubeSum)
                newCotesArea.append(areas[p].newCotesSum)
                gaussianQuadratureArea.append(areas[p].gaussianQuadratureSum)

                cubicError.append(abs(expectedArea - areas[p].cubeSum))
                newCotesError.append(abs(expectedArea - areas[p].newCotesSum))
                gaussianQuadratureError.append(abs(expectedArea - areas[p].gaussianQuadratureSum))

    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(resolutions, cubicArea, 'go', label = 'Cubic')
    ax1.plot(resolutions, newCotesArea, 'b*', label = 'New Cotes')
    ax1.plot(resolutions, gaussianQuadratureArea, 'r--', label = 'Gaussian Quadrature')
    ax1.set_title("Area Calculation of Simple F=1") 
    ax1.set_xlabel("Resolution (N)")
    ax1.set_ylabel("Area")
    ax1.legend()

    ax2 = plt.subplot(2, 2, 3)
    ax2.plot(resolutions, cubicError, 'g--', label = 'Cubic')
    ax2.plot(resolutions, newCotesError, 'b--', label = 'New Cotes')
    ax2.plot(resolutions, gaussianQuadratureError, 'r--', label = 'Gaussian Quadrature')
    ax2.set_title("Error")
    ax2.set_xlabel("Resolution (N)")
    ax2.set_ylabel("Error difference from expected Simple")   
    ax2.legend()      
     

    ###########################################################################################
    #########Second test: single gaussian plot ################################################
    ###########################################################################################
    #establish one target in the center at different comparable resolutions and Ns
    plane = np.zeros((100,100))
    plane[50,50] = 1
    peakThreshold = 1e-2
    weights = [1]

    #make the gaussian distribution for one target at one time step
    merger = planeMerger.PlaneMerger([plane], weights)
    expectedArea = 1
    size = 5

    cubicArea = []
    newCotesArea = []
    gaussianQuadratureArea = [] 

    cubicError = []
    newCotesError = []
    gaussianQuadratureError = []   

    resolutions = [3, 9, 18]
    for i in range(len(resolutions)):
        #True enforces simple version of f = 1 function
        mergedPlanes = merger.mergePlanes(resolutions[i], simpleVersion=False)
        pf = peakFinder.PeakFinder(mergedPlanes)
        secondDerivImage = pf.getSecondDerivative()   
        peaks = pf.getPeaks(peakThreshold)
        print(peaks)
        if len(peaks) > 0:       
            areas = None            
            quadrature = qc.QuadratureCalculator([plane], mergedPlanes, peaks, resolutions[i], weights)

            areas = quadrature.getAreas(size, resolutions[i], simpleVersion=False)  
            for p in peaks:
                print("Adding areas for resolution: ", resolutions[i])
                print("Results (N): ", resolutions[i], " Cubic: ", areas[p].cubeSum, " NC: ", areas[p].newCotesSum, "GQ: ", areas[p].gaussianQuadratureSum)
                cubicArea.append(areas[p].cubeSum)
                newCotesArea.append(areas[p].newCotesSum)
                gaussianQuadratureArea.append(areas[p].gaussianQuadratureSum)

                cubicError.append(abs(expectedArea - areas[p].cubeSum))
                newCotesError.append(abs(expectedArea - areas[p].newCotesSum))
                gaussianQuadratureError.append(abs(expectedArea - areas[p].gaussianQuadratureSum))
    
    ax3 = plt.subplot(2, 2, 2)
    ax3.plot(resolutions, cubicArea, 'go', label = 'Cubic')
    ax3.plot(resolutions, newCotesArea, 'b*', label = 'New Cotes')
    ax3.plot(resolutions, gaussianQuadratureArea, 'r--', label = 'Gaussian Quadrature')
    ax3.set_title("Area Calculation of 1 Gaussian") 
    ax3.set_xlabel("Resolution (N)")
    ax3.set_ylabel("Area")
    ax3.legend()

    ax4 = plt.subplot(2, 2, 4)
    ax4.plot(resolutions, cubicError, 'g--', label = 'Cubic')
    ax4.plot(resolutions, newCotesError, 'b--', label = 'New Cotes')
    ax4.plot(resolutions, gaussianQuadratureError, 'r--', label = 'Gaussian Quadrature')
    ax4.set_title("Error")
    ax4.set_xlabel("Resolution (N)")
    ax4.set_ylabel("Error difference from expected Gaussian")   
    ax4.legend()  

    plt.show()