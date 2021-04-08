import numpy as np
import defs

class QuadratureCalculator:
    def __init__(self, mergedPlanes, peaks):
        self.mergedPlanes = mergedPlanes
        self.peaks = peaks

    def getCubicArea(self, objectType):
        if objectType == defs.ObjectType.PERSON:

        elif objectType == defs.ObjectType.CAR:

        else:
            print("Error! Object Type not recognized! ", objectType)
        
    def getTriangulatedArea(self, objectType):
        if objectType == defs.ObjectType.PERSON:

        elif objectType == defs.ObjectType.CAR:

        else:
            print("Error! Object Type not recognized! ", objectType)

    def getQuadratureArea(self, objectType):
        if objectType == defs.ObjectType.PERSON:

        elif objectType == defs.ObjectType.CAR:

        else:
            print("Error! Object Type not recognized! ", objectType)    
