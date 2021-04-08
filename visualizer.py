import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    def __init__(self):
        print("Opening visualizer")

    def plotPlane(self, plane):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(plane, 
                        cmap=cm.coolwarm,
                        linewidth=0,
                        antialiased=True)
        ax.set_xlabel('x space')
        ax.set_ylabel('y space')
        ax.set_zlabel('Gaussians representing target sensor returns')
        plt.show()