#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setup for the pxst_widgets package
"""

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get current version
import versioneer
__version__ = versioneer.get_version()

setup(
  name = 'pxst_widgets',
  version=__version__,
  description = 'pxst_widgets',
  long_description=long_description,
  url='https://github.com/PixelStereo/pxst_widgets',
  author = 'Pixel Stereo',
  author_email='contact@pixelstereo.org',
  license='GPLv3+',
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ],
  keywords=['creative', 'controls', 'osc', 'oscquery', 'websocket', 'gui', 'graphic user interface'],
  packages          = ['pxst_widgets'],
  install_requires=[
          'PyQt5', 'pyossia'
      ],
  extras_require={
    'test': ['coverage']
    },
  zip_safe=False,
)
