
def plot_circular_fidi_mesh(diameter, x_spacing=2, y_spacing=2,
centre_mesh='auto', show_axes=True, show_title=True):
    """
    Plots a representation of a circular mesh of specified diameter 
    comprised of rectangular elements of size x_spacing x y_spacing nm.
    
    
    Requires the following imports:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    
    
    Miscellaneous info:
    ~~~~~~~~~~~~~~~~~~~
    
    centre_mesh = True    This will set the middle of the mesh to lie at the centre of an element.
    centre_mesh = False     "    "   "   "     "    "  "    "   "  "   "  "  corner  "  "    "   .
    centre_mesh = 'auto'  The centering will be decided based on whichever will fit the geometry best.
    
    
    Known bugs:
    ~~~~~~~~~~~
    
    When the diameter/x_spacing or y_spacing does not produce an integer, the mesh will not be centered correctly.
    It is recommended that centre_mesh be set to True in this case.
    """
    
    #initial setup of figure
    fig = plt.figure(figsize = (diameter**0.45,diameter**0.45))
    ax0 = fig.add_subplot(111)
    
    ax0.set_xlim(-0.5*diameter, 0.5*diameter)
    ax0.set_ylim(-0.5*diameter, 0.5*diameter)
    
    if show_axes == True:
        ax0.set_xlabel("Radius (nm)"); ax0.set_ylabel("Radius (nm)")
    else:
        ax0.get_yaxis().set_visible(False)
        ax0.get_xaxis().set_visible(False)
        ax0.set_frame_on(False)
    
    #plotting reference circle
    ax0.add_patch(plt.Circle((0,0), radius = 0.5*diameter, alpha = 0.25))
    
    #decide if centering will cause asymmetry
    if centre_mesh == 'auto':
        if diameter%(2*x_spacing) == 0 and diameter%(2*y_spacing) == 0:
            centre_mesh = False
        else:
            centre_mesh = True
    
    area = 0
    unit_area = x_spacing*y_spacing
    
    if centre_mesh == True:
        #produces lists of the form [0,2,-2,4,-4,6,-6,8,-8,10,-10]
        #(spacing = 2; diameter = 20, in this example)
        #trailing slice index is to remove leading zero which would cause duplicate patches
        xlist = sorted(list(range(0, (diameter/2)+1, x_spacing)) 
                       + list(range(0,-(diameter/2)-1,-x_spacing)), 
                       key=abs)[1:]
        ylist = sorted(list(range(0, (diameter/2)+1, y_spacing)) 
                       + list(range(0,-(diameter/2)-1,-y_spacing)), 
                       key=abs)[1:]
    
        for y in ylist:
            for x in xlist:
                box_coord = (x - 0.5*x_spacing, y - 0.5*y_spacing)
                if CartesianCoords(x,y).r <= 0.5*diameter:
                    #plot rectangle
                    ax0.add_patch(patches.Rectangle(box_coord, x_spacing, y_spacing, alpha = 0.25))
                    area += unit_area
                else:
                    break #if circle boundary exceeded once, no point proceeding with this row
    elif centre_mesh == False:
        xmax = int((diameter/2.)+(diameter%x_spacing))
        ymax = int((diameter/2.)+(diameter%y_spacing))
        xlist = range(-xmax,xmax,x_spacing)
        ylist = range(-ymax,ymax,y_spacing)
        for y in ylist:
            for x in xlist:
                centre_coord = (x + 0.5*x_spacing, y + 0.5*y_spacing)
                if (CartesianCoords(centre_coord[0], centre_coord[1]).r <= 0.5*diameter):
                    #plot element
                    ax0.add_patch(patches.Rectangle((x,y), x_spacing, y_spacing, alpha = 0.25))
                    area += unit_area
                else:
                    pass 
    else:
        raise ValueError("Unrecognised value for centre_mesh! Please choose True, False or 'auto'.")
    
    elem_count = area/(x_spacing*y_spacing)
    
    if show_title == True:
        ax0.set_title("Finite difference mesh demonstration\n        Diameter = {} nm\n{} elements of size {}x{} nm"
                      .format(diameter, elem_count, x_spacing, y_spacing))
    #return area



def plot_poly_fidi_mesh(diameter,n,x_spacing=2,y_spacing=2,rotation=0,translate=(0,0),
                        centre_mesh='auto',show_axes=True, show_title=True):
    """
    Plots a representation of an n-sided polygon mesh with a containing circle
    of specified diameter, comprised of rectangular elements of size 
    x_spacing*y_spacing (in nanometres).
    
    
    Requires the following imports:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    
    
    Miscellaneous info:
    ~~~~~~~~~~~~~~~~~~~
    
    centre_mesh = True    will set the middle of the mesh to lie at the centre of an element.
    centre_mesh = False     "   "   "     "    "  "    "   "  "   "  "  corner  "  "    "   .
    centre_mesh = 'auto'  will decide True or False based on whichever will best fit the geometry.
    
    The radius is defined as the circumradius, i.e., the distance from the circumcentre
    of the shape to one of its vertices.
    For example, to get a square with edge length 50, diameter must be given as 50*(2**0.5).
    
    
    Known bugs:
    ~~~~~~~~~~~
    Using find_circumradius to give exact side lengths can produce unusual
    tails trailing off some corners.
    """
    
    #initial setup of figure
    fig = plt.figure(figsize = (diameter**0.45,diameter**0.45))
    ax0 = fig.add_subplot(111)
    
    ax0.set_xlim(-0.5*diameter+translate[0], 0.5*diameter+translate[0])
    ax0.set_ylim(-0.5*diameter+translate[1], 0.5*diameter+translate[1])
    
    if show_axes == True:
        ax0.set_xlabel("x (nm)"); ax0.set_ylabel("y (nm)")
    else:
        ax0.get_yaxis().set_visible(False)
        ax0.get_xaxis().set_visible(False)
        ax0.set_frame_on(False)    
    
    #decide if centering will prevent asymmetry
    #maybe incorporate independent centering for x and y
    #(tried this and it was extremely difficult...)
    if centre_mesh == 'auto':
        if diameter%(2*x_spacing) == 0 and diameter%(2*y_spacing) == 0:
            centre_mesh = False
        else:
            centre_mesh = True
    
    area = 0
    unit_area = x_spacing*y_spacing
    
    if centre_mesh == True:
        #produces lists of the form [0,2,-2,4,-4,6,-6,8,-8,10,-10]
        #(spacing = 2; diameter = 20, in this example)
        #trailing slice index is to remove leading zero which would cause duplicate patches
        xlist = sorted(list(range(0, int(diameter/2)+1, x_spacing)) 
                       + list(range(0,-int(diameter/2)-1,-x_spacing)), key=abs)[1:]
        xlist = [x + translate[0] for x in xlist[:]]
        ylist = sorted(list(range(0, int(diameter/2)+1, y_spacing)) 
                      + list(range(0,-int(diameter/2)-1,-y_spacing)), key=abs)[1:]
        ylist = [y + translate[1] for y in ylist[:]]
    
        for y in ylist:
            for x in xlist:
                box_coord = (x - 0.5*x_spacing, y - 0.5*y_spacing)
                if in_poly(x, y, n=n, r=diameter/2.,
                           rotation=rotation, translate=translate, plot=False):
                    #plot element
                    ax0.add_patch(patches.Rectangle(box_coord, x_spacing, y_spacing, alpha = 0.25))
                    area += unit_area
                else:
                    pass
                
    elif centre_mesh == False:
        xmax = int((diameter/2.)+(diameter%x_spacing))
        ymax = int((diameter/2.)+(diameter%y_spacing))
        xlist = [x + translate[0] for x in range(-xmax,xmax,x_spacing)]
        ylist = [y + translate[1] for y in range(-ymax,ymax,y_spacing)]
        
        for y in ylist:
            for x in xlist:
                centre_coord = (x + 0.5*x_spacing, y + 0.5*y_spacing)
                if in_poly(centre_coord[0], centre_coord[1], n=n, r=diameter/2.,
                           rotation=rotation, translate=translate):
                    ax0.add_patch(patches.Rectangle((x,y), x_spacing, y_spacing, alpha = 0.25))
                    area += unit_area
                else:
                    pass        
    else:
        raise ValueError("Unrecognised value \"{}\" for centre_mesh! Please choose True, False or 'auto'."
                         .format(centre_mesh))
    
    #plot reference polygon
    coords = np.empty((n,2))
    for i in range(n):
        coord = PolarCoords(diameter/2., (2.*np.pi*i/n)+rotation)
        coords[i][0], coords[i][1] = coord.x+translate[0], coord.y+translate[1]
    ax0.plot(np.transpose(np.concatenate((coords, coords),axis=0)[:n+1],
                          (1,0))[0],np.transpose(np.concatenate((coords, coords),axis=0)[:n+1], (1,0))[1])
    elem_count = area/(x_spacing*y_spacing)
    
    if show_title == True:
        ax0.set_title("Finite difference mesh demonstration\nDiameter = {:.2f} nm\n{} elements of size {}x{} nm"
                      .format(diameter, elem_count, x_spacing, y_spacing))

