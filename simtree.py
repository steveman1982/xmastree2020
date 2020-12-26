import re
import matplotlib.pyplot as plt


class Simtree:
    def __init__(self, coords):
        self.coords = coords
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

    def update(self, grb_colors):
        plt.show()
        # grb_colors should always match the number of lights, length of coords

        for i in range(0, len(grb_colors)):
            coord = self.coords[i]
            grb = grb_colors[i]
            # translate to rgb
            self.ax.scatter(coord[0], coord[1], coord[2], marker='^',
                            facecolor=[grb[1] / 255.0, grb[0] / 255.0, grb[2] / 255.0])

        plt.draw()
        # wait a bit so we can enjoy the result
        plt.pause(0.1)
