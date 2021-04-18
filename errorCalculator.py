import numpy as np
import gausianEquation

class ErrorCalculator:
    def __init__(self, separatedPlanes, weights, peaks):
        self.separatedPlanes = separatedPlanes
        self.weights = weights
        self.peaks = peaks