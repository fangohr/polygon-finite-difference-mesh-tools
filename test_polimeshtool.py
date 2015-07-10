import numpy as np
import polymeshtool as p

def test_coordinate_transformation_many():
    for x in np.linspace(0, 10, 0.5):
        for y in np.linspace(0, 10, 0.2):
            c = p.CartesianCoords(x, y)
            d = p.PolarCoords(c.r, c.a)
            assert abs(d.x - x) < 1e-15
            assert abs(d.y - y) < 1e-15


