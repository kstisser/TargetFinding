import planeManager
import scenarioReader
import sys
import os.path
import time

if __name__ == "__main__":
    if len(sys.argv < 2):
        print("Error! Need to pass in a json path that describes the scenario you want to run!")
    else:
        fileName = sys.argv[1]
        if(os.path.exists(fileName) and os.path.isFile(fileName)):
            sr = scenarioReader.ScenarioReader(fileName)
            movers = sr.getMoversForPlane()  
            domainSize = sr.getDomainSize()          
            pm = planeManager.PlaneManager(movers, domainSize)
            
            runRate = 0.5
            if len(sys.argv) > 2:
                runRate = sys.argv[2]
            #Make movement happen 1/2 second at a time, or by the variable speed entered
            while True:
                pm.plotMoversWithNewTimestep()
                pm.mergePlanesAndDisplay()
                time.sleep(runRate)
        else:
            print("Error! Your entry does not seem to be a real file, try again! ", fileName)