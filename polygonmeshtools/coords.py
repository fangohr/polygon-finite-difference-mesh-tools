import math
import numpy as np


class CartesianCoords(object):
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

        #radial
        self.r = math.sqrt(x**2 + y**2)

        #azimuth
        self.a = np.arctan2(y, x)

        #cylindrical height
        self.h = z


class CylindricalCoords(object):
    def __init__(self, radial, azimuth, height=0):
        self.r = radial
        self.a = azimuth
        self.h = height
        self.x = radial*np.cos(azimuth)
        self.y = radial*np.sin(azimuth)
        self.z = height
