import planeManager
import scenarioReader
import sys
import os.path
import time
import gui

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error! Need to pass in a json path that describes the scenario you want to run!")
    else:
        #establish run rate and whether we're running with noise
        runRate = 0.1
        noise = False
        if len(sys.argv) > 2:
            runRate = float(sys.argv[2])
            if len(sys.argv) > 3:
                noise = True

        #read in scenario file and generate movers
        fileName = sys.argv[1]
        print(fileName)
        if(os.path.exists(fileName) and os.path.isfile(fileName)):
            sr = scenarioReader.ScenarioReader(fileName)
            movers = sr.getMoversForPlane()  
            domainSize = sr.domainSize          

            guiManager = gui.GuiManager(movers, domainSize, runRate, noise)
            guiManager.start()
        else:
            print("Error! Your entry does not seem to be a real file, try again! ", fileName)