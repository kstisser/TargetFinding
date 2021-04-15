import json
import mover
import defs

class ScenarioReader:
    def __init__(self, jsonFile):
        with open(jsonFile) as f:
            self.scenario = json.load(f)
        self.domainSize = self.scenario["domainSize"] if "domainSize" in self.scenario else [100,100]
        self.movers = []

    def getMoversForPlane(self):
        for mov in self.scenario['objects']:
            movementType = (defs.getMovementTypeFromString(mov["movementType"])) if "movementType" in mov else defs.MovementType.STATIC
            startPoint = mov["startingPixel"]
            paceLength = mov["paceLength"] if "paceLength" in mov else 0
            radius = mov["radius"] if "radius" in mov else 10
            movementDirection = (defs.getMovementDirectionFromString(mov["movementDirection"])) if "movementDirection" in mov else defs.MovementDirection.VERTICALUP
            m = mover.Mover(movementType, startPoint, self.domainSize, pacelength=paceLength, radius=radius, movementDirection=movementDirection)
            self.movers.append(m)
        return self.movers
