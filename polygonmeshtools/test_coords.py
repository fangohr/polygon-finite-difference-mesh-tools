import numpy as np

from .coords import CylindricalCoords, CartesianCoords


def test_CartesianCoords_initialisation():
    c = CartesianCoords(0, 0, 0)
    assert c.x == 0
    assert c.y == 0
    assert c.z == 0
    assert c.r == 0
    assert c.a == 0
    assert c.h == 0


def test_CylindricalCoords_initialisation():
    d = CylindricalCoords(0, 0, 0)
    assert d.x == 0
    assert d.y == 0
    assert d.z == 0
    assert d.r == 0
    assert d.a == 0
    assert d.h == 0


def test_coordinate_transformation_many():
    for x in np.linspace(-10, 10, 21):
        for y in np.linspace(-10, 10, 41):
            for z in np.linspace(-10, 10, 31):
                c = CartesianCoords(x, y, z)
                assert (c.x, c.y, c.z) == (x, y, z)
                d = CylindricalCoords(c.r, c.a, c.h)
                assert (d.r, d.a, d.h) == (c.r, c.a, c.h)

                # Offending statements are x and y

                assert np.isclose(d.x, x) is True
                assert np.isclose(d.y, y) is True
                assert np.isclose(d.z, z) is True
