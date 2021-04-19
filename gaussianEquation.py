import math

def getGaussianDistributionValue(mean, x, y, stddev):
    val = 1.0/(2.0 * math.pi) * math.exp(-((x - mean[1])**2 + (y - mean[0])**2)/(2 * stddev * stddev))
    #print("Computed: ", val, " x: ", x, ", y: ", y, ", stddev: ", stddev, " mean: ", mean)
    return val