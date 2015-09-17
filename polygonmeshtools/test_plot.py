import numpy as np
import matplotlib.pyplot as plt
import pytest

from .plot import *


def test_mesher():
    # Basic case
    xmesh, ymesh = mesher(
        diameter=20, x_spacing=1, y_spacing=2,
        translate=(0, 0), centre_mesh=True
    )
    for x in range(-10, 11, 1):
        assert x in xmesh
    for y in range(-10, 11, 2):
        assert y in ymesh

    # Testing translation
    xmesh, ymesh = mesher(
        diameter=20, x_spacing=1, y_spacing=2,
        translate=(10, -10), centre_mesh=True
    )
    for x in range(21):
        assert x in xmesh
    for y in range(-20, 1, 2):
        assert y in ymesh

    # centre_mesh = False
    xmesh, ymesh = mesher(
        diameter=20, x_spacing=1, y_spacing=2,
        translate=(0, 0), centre_mesh=False
    )
    for x in np.linspace(-10.5, 9.5, 21):
        assert x in xmesh
    for y in np.linspace(-11, 9, 11):
        assert y in ymesh

    # centre_mesh = auto
    xmesh, ymesh = mesher(
        diameter=20, x_spacing=1, y_spacing=2,
        translate=(0, 0), centre_mesh='auto'
    )
    for x in np.linspace(-10.5, 9.5, 21):
        assert x in xmesh
    for y in np.linspace(-11, 9, 11):
        assert y in ymesh


def test_plot_circular_fidi_mesh():
    # Testing default conditions
    plot_circular_fidi_mesh(diameter=30)

    # Hiding axes
    plot_circular_fidi_mesh(diameter=10, show_axes=False)

    # Hiding title
    plot_circular_fidi_mesh(diameter=10, show_title=False)

    # centre_mesh = False
    plot_circular_fidi_mesh(diameter=30, centre_mesh=False)

    # incorrect value for centre_mesh
    with pytest.raises(ValueError):
        plot_circular_fidi_mesh(diameter=10, centre_mesh='test')


def test_plot_poly_fidi_mesh():
    # Default conditions
    for n in range(3, 8):
        plot_poly_fidi_mesh(diameter=20, n=n)

    # Hiding axes
    plot_poly_fidi_mesh(diameter=20, n=3, show_axes=False)

    # Hiding title
    plot_poly_fidi_mesh(diameter=20, n=3, show_title=False)

    # centre_mesh = 'auto', decision-making
    plot_poly_fidi_mesh(
        diameter=30, x_spacing=3, y_spacing=3, n=6, centre_mesh='auto'
    )
    # Above test inexplicably fails to satisfy the following:
    # (diameter % (2*x_spacing) == 0) and (diameter % (2*y_spacing) == 0)
    # Assuming bug in coverage.py...
    plot_poly_fidi_mesh(
        diameter=30, x_spacing=3, y_spacing=4, n=5, centre_mesh='auto'
    )

    # centre_mesh = False
    plot_poly_fidi_mesh(diameter=30, n=5, centre_mesh=False)
    # Incorrect value for centre_mesh
    with pytest.raises(ValueError):
        plot_poly_fidi_mesh(diameter=10, n=3, centre_mesh='test')
