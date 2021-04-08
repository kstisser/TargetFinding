from enum import Enum

class ObjectType(Enum):
    PERSON = 1
    CAR = 1

def getObjectTypeFromString(str):
    if str == "Person":
        return ObjectType.PERSON
    elif str == "Car":
        return ObjectType.CAR
    else:
        print("Error! Read in unrecognizable object type!")

class MovementType(Enum):
    STATIC = 1
    LINEAR = 2
    PACING = 3
    CIRCLE = 4

def getMovementTypeFromString(str):
    if str == "Static":
        return MovementType.STATIC
    elif str == "Linear":
        return MovementType.LINEAR
    elif str == "Pacing":
        return MovementType.PACING
    elif str == "Circle":
        return MovementType.CIRCLE
    else:
        print("Error! Read in unrecognizable movement type!")

class MovementDirection(Enum):
    VERTICALUP = 1
    VERTICALDOWN = 2
    HORIZONTALRIGHT = 3
    HORIZONTALLEFT = 4
    DIAGUPRIGHT = 5
    DIAGUPLEFT = 6
    DIAGDOWNRIGHT = 7
    DIAGDOWNLEFT = 8

def getMovementDirectionFromString(str):
    if str == "VerticalUp":
        return MovementDirection.VERTICALUP
    elif str == "VerticalDown":
        return MovementDirection.VERTICALDOWN
    elif str == "HorizontalRight":
        return MovementDirection.HORIZONTALRIGHT
    elif str == "HorizontalLeft":
        return MovementDirection.HORIZONTALLEFT
    elif str == "DiagUpRight":
        return MovementDirection.DIAGUPRIGHT
    elif str == "DiagUpLeft":
        return MovementDirection.DIAGUPLEFT
    elif str == "DiagDownRight":
        return MovementDirection.DIAGDOWNRIGHT
    elif str == "DiagDownLeft":
        return MovementDirection.DIAGDOWNLEFT
    else:
        print("Error! Read in unrecognizable movement direction!")

def getPersonFootprint():
    return [1,1]

def getCarFootprint():
    return [3,3]