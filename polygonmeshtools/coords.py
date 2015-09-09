import math
import numpy as np


class CartesianCoords(object):
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.r = math.sqrt(x**2 + y**2 + z**2)  # radial
        self.a = np.arctan2(x, y)    # azimuth
        self.h = z                   # cylindrical height


class PolarCoords(object):
    def __init__(self, radial, azimuth, height=0):
        self.r = radial
        self.a = azimuth
        self.h = height
        self.x = radial*np.cos(azimuth)
        self.y = radial*np.sin(azimuth)
        self.z = height
