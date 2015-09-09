import math

import numpy as np

from .coords import CartesianCoords, PolarCoords

def in_poly(x, y, n, r=1, rotation=0, translate=(0,0), plot=False):
    """
    Determines whether or not the point (x,y) lies within a regular n-sided
    polygon whose circumscribing circle has radius r.
    
    By default, a point will lie at the Cartesian location (r, 0) but can
    be rotated by specifying a rotation (in radians).
    
    Polygon centred at (0,0) by default, but this can be changed by giving
    translate as an (x,y) tuple.
    """
    
    def poly_coords(r, n, rotation=rotation, translate=translate):
        coords = np.empty((n,2))
        for i in range(n):
            coord = PolarCoords(r, (2.*np.pi*i/n)+rotation)
            coords[i][0], coords[i][1] = coord.x+translate[0], coord.y+translate[1]
        return coords
    
    def angle_test(x, y, r=r, n=n, rotation=rotation):
        """
        Taking all pairs of adjacent vertices of the polygon, the sum of
        the angles made by each pair of points about the point in question
        should be approximately 2*pi.
        """
        np.seterr(all='raise')
        
        coords = poly_coords(r,n,rotation,translate)
        coord1 = [x,y]
        angle = 0
        for i in range(len(coords)):
            try:
                coord2 = coords[i]
                coord3 = coords[i+1]
            except IndexError:
                coord3 = coords[0]
                
            #cosine rule to determine angle
            length12 = math.sqrt((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)
            length13 = math.sqrt((coord1[0]-coord3[0])**2 + (coord1[1]-coord3[1])**2)
            length23 = math.sqrt((coord2[0]-coord3[0])**2 + (coord2[1]-coord3[1])**2)
            if (np.isclose(length12,0)) or (np.isclose(length13,0)):
                angle = 2*np.pi
                break

            try:
                angle_increment = (length12**2 + length13**2 - length23**2)/(2*length12*length13)
                angle += np.arccos(angle_increment)
            except (FloatingPointError,ZeroDivisionError):
                if np.isclose(angle_increment,-1): #inside, on the line
                    return 2*np.pi #automatic pass
                if np.isclose(angle_increment,1): #outside, 'on the line'
                    return 0 #automatic fail
        return angle
    
    if plot == True:
        coords = poly_coords(r,n,rotation,translate)
        fig = plt.figure()
        ax0 = fig.add_subplot(111)
        ax0.set_xlim(-r+translate[0],r+translate[0])
        ax0.set_ylim(-r+translate[1],r+translate[1])
        ax0.set_aspect('equal')
        ax0.plot(np.transpose(np.concatenate((coords, coords),axis=0)[:n+1],
                              (1,0))[0],np.transpose(np.concatenate((coords, coords),axis=0)[:n+1], (1,0))[1])
        if np.isclose(2*np.pi, angle_test(x,y), atol=1e-4):
            dotcolour = 'g'
        else:
            dotcolour = 'r'
        ax0.scatter([x,0+translate[0]],[y,0+translate[1]], c=[dotcolour,'b'], s=[20,10],lw = 0)
    return np.isclose(2*np.pi, angle_test(x,y), atol=1e-4)






def find_circumradius(n, side = 0, apothem = 0):
    """
    Returns the radius of the circumscribing circle for a regular polygon
    given the side length or the apothem (distance from circumcentre to 
    centre of a face).
    """
    if side == 0 and apothem != 0:
        circumradius = apothem/(np.cos(np.pi/n))
    elif side != 0 and apothem == 0:
        circumradius = side/(2*np.sin(np.pi/n))
    elif side == 0 and apothem == 0:
        raise ValueError("Please specify a side length or an apothem.")
    else:
        raise ValueError("Please specify side length OR apothem, not both!")
    return circumradius



