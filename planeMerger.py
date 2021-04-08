import visualizer

class PlaneMerger:
    def __init__(self, planes, weights):
        self.referencePlanes = np.array(planes)
        self.weights = weights
        self.viz = visualizer.Visualizer()

        #meshgrid used for gaussian calculations
        xlength, ylength, dimensions = self.referencePlanes.shape
        X = np.arrange(0,xlength,1)
        Y = np.arrange(0,ylength,1)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**2)
        Z = ((1./np.sqrt(2. * np.pi)) * np.exp(-0.5 * R**2))
        print(Z)

        #Fixed gaussian distribution parameters
        self.variance = 0.25

    def merge(self):
        self.gaussianMixturePlanes = np.zeros(planes.shape)
        targetPoints = np.nonzero(self.referencePlanes)
        for point in targetPoints:
            addGaussianDistributionForPoint(point)
        mergePlanesByWeights()
        self.viz.plotPlane(self.mergedPlane)

    #reference for gaussian distribution equation: 
    # https://towardsdatascience.com/a-python-tutorial-on-generating-and-plotting-a-3d-guassian-distribution-8c6ec6c41d03
    def addGaussianDistributionForPoint(self, point):
        #Note- the mean is at the point given, and the variance is fixed above
        #TODO
        pass

    #This function both mulitplies the planes by their weights, 
    # and sums the Z direction to collapse all into one 2D array of heights
    def mergePlanesByWeights(self):
        self.mergedPlanes = np.sum((self.gaussianMixturePlanes * self.weights), axis=2, dtype='float32')