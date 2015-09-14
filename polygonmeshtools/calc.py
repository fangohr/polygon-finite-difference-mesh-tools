import math

import numpy as np
import matplotlib.pyplot as plt

from .coords import CartesianCoords, CylindricalCoords


def in_poly(x, y, n, r=1, rotation=0, translate=(0, 0), plot=False):
    """
    Determines whether or not the point (x,y) lies within a regular
    n-sided polygon whose circumscribing circle has radius r.

    By default, a point will lie at the Cartesian location (r, 0) but
    can be rotated by specifying a rotation (in radians).

    Polygon centred at (0,0) by default, but this can be changed by
    giving translate in the form (x,y).
    """

    def poly_coords(r, n, rotation=rotation, translate=translate):
        coords = np.empty((n, 2))
        for i in range(n):
            coord = CylindricalCoords(r, (2.*np.pi*i/n)+rotation)
            coords[i][0] = coord.x + translate[0]
            coords[i][1] = coord.y + translate[1]
        return coords

    def angle_test(x, y, r=r, n=n, rotation=rotation):
        """
        Taking all pairs of adjacent vertices of the polygon, the sum
        of the angles made by each pair of points about the point in
        question should be approximately 2*pi.

        Method demonstrated at:
        -----------------------
        http://demonstrations.wolfram.com/
        IsAPointInsideOrOutsideARegularPolygon/
        """
        np.seterr(all='raise')

        coords = poly_coords(r, n, rotation, translate)
        coordA = [x, y]
        angle = 0
        for i in range(len(coords)):
            try:
                coordB = coords[i]
                coordC = coords[i+1]
            except IndexError:
                coordC = coords[0]

            # Finding side lengths
            lengthAB = math.sqrt((
                coordA[0]-coordB[0])**2 + (coordA[1]-coordB[1])**2
            )

            lengthAC = math.sqrt((
                coordA[0]-coordC[0])**2 + (coordA[1]-coordC[1])**2
            )

            lengthBC = math.sqrt((
                coordB[0]-coordC[0])**2 + (coordB[1]-coordC[1])**2
            )

            if (np.isclose(lengthAB, 0)) or (np.isclose(lengthAC, 0)):
                angle = 2*np.pi
                break

            try:
                # Cosine rule
                # NB: (side a is opposite side of triangle to point A)
                a, b, c = lengthBC, lengthAC, lengthAB
                angle_increment = (c**2 + b**2 - a**2) / (2*c*b)
                angle += np.arccos(angle_increment)

            except (FloatingPointError, ZeroDivisionError):
                # Inside, on the line
                if np.isclose(angle_increment, -1):
                    # Automatic pass
                    return 2*np.pi

                # Outside, 'on the line'
                if np.isclose(angle_increment, 1):
                    # Automatic fail
                    return 0
        return angle

    if plot:
        coords = poly_coords(r, n, rotation, translate)
        fig = plt.figure()
        ax0 = fig.add_subplot(111)
        ax0.set_xlim(-r+translate[0], r+translate[0])
        ax0.set_ylim(-r+translate[1], r+translate[1])
        ax0.set_aspect('equal')

        ax0.plot(
            np.transpose(
                np.concatenate(
                    (coords, coords), axis=0)[:n+1], (1, 0)
            )[0],
            np.transpose(
                np.concatenate(
                    (coords, coords), axis=0)[:n+1], (1, 0)
            )[1]
        )

        if np.isclose(2*np.pi, angle_test(x, y), atol=1e-4):
            dotcolour = 'g'
        else:
            dotcolour = 'r'

        ax0.scatter(
            [x, 0+translate[0]], [y, 0+translate[1]],
            c=[dotcolour, 'b'], s=[20, 10], lw=0
        )

    return np.isclose(2*np.pi, angle_test(x, y), atol=1e-4)


def find_circumradius(n, side=0, apothem=0):
    """
    Returns the radius of the circumscribing circle for a regular
    polygon given the side length or the apothem (distance from
    circumcentre to centre of a face).
    """
    if side == 0 and apothem != 0:
        circumradius = apothem/(np.cos(np.pi/n))
    elif side != 0 and apothem == 0:
        circumradius = side/(2*np.sin(np.pi/n))
    elif side == 0 and apothem == 0:
        raise ValueError(
            "Please specify a side length or an apothem."
        )
    else:
        raise ValueError(
            "Please specify side length OR apothem, not both!"
        )
    return circumradius
