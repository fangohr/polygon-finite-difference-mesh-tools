import math

import numpy as np
import pytest

from .calc import in_poly, find_circumradius


def test_in_poly():
    for n in range(3, 11):
        # Inside boundary
        assert in_poly(x=0, y=0, n=n, r=10) is True
        # Outside boundary
        assert in_poly(x=11, y=0, n=n, r=10) is False
        # At vertex
        assert in_poly(x=10, y=0, n=n, r=10) is True
    # Attempted exception triggering. Testing all corners of a square.
    for x, y in zip([20, 0, -20, 0], [0, 20, 0, -20]):
        assert in_poly(x=x, y=y, n=4, r=20) is True

    # Test rotation for square, on edge
    assert in_poly(x=25/math.sqrt(2), y=5, n=4, r=25, rotation=np.pi/4) is True
    # Upper vertices
    assert in_poly(
        x=-25/math.sqrt(2), y=25/math.sqrt(2), n=4, r=25, rotation=np.pi/4
    ) is True

    assert in_poly(
        x=25/math.sqrt(2), y=25/math.sqrt(2), n=4, r=25, rotation=np.pi/4
    ) is True

    # Testing lower vertices
    assert in_poly(
        x=-25/math.sqrt(2), y=-25/math.sqrt(2), n=4, r=25, rotation=np.pi/4
    ) is True

    assert in_poly(
        x=25/math.sqrt(2), y=-25/math.sqrt(2), n=4, r=25, rotation=np.pi/4
    ) is True

    # Positive translation
    assert in_poly(
        x=25/math.sqrt(2)+5, y=10, n=4, r=25, translate=(5, 5)
    ) is True

    # Negative translation
    assert in_poly(
        x=25/math.sqrt(2)-5, y=0, n=4, r=25, translate=(-5, -5)
    ) is True

    # Need to try and trigger FloatingPointError or ZeroDivisionError


def test_find_circumradius():
    # Square of given side length
    s = find_circumradius(n=4, side=10)
    assert abs(s-0.5*10*math.sqrt(2)) < 1e-15
    # Square of given apothem
    a = find_circumradius(n=4, apothem=5)
    assert abs(a-0.5*10*math.sqrt(2)) < 1e-15
    # Circle approximation (apothem = radius for a circle)
    r = find_circumradius(n=10000, apothem=25)
    assert abs(25-r) < 1e-5


def test_find_circumradius_errors():
    # Neither side nor apothem given
    with pytest.raises(ValueError):
        find_circumradius(n=5, apothem=0, side=0)
    # Both side and apothem given
    with pytest.raises(ValueError):
        find_circumradius(n=3, apothem=5, side=2)


def test_in_poly_plot():
    # Triggering if plot clause
    assert in_poly(x=0, y=0, n=4, r=10, plot=True) is True
    # Testing change of dot colour
    assert in_poly(x=15, y=15, n=4, r=10, plot=True) is False
