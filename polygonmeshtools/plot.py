import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .coords import CartesianCoords, CylindricalCoords
from .calc import in_poly


def plot_circular_fidi_mesh(
    diameter, x_spacing=2, y_spacing=2, centre_mesh='auto',
    show_axes=True, show_title=True
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

    Known bugs:
    ~~~~~~~~~~~

    When the x_spacing OR y_spacing is not a factor of the diameter,
    the mesh will not be centered correctly.

    It is recommended that centre_mesh be set to True in this case.
    """

    # Initial setup of figure
    fig = plt.figure(figsize=(diameter**0.45, diameter**0.45))
    ax0 = fig.add_subplot(111)

    ax0.set_xlim(-0.5*diameter, 0.5*diameter)
    ax0.set_ylim(-0.5*diameter, 0.5*diameter)

    # Plotting reference circle
    ax0.add_patch(plt.Circle((0, 0), radius=0.5*diameter, alpha=0.25))

    # Decide if centering will cause asymmetry
    if centre_mesh == 'auto':
        if diameter % (2*x_spacing) == 0 and diameter % (2*y_spacing) == 0:
            centre_mesh = False
        else:
            centre_mesh = True

    area = 0
    unit_area = x_spacing*y_spacing

    if centre_mesh == True:
        # Produce lists of the form [0,2,-2,4,-4,6,-6,8,-8,10,-10]
        #+ (spacing = 2; diameter = 20, in this^ example)
        # The idea is to start in the centre and then work outwards,
        #+ alternating sides
        xlist, ylist = centre_mesh_lists(diameter, x_spacing, y_spacing)

        for y in ylist:
            for x in xlist:
                box_coord = (x - 0.5*x_spacing, y - 0.5*y_spacing)
                if CartesianCoords(x, y).r <= 0.5*diameter:
                    # Plot rectangle
                    ax0.add_patch(
                        patches.Rectangle(
                            box_coord, x_spacing, y_spacing, alpha=0.25
                        )
                    )
                    area += unit_area
                else:
                    # If circle boundary is exceeded once, there is no
                    # point proceeding with this row, as all following
                    # coordinates will also lie outside the circle

                    # (Recall: we are working outwards and circles
                    # are symmetric)
                    break

    elif centre_mesh == False:
        xmax = int((diameter/2.)+(diameter % x_spacing))
        ymax = int((diameter/2.)+(diameter % y_spacing))
        xlist = range(-xmax, xmax, x_spacing)
        ylist = range(-ymax, ymax, y_spacing)
        for y in ylist:
            for x in xlist:
                centre_coord = (x + 0.5*x_spacing, y + 0.5*y_spacing)
                if (CartesianCoords(centre_coord[0], centre_coord[1]).r <=
                        0.5*diameter):
                    # Plot element
                    ax0.add_patch(
                        patches.Rectangle(
                            (x, y), x_spacing, y_spacing, alpha=0.25
                        )
                    )
                    area += unit_area
    else:
        raise ValueError(
            'Unrecognised value "{}" for centre_mesh! \
            Please choose True, False or "auto".'.format(centre_mesh)
        )

    elem_count = area/(x_spacing*y_spacing)

    titles_and_axes(
        show_title=show_title, show_axes=show_axes, axes=ax0,
        diameter=diameter, x_spacing=x_spacing, y_spacing=y_spacing,
        elem_count=elem_count
    )


def plot_poly_fidi_mesh(
    diameter, n, x_spacing=2, y_spacing=2, rotation=0, translate=(0, 0),
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

    # Initial setup of figure
    fig = plt.figure(figsize=(diameter**0.45, diameter**0.45))
    ax0 = fig.add_subplot(111)

    ax0.set_xlim(-0.5*diameter+translate[0], 0.5*diameter+translate[0])
    ax0.set_ylim(-0.5*diameter+translate[1], 0.5*diameter+translate[1])

    # Decide if centering will prevent asymmetry
    # In future, potentially decide x and y centring separately
    #+ (will add many lines of code and complexity, is it worth it?)
    if centre_mesh == 'auto':
        if diameter % (2*x_spacing) == 0 and diameter % (2*y_spacing) == 0:
            centre_mesh = False
        else:
            centre_mesh = True

    area = 0
    unit_area = x_spacing*y_spacing

    if centre_mesh == True:
        #produce lists of the form [0,2,-2,4,-4,6,-6,8,-8,10,-10]
        # (spacing = 2; diameter = 20, in this^ example)
        xlist, ylist = centre_mesh_lists(
            diameter, x_spacing, y_spacing, translate
        )

        for y in ylist:
            for x in xlist:
                box_coord = (x - 0.5*x_spacing, y - 0.5*y_spacing)
                if in_poly(
                    x, y, n=n, r=diameter/2., rotation=rotation,
                    translate=translate, plot=False
                ):
                    # Plot element
                    ax0.add_patch(
                        patches.Rectangle(
                            box_coord, x_spacing, y_spacing, alpha=0.25
                        )
                    )

                    area += unit_area

    elif centre_mesh == False:
    # Start from top left corner and work across and down
    # Note: this is less efficient than centre_mesh = True, as the
    #+ entirety of the area is tested
        xmax = int((diameter/2.) + (diameter % x_spacing))
        ymax = int((diameter/2.) + (diameter % y_spacing))

        xlist = [x + translate[0] for x in range(-xmax, xmax, x_spacing)]
        ylist = [y + translate[1] for y in range(-ymax, ymax, y_spacing)]

        for y in ylist:
            for x in xlist:
                centre_coord = (x + 0.5*x_spacing, y + 0.5*y_spacing)

                if in_poly(
                    centre_coord[0], centre_coord[1], n=n, r=diameter/2.,
                    rotation=rotation, translate=translate
                ):
                    ax0.add_patch(
                        patches.Rectangle(
                            (x, y), x_spacing, y_spacing, alpha=0.25
                        )
                    )
                    area += unit_area

    else:
        raise ValueError(
            'Unrecognised value "{}" for centre_mesh! \
            Please choose True, False or "auto".'.format(centre_mesh)
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

    elem_count = area/(x_spacing*y_spacing)

    titles_and_axes(
        show_title=show_title, show_axes=show_axes, axes=ax0,
        diameter=diameter, x_spacing=x_spacing, y_spacing=y_spacing,
        elem_count=elem_count
    )


def titles_and_axes(
    show_title, show_axes, axes, diameter, x_spacing, y_spacing, elem_count
):
    """
    Handles axes and titles for plot_poly_fidi_mesh and
    plot_circular_fidi_mesh.
    """
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


def centre_mesh_lists(diameter, x_spacing, y_spacing, translate=(0, 0)):
    """
    Returns xlist and ylist
    """
    xlist = sorted(
        list(range(0, int(diameter/2)+1, x_spacing)) +
        list(range(0, -int(diameter/2)-1, -x_spacing)), key=abs
    )[1:]

    ylist = sorted(
        list(range(0, int(diameter/2)+1, x_spacing)) +
        list(range(0, -int(diameter/2)-1, -y_spacing)), key=abs
    )[1:]

    xlist = [x + translate[0] for x in xlist[:]]
    ylist = [y + translate[1] for y in ylist[:]]

    return xlist, ylist
