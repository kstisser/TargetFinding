import tkinter as tk 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import time
import matplotlib.pyplot as plt
import planeManager
import threading

class GuiManager:
    def __init__(self, movers, domainSize, runRate):
        self.runRate = runRate
        self.resolution = domainSize[0]
        self.threshold = 1
        self.size = 5
        self.tkGui = tk.Tk()
        self.wholeFrame = tk.Frame(master = self.tkGui)
        self.addWidgets()
        self.pm = planeManager.PlaneManager(movers, domainSize)
        
    def runGUI(self):
        self.tkGui.mainloop()

    def start(self):
        self.pm.plotMoversWithNewTimestep()
        separatedPlanes, mergedPlanes, secondDerivative, peaks, areas = self.pm.mergePlanes(self.resolution, self.size, self.threshold)
        self.updatePlots(separatedPlanes, mergedPlanes, secondDerivative, peaks, areas)
        #guiThread = threading.Thread(target=self.runGUI)
        #guiThread.start()
        #Make movement happen 1/2 second at a time, or by the variable speed entered
        '''while True:
            startTime = time.time()
            self.pm.plotMoversWithNewTimestep()
            self.updatePlots(self.pm.mergePlanes(self.resolution, self.size, self.threshold))
            #sleep amount of time still needed after processing to get to the run rate
            waitTime = self.runTime - (time.time() - startTime)
            if waitTime > 0:
                time.sleep(self.runRate) 
        '''      

    def updatePlots(self, separatedPlanes, mergedPlanes, secondDerivative, peaks, areas):
        #TODO
        pass

    def addWidgets(self):
        #5 grids of moving targets
        #0
        '''self.wholeFrame.grid(row=1, column=1, padx=5, pady=5)
        self.movers0Fig = plt.figure(1)
        self.movers0Plane = FigureCanvasTkAgg(self.movers0Fig, master = self.wholeFrame)
        self.movers0Plane.draw()
        #self.movers0Plane.pack()

        #2
        self.wholeFrame.grid(row=1, column=2, padx=5, pady=5)
        self.movers2Fig = plt.figure(2)
        self.movers2Plane = FigureCanvasTkAgg(self.movers2Fig, master = self.wholeFrame)
        self.movers2Plane.draw()
        #self.movers2Plane.pack()  

        #4
        self.wholeFrame.grid(row=1, column=3, padx=5, pady=5)
        self.movers4Fig = plt.figure(3)
        self.movers4Plane = FigureCanvasTkAgg(self.movers4Fig, master = self.wholeFrame)
        self.movers4Plane.draw()
        #self.movers4Plane.pack() 

        #6
        self.wholeFrame.grid(row=1, column=4, padx=5, pady=5)
        self.movers6Fig = plt.figure(4)
        self.movers6Plane = FigureCanvasTkAgg(self.movers6Fig, master = self.wholeFrame)
        self.movers6Plane.draw()
        #self.movers6Plane.pack()     

        #8
        self.wholeFrame.grid(row=1, column=5, padx=5, pady=5)
        self.movers8Fig = plt.figure(5)
        self.movers8Plane = FigureCanvasTkAgg(self.movers8Fig, master = self.wholeFrame)
        self.movers8Plane.draw()
        #self.movers8Plane.pack()        

        #merged plane
        self.wholeFrame.grid(row=2, column=3, padx=5, pady=5)
        self.mergedPlaneFig = plt.figure(6)
        self.mergedPlane = FigureCanvasTkAgg(self.mergedPlaneFig, master = self.wholeFrame)
        self.mergedPlane.draw()
        #self.mergedPlane.pack()

        #2nd derivative plane
        self.wholeFrame.grid(row=3, column=3, padx=5, pady=5)
        self.secondDerivativeFig = plt.figure(7)
        self.secondDerivative = FigureCanvasTkAgg(self.secondDerivativeFig, master = self.wholeFrame)
        self.secondDerivative.draw()
        #self.secondDerivative.pack()

        #peaks
        self.wholeFrame.grid(row=4, column=3, padx=5, pady=5)
        self.peaksFig = plt.figure(8)
        self.peaks = FigureCanvasTkAgg(self.peaksFig, master = self.wholeFrame)
        self.peaks.draw()
        #self.peaks.pack()

        #cubic area
        self.wholeFrame.grid(row=2, column=4, padx=5, pady=5)
        self.cubicAreaFig = plt.figure(9)
        self.cubicArea = FigureCanvasTkAgg(self.cubicAreaFig, master = self.wholeFrame)
        self.cubicArea.draw()
        #self.cubicArea.pack()

        #cubic probability
        self.wholeFrame.grid(row=2, column=5, padx=5, pady=5)
        self.cubicProbabilityFig = plt.figure(10)
        self.cubicProbability = FigureCanvasTkAgg(self.cubicProbabilityFig, master = self.wholeFrame)
        self.cubicProbability.draw()
        #self.cubicProbability.pack()

        #gaussian quadrature area
        self.wholeFrame.grid(row=3, column=4, padx=5, pady=5)
        self.gaussianQuadratureAreaFig = plt.figure(11)
        self.gaussianQuadratureArea = FigureCanvasTkAgg(self.gaussianQuadratureAreaFig, master = self.wholeFrame)
        self.gaussianQuadratureArea.draw()
        #self.gaussianQuadratureArea.pack()

        #gaussian quadrature probability
        self.wholeFrame.grid(row=3, column=5, padx=5, pady=5)
        self.gaussianQuadratureProbabilityFig = plt.figure(12)
        self.gaussianQuadratureProbability = FigureCanvasTkAgg(self.gaussianQuadratureProbabilityFig, master = self.wholeFrame)
        self.gaussianQuadratureProbability.draw()
        #self.gaussianQuadratureProbability.pack()

        #newcodes area
        self.wholeFrame.grid(row=4, column=4, padx=5, pady=5)
        self.newCodesAreaFig = plt.figure(13)
        self.newCodesArea = FigureCanvasTkAgg(self.newCodesAreaFig, master = self.wholeFrame)
        self.newCodesArea.draw()
        #self.newCodesArea.pack()

        #newcodes probability
        self.wholeFrame.grid(row=4, column=5, padx=5, pady=5)
        self.newCodesProbabilityFig = plt.figure(14)
        self.newCodesProbability = FigureCanvasTkAgg(self.newCodesProbabilityFig, master = self.wholeFrame)
        self.newCodesProbability.draw()
        #self.newCodesProbability.pack()

        #threshold slider
        self.wholeFrame.grid(row=2, column=1, padx=5, pady=5)
        self.thresholdSlider = tk.Scale(self.wholeFrame, from_=0, to=100)
        self.thresholdSlider.pack()
        self.thresholdSlider.bind("ThresholdSlider", self.handleThresholdUpdate)

        #resolution slider
        self.wholeFrame.grid(row=3, column=1, padx=5, pady=5)
        self.resolutionSlider = tk.Scale(self.wholeFrame, from_=10, to=1000)
        self.resolutionSlider.set(self.resolution)
        self.resolutionSlider.pack()
        self.resolutionSlider.bind("ResolutionSlider", self.handleResolutionUpdate)

        #objects size
        self.wholeFrame.grid(row=4, column=1, padx=5, pady=5)
        self.objectSizeSlider = tk.Scale(self.wholeFrame, from_=1, to=100)
        self.objectSizeSlider.pack()
        self.objectSizeSlider.bind("ObjectSizeSlider", self.handleSizeUpdate)

        #run rate
        self.wholeFrame.grid(row=2, column=2, padx=5, pady=5)
        self.runRateSlider = tk.Scale(self.wholeFrame, from_=0.05, to=2)
        self.runRateSlider.set(self.runRate)
        self.runRateSlider.pack()
        self.runRateSlider.bind("RunRateSlider", self.handleRunRateUpdate)'''

    def handleThresholdUpdate(self, event):
        self.threshold = self.thresholdSlider.get()

    def handleResolutionUpdate(self, event):
        self.resolution = self.resolutionSlider.get()

    def handleSizeUpdate(self, event):
        self.size = self.objectSizeSlider.get()

    def handleRunRateUpdate(self, event):
        self.runRate = self.runRateSlider.get()