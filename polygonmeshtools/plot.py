import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .coords import CartesianCoords, CylindricalCoords
from .calc import in_poly


def mesher(
    diameter, translate,
    x_spacing=1, y_spacing=1, centre_mesh='auto'
):
    """
    Creates mesh grid for plotting functions to sweep.
    """
    def make_list(diameter, spacing):
        l = sorted(
            range(0, -(diameter/2) - spacing, -spacing) +
            range(0, (diameter/2) + spacing, spacing)[1:]
        )
        return l

    xlist = [x + translate[0] for x in make_list(diameter, x_spacing)]
    ylist = [y + translate[1] for y in make_list(diameter, y_spacing)]

    # Decide if centering will cause asymmetry
    if centre_mesh == 'auto':
        if diameter % (2*x_spacing) == 0 and diameter % (2*y_spacing) == 0:
            centre_mesh = False
        else:
            centre_mesh = True

    if centre_mesh == True:
        xcoords, ycoords = xlist, ylist
    elif centre_mesh == False:
        xcoords = [x - x_spacing/2. for x in xlist]
        ycoords = [y - y_spacing/2. for y in ylist]
    else:
        raise ValueError(
            'Unrecognised value "{}" for centre_mesh! \
            Please choose True, False, or "auto".'.format(centre_mesh)
        )

    return xcoords, ycoords


def titles_and_axes(
    show_title, show_axes, axes, diameter,
    x_spacing, y_spacing, elem_count, translate
):
    """
    Handles axes and titles for plot_poly_fidi_mesh and
    plot_circular_fidi_mesh.
    """
    axes.set_xlim(-diameter/2. + translate[0], diameter/2. + translate[0])
    axes.set_ylim(-diameter/2. + translate[1], diameter/2. + translate[1])

    if show_axes:
        axes.set_xlabel("x (nm)")
        axes.set_ylabel("y (nm)")
    else:
        axes.get_yaxis().set_visible(False)
        axes.get_xaxis().set_visible(False)
        axes.set_frame_on(False)

    if show_title:
        axes.set_title(
            "Finite difference mesh demonstration\nDiameter = {:.2f} nm\n\
            {} elements of size {}x{} nm".format(
            diameter, elem_count, x_spacing, y_spacing
        )
        )


def plot_circular_fidi_mesh(
    diameter, x_spacing=1, y_spacing=1, translate=(0, 0),
    centre_mesh='auto', show_axes=True, show_title=True
):
    """
    Plots a representation of a circular mesh of specified diameter
    comprised of rectangular elements of size x_spacing x y_spacing nm.


    Miscellaneous info:
    ~~~~~~~~~~~~~~~~~~~
    This will set the middle of the mesh to lie at the centre of an
    element.
    centre_mesh = True

    This will set the middle of the mesh to lie at the corner of an
    element.
    centre_mesh = False

    The centering will be decided based on whichever will fit the
    geometry best.
    centre_mesh = 'auto'
    """
    fig = plt.figure(figsize=(0.1*diameter, 0.1*diameter))
    ax0 = fig.add_subplot(111)

    # Plot reference circle
    ax0.add_patch(plt.Circle((0, 0), radius=0.5*diameter, alpha=0.25))

    xcoords, ycoords = mesher(
        diameter=diameter, x_spacing=x_spacing, y_spacing=y_spacing,
        centre_mesh=centre_mesh, translate=translate
    )

    unit_area = x_spacing*y_spacing
    area = 0

    for x in xcoords:
        for y in ycoords:
            if CartesianCoords(x, y).r <= diameter/2.:
                ax0.add_patch(
                    patches.Rectangle(
                        (x-x_spacing/2., y-y_spacing/2.),
                        x_spacing, y_spacing, alpha=0.25
                    )
                )
                area += unit_area
    elem_count = area/unit_area

    titles_and_axes(
        show_title=show_title, show_axes=show_axes, axes=ax0,
        diameter=diameter, x_spacing=x_spacing, y_spacing=y_spacing,
        elem_count=elem_count, translate=translate
    )


def plot_poly_fidi_mesh(
    diameter, n, x_spacing=1, y_spacing=1, rotation=0, translate=(0, 0),
    centre_mesh='auto', show_axes=True, show_title=True
):
    """
    Plots a representation of an n-sided polygon mesh with a containing
    circle of specified diameter, comprised of rectangular elements of
    size x_spacing*y_spacing (in nanometres).


    Miscellaneous info:
    ~~~~~~~~~~~~~~~~~~~

    This will set the middle of the mesh to lie at the centre of an
    element.
    centre_mesh = True

    This will set the middle of the mesh to lie at the corner of an
    element.
    centre_mesh = False

    This will decide True or False based on whichever will best fit the
    geometry.
    centre_mesh = 'auto'

    The radius is defined as the circumradius, i.e., the distance from
    the circumcentre of the shape to one of its vertices.

    For example, to get a square with an edge length of 50, the
    diameter must be given as 50*(2**0.5), which is the distance from
    the centre of the square to one of its corners.
    """
    fig = plt.figure(figsize=(0.1*diameter, 0.1*diameter))
    ax0 = fig.add_subplot(111)
    xcoords, ycoords = mesher(
        diameter=diameter, x_spacing=x_spacing, y_spacing=y_spacing,
        centre_mesh=centre_mesh, translate=translate
    )

    # Plot reference polygon
    coords = np.empty((n, 2))
    for i in range(n):
        coord = CylindricalCoords(diameter/2., (2.*np.pi*i/n)+rotation)

        coords[i][0] = coord.x + translate[0]
        coords[i][1] = coord.y + translate[1]

    ax0.plot(
        np.transpose(
            np.concatenate((coords, coords), axis=0)[:n+1], (1, 0)
        )[0],
        np.transpose(
            np.concatenate((coords, coords), axis=0)[:n+1], (1, 0)
        )[1]
    )

    unit_area = x_spacing*y_spacing
    area = 0

    for x in xcoords:
        for y in ycoords:
            if in_poly(
                x=x, y=y, n=n, r=diameter/2., rotation=rotation,
                translate=translate, plot=False
            ):
                ax0.add_patch(
                    patches.Rectangle(
                        (x-x_spacing/2., y-y_spacing/2.),
                        x_spacing, y_spacing, alpha=0.25
                    )
                )
                area += unit_area
    elem_count = area/unit_area

    titles_and_axes(
        show_title=show_title, show_axes=show_axes, axes=ax0,
        diameter=diameter, x_spacing=x_spacing, y_spacing=y_spacing,
        elem_count=elem_count, translate=translate
    )
