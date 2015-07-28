#Polygon Mesh Tools

A package for creating polygon-shaped geometries from cuboidal finite difference elements.

Also contains some visualisation functions which use matplotlib.

---

##in_poly

Returns a boolean stating whether or not a given Cartesian coordinate lies within the boundaries of a regular polygon.

Inputs are:

- x- and y- coordinates for the point in question
- n, the number of sides the polygon has
- r, the [circumradius](https://en.wikipedia.org/wiki/Regular_polygon#Circumradius)
- rotation, in radians (anti-clockwise)
- translate, shifts the centre of the polygon to the given Cartesian co-ordinate tuple
- plot, a boolean to dictate whether or not the plot should be shown.

Some example plots are shown below:

    in_poly(x = 10, y = 10, n = 3, r = 20, plot = True)

False  
![inpoly1.png](https://bitbucket.org/repo/n5rKzp/images/3387981976-inpoly1.png)

    in_poly(x = 10, y = 10, n = 5, r = 20, plot = True)

True  
![inpoly2.png](https://bitbucket.org/repo/n5rKzp/images/4244237353-inpoly2.png)

---

##plot_poly_fidi_mesh

Produces a 2D visualisation of the finite difference mesh comprising of rectangular elements.

Inputs are:

- diameter, of the circumscribing circle
- n, the number of sides the polygon has
- x_spacing, the width of the rectangular elements
- y_spacing, the height of the rectangular elements
- rotation, in radians (anti-clockwise)
- translate, shifts the centre of the polygon to the given Cartesian co-ordinate tuple
- centre_mesh, determines whether or not the centre of the mesh occurs at the corner of multiple elements or the centre of an element
- show_axes, boolean, performing as expected
- show_title, boolean, performing as expected

Some example plots are shown below:

    plot_poly_fidi_mesh(diameter=40, n = 3, x_spacing = 1, y_spacing = 1, rotation = np.pi/2)

![plotpolyfidimesh1.png](https://bitbucket.org/repo/n5rKzp/images/1004336124-plotpolyfidimesh1.png)

    plot_poly_fidi_mesh(diameter = 60, n = 9, x_spacing = 2, y_spacing = 1, centre_mesh = False)

![plotpolyfidimesh2.png](https://bitbucket.org/repo/n5rKzp/images/266576477-plotpolyfidimesh2.png)

#Prerequisites

Requires the following imports:

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches