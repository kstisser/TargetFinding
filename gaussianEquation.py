import math

def getGaussianDistributionValue(mean, x, y, stddev):
    return 1.0/(2.0 * math.pi) * math.exp(-((x - mean[1])**2 + (y - mean[0])**2)/(2 * stddev * stddev))