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
- translation, shifts the centre of the polygon to the given Cartesian co-ordinate tuple
- plot, a boolean to dictate whether or not the plot should be shown.

Some example plots are shown below:

    in_poly(x=10,y=10,n=3,r=20,plot=True)

![inpoly1.png](https://bitbucket.org/repo/n5rKzp/images/3387981976-inpoly1.png)

    in_poly(x=10,y=10,n=5,r=20,plot=True)

![inpoly2.png](https://bitbucket.org/repo/n5rKzp/images/4244237353-inpoly2.png)