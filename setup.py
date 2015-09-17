import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "polygonmeshtools",
    packages = ["polygonmeshtools"],
    version = "0.46",
    description = "A package for creating polygon-shaped geometries \
        from cuboidal finite difference elements",
    author = "Xander Marjoram",
    author_email = "am31g12@soton.ac.uk",
    keywords = [
            "polygon", "mesh", "geometry",
            "finite", "difference", "fidimag"
        ],
    url = "https://bitbucket.org/fangohr/polygon-finite-difference-mesh-tools/get/tip.tar.gz",
    #classifiers = [],
)
