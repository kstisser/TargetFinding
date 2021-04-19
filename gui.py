import tkinter as tk 
#from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk, )
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import planeManager
import threading
from multiprocessing import Process
import numpy as np
from scipy.stats import multivariate_normal
import cv2

class GuiManager:
    def __init__(self, movers, domainSize, runRate, noise=False):
        self.runRate = runRate
        self.resolution = 18
        self.threshold = 0.5
        self.size = 5
        self.tkGui = tk.Tk()
        w, h = self.tkGui.winfo_screenwidth(), self.tkGui.winfo_screenheight()
        self.tkGui.geometry("%dx%d+0+0" % (w, h))
        self.wholeFrame = tk.Frame(master = self.tkGui)
        self.addWidgets()
        self.pm = planeManager.PlaneManager(movers, domainSize, noise)
        self.X = np.arange(0, domainSize[1])
        self.Y = np.arange(0, domainSize[0])
        self.X, self.Y = np.meshgrid(self.X, self.Y)
        self.noise = noise
        
    def runGUI(self):
        self.tkGui.mainloop()

    def start(self):
        while True:
            startTime = time.time()
            self.pm.plotMoversWithNewTimestep()
            r = self.resolution
            s = self.size
            t = self.threshold
            rate = self.runRate
            separatedPlanes, mergedPlanes, secondDerivative, peaks, areas = self.pm.mergePlanes(r, s, t)
            self.updatePlots(separatedPlanes, mergedPlanes, secondDerivative, peaks, areas)
            self.tkGui.update()
            #sleep amount of time still needed after processing to get to the run rate
            endTime = time.time()
            print("Process time: ", (endTime - startTime))
            waitTime = rate - (time.time() - startTime)
            if waitTime > 0:
                time.sleep(waitTime) 

    def getTestXYZ(self, sigmaVal):
        x, y = np.mgrid[-1.0:1.0:30j, -1.0:1.0:30j]

        # Need an (N, 2) array of (x, y) pairs.
        xy = np.column_stack([x.flat, y.flat])

        mu = np.array([0.0, 0.0])

        sigma = np.array([sigmaVal, sigmaVal])
        covariance = np.diag(sigma**2)

        z = multivariate_normal.pdf(xy, mean=mu, cov=covariance)

        # Reshape back to a (30, 30) grid.
        z = z.reshape(x.shape)
        return x,y,z

    #used for testing
    def updatePlot(self):
        time.sleep(3)
        self.fig.clear()
        x, y, z = self.getTestXYZ(0.2)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.plot_surface(x,y,z, color='green')
        self.movers0Plane.draw_idle()  
        
    def updatePlots(self, separatedPlanes, mergedPlanes, secondDerivative, peaks, areas):
        self.fig.clear()
        #plot each plot
        #############################################
        #plot 0
        self.ax0 = self.fig.add_subplot(3, 4, 9)
        self.ax0.imshow(separatedPlanes[0])
        self.ax0.set_title("Targets Plane 1")

        #plot 5
        self.ax5 = self.fig.add_subplot(3, 4, 5)
        if(len(separatedPlanes) > 4):
            self.ax5.imshow(separatedPlanes[4])
        self.ax5.set_title("Targets Plane 5")

        #plot 10
        self.ax10 = self.fig.add_subplot(3, 4, 1)
        if(len(separatedPlanes) > 9):
            self.ax10.imshow(separatedPlanes[9])
        self.ax10.set_title("Targets Plane 10")

        #Merged
        #print("X shape: ", self.X.shape, ", Y shape: ", self.Y.shape, " merged planes shape: ", mergedPlanes.shape)
        self.axMerged = self.fig.add_subplot(3, 4, 2, projection='3d')
        self.axMerged.plot_surface(self.X, self.Y, mergedPlanes, 
                        cmap=plt.cm.cool,
                        linewidth=0,
                        antialiased=True)
        self.axMerged.set_title("Merged Planes")

        #2nd Derivative
        self.axDeriv = self.fig.add_subplot(3, 4, 6)
        self.axDeriv.imshow(secondDerivative)
        self.axDeriv.set_title("2nd Derivative")

        #peaks
        self.axPeaks = self.fig.add_subplot(3, 4, 10)
        peaksImg = np.zeros(mergedPlanes.shape)
        if len(peaks) > 0:
            for p in peaks:
                peaksImg[p[0],p[1]] = 255       
        self.axPeaks.set_title("Peaks")
        self.axPeaks.imshow(peaksImg) 

        #area cubes
        self.axCubes = self.fig.add_subplot(3, 4, 3)
        cubeAreaImg = np.zeros(mergedPlanes.shape)
        self.axCubes.set_title("Cubes Area")

        #area NewCotes
        self.axNewCotes = self.fig.add_subplot(3, 4, 7)
        newCotesAreaImg = np.zeros(mergedPlanes.shape)
        self.axNewCotes.set_title("New Cotes Area")

        #area Gaussian Quadrature
        self.axGaussianQuadrature = self.fig.add_subplot(3, 4, 11)
        gaussianQuadAreaImg = np.zeros(mergedPlanes.shape)
        self.axGaussianQuadrature.set_title("Gaussian Quadrature Area")

        #probability of objects- cubic area
        self.axProbCubic = self.fig.add_subplot(3, 4, 4, projection='3d')
        probCubicImg = np.zeros(mergedPlanes.shape)
        self.axProbCubic.set_title("Cube Targets Thresholded")

        #probability of objects- NewCotes area
        self.axProbNewCotes = self.fig.add_subplot(3, 4, 8, projection='3d')
        probNewCotesImg = np.zeros(mergedPlanes.shape)
        self.axProbNewCotes.set_title("New Cotes Targets Thresholded")

        #probability of objects- Gaussian Quadrature
        self.axProbGaussianQuadrature = self.fig.add_subplot(3, 4, 12, projection='3d')
        probGaussianQuadratureImg = np.zeros(mergedPlanes.shape)
        self.axProbGaussianQuadrature.set_title("Gaussian Quadrature Targets Thresholded")

        if areas is not None:
            #loop through areas stored within each of the keys, and draw on appropriate plane
            for peakKey in areas:
                cubicArea = areas[peakKey].cubeSum
                newCotesArea = areas[peakKey].newCotesSum
                gaussianQuadratureArea = areas[peakKey].gaussianQuadratureSum

                x1 = int(max(peakKey[1] - self.size/2, 0))
                x2 = int(min(peakKey[1] + self.size/2, mergedPlanes.shape[1]-1))
                y1 = int(max(peakKey[0] - self.size/2, 0))
                y2 = int(min(peakKey[0] + self.size/2, mergedPlanes.shape[0]-1))

                x2Text = min(x2 + 5, cubeAreaImg.shape[1]-1)
                y2Text = min(y2 + 5, cubeAreaImg.shape[0]-1)
                cv2.putText(cubeAreaImg, self.truncate(cubicArea, 4), (x2Text, y2Text), cv2.FONT_HERSHEY_SIMPLEX, 0.25,(255,255,255))
                cv2.circle(cubeAreaImg, (x2, y2), 3, (200, 200, 200),-1)
                cv2.putText(newCotesAreaImg, self.truncate(newCotesArea, 4), (x2Text, y2Text), cv2.FONT_HERSHEY_SIMPLEX, 0.25,(255,255,255))
                cv2.circle(newCotesAreaImg, (x2, y2), 3, (200, 200, 200),-1)
                cv2.putText(gaussianQuadAreaImg, self.truncate(gaussianQuadratureArea, 4), (x2Text, y2Text), cv2.FONT_HERSHEY_SIMPLEX, 0.25,(255,255,255))                
                cv2.circle(gaussianQuadAreaImg, (x2, y2), 3, (200, 200, 200),-1)

                print("Cubic area: ", cubicArea, ", New Cotes area: ", newCotesArea, ", Gaussian Quadrature area: ", gaussianQuadratureArea, ", threshold: ", self.threshold)

                probCubicImg[y1:y2, x1:x2] = cubicArea
                probNewCotesImg[y1:y2, x1:x2] = newCotesArea
                probGaussianQuadratureImg[y1:y2, x1:x2] = gaussianQuadratureArea

        self.axCubes.imshow(cubeAreaImg)
        self.axNewCotes.imshow(newCotesAreaImg)
        self.axGaussianQuadrature.imshow(gaussianQuadAreaImg)

        thresholdPlane = np.zeros(cubeAreaImg.shape)
        thresholdPlane.fill(self.threshold)
        self.axProbCubic.plot_surface(self.X, self.Y, probCubicImg, 
                cmap=plt.cm.summer,
                linewidth=0,
                antialiased=True)

        self.axProbCubic.plot_surface(self.X, self.Y, thresholdPlane, 
                cmap=plt.cm.autumn,
                linewidth=0,
                antialiased=True)                

        self.axProbNewCotes.plot_surface(self.X, self.Y, probNewCotesImg, 
                cmap=plt.cm.ocean,
                linewidth=0,
                antialiased=True)

        self.axProbNewCotes.plot_surface(self.X, self.Y, thresholdPlane, 
                cmap=plt.cm.autumn,
                linewidth=0,
                antialiased=True)                

        self.axProbGaussianQuadrature.plot_surface(self.X, self.Y, probGaussianQuadratureImg, 
                cmap=plt.cm.inferno,
                linewidth=0,
                antialiased=True)

        self.axProbGaussianQuadrature.plot_surface(self.X, self.Y, thresholdPlane, 
                cmap=plt.cm.autumn,
                linewidth=0,
                antialiased=True)                
        
        ############################################
        #update
        self.canvas.draw_idle()

    def truncate(self, f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])

    def addWidgets(self):
        #plot widgets
        self.fig = plt.figure()

        #interactive widgets
        self.interactiveFrame = tk.Frame(self.tkGui)

        #threshold slider
        '''self.thresholdSlider = tk.Scale(self.interactiveFrame, from_=0, to=100, orient=tk.HORIZONTAL, label="Target threshold")
        self.thresholdSlider.pack()
        self.thresholdSlider.bind("ThresholdSlider", self.handleThresholdUpdate)'''

        #resolution slider
        self.resolutionSlider = tk.Scale(self.interactiveFrame, from_=8, to=32, tickinterval=8, orient=tk.HORIZONTAL, label="Resolution (N)")
        self.resolutionSlider.set(self.resolution)
        self.resolutionSlider.pack()
        self.resolutionSlider.bind("ResolutionSlider", self.handleResolutionUpdate)

        #objects size
        '''self.objectSizeSlider = tk.Scale(self.interactiveFrame, from_=1, to=100, orient=tk.HORIZONTAL, label="Object size")
        self.objectSizeSlider.set(5)
        self.objectSizeSlider.pack()
        self.objectSizeSlider.bind("ObjectSizeSlider", self.handleSizeUpdate)'''

        #run rate
        self.runRateSlider = tk.Scale(self.interactiveFrame, from_=0.05, to=2, orient=tk.HORIZONTAL, label="Run rate")
        self.runRateSlider.set(self.runRate)
        self.runRateSlider.pack()
        self.runRateSlider.bind("RunRateSlider", self.handleRunRateUpdate)

        self.interactiveFrame.pack(side=tk.LEFT)


        xTest = np.arange(1,100)
        yTest = xTest
        #3 grids of moving targets
        #0
        self.ax0 = self.fig.add_subplot(3, 4, 1)
        self.ax0.plot(xTest, yTest)
        self.ax1 = self.fig.add_subplot(3, 4, 2)
        self.ax1.plot(xTest, yTest)
        self.ax2 = self.fig.add_subplot(3, 4, 3)
        self.ax2.plot(xTest, yTest)
        self.ax3 = self.fig.add_subplot(3, 4, 4)
        self.ax3.plot(xTest, yTest)
        self.ax4 = self.fig.add_subplot(3, 4, 5)
        self.ax4.plot(xTest, yTest)
        self.ax5 = self.fig.add_subplot(3, 4, 6)
        self.ax5.plot(xTest, yTest)
        self.ax6 = self.fig.add_subplot(3, 4, 7)
        self.ax6.plot(xTest, yTest)
        self.ax7 = self.fig.add_subplot(3, 4, 8)
        self.ax7.plot(xTest, yTest)
        self.ax8 = self.fig.add_subplot(3, 4, 9)
        self.ax8.plot(xTest, yTest)
        self.ax9 = self.fig.add_subplot(3, 4, 10)
        self.ax9.plot(xTest, yTest)
        self.ax10 = self.fig.add_subplot(3, 4, 11)
        self.ax10.plot(xTest, yTest)
        self.ax11 = self.fig.add_subplot(3, 4, 12)
        self.ax11.plot(xTest, yTest)

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.tkGui)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tkGui, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def handleThresholdUpdate(self, event):
        self.threshold = self.thresholdSlider.get()
        self.pm.updateThreshold(self.threshold)

    def handleResolutionUpdate(self, event):
        self.resolution = self.resolutionSlider.get()
        self.pm.updateResolution(self.resolution)

    def handleSizeUpdate(self, event):
        self.size = self.objectSizeSlider.get()

    def handleRunRateUpdate(self, event):
        self.runRate = self.runRateSlider.get()
