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
        fileName = sys.argv[1]
        print(fileName)
        if(os.path.exists(fileName) and os.path.isfile(fileName)):
            sr = scenarioReader.ScenarioReader(fileName)
            movers = sr.getMoversForPlane()  
            domainSize = sr.domainSize          

            runRate = 0.5
            if len(sys.argv) > 2:
                runRate = sys.argv[2]

            guiManager = gui.GuiManager(movers, domainSize, runRate)
            guiManager.start()
        else:
            print("Error! Your entry does not seem to be a real file, try again! ", fileName)