import os
from setuptools import setup

#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "polygon-finite-difference-mesh-tools",
    version = "0.0.1",
    author = "Xander Marjoram",
    author_email = "am31g12@soton.ac.uk",
    description = ("A package for creating polygon-based geometries from"
                   "cuboidal finite difference meshes"),
    keywords = "polygon mesh geometry finite difference",
    url = "https://bitbucket.org/fangohr/polygon-finite-difference-mesh-tools",
    packages=['notebooks', 'tests'],
    long_description=read('readme')
)
