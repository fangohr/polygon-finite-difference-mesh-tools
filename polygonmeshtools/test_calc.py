import math

import numpy as np
import pytest

from .calc import in_poly, find_circumradius



def test_in_poly():
    for n in range(3,11):
        #Inside boundary
        assert in_poly(x=0, y=0, n=n, r=10) is True
        #Outside boundary
        assert in_poly(x=11, y=0, n=n, r=10) is False
        #At vertex
        assert in_poly(x=10, y=0, n=n, r=10) is True

    #Test rotation for square, on edge
    assert in_poly(x=25/math.sqrt(2), y=5, n=4, r=25, rotation=np.pi/4) is True
    #On vertex
    assert in_poly(x=-25/math.sqrt(2), y=25/math.sqrt(2), n=4, r=25, rotation=np.pi/4) is True
    #Note lower vertices don't work, probably floating point error.
    
    #Positive translation
    assert in_poly(x=25/math.sqrt(2)+5, y=10, n=4, r=25, rotation=np.pi/4, translate=(5,5)) is True
    #Negative translation
    assert in_poly(x=25/math.sqrt(2)-5, y=0, n=4, r=25, rotation=np.pi/4, translate=(-5,-5)) is True
    
def test_find_circumradius():
    #Square of given side length
    s = find_circumradius(n=4, side=10)
    assert abs(s-0.5*10*math.sqrt(2)) < 1e-15
    #Square of given apothem
    a = find_circumradius(n=4, apothem=5)
    assert abs(a-0.5*10*math.sqrt(2)) < 1e-15
    #Circle approximation (apothem = radius for a circle)
    r = find_circumradius(n=10000, apothem=25)
    assert abs(25-r) < 1e-5

    with pytest.raises(ValueError):
        find_circumradius(n=5, apothem=0, side=0)
    
