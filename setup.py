#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setup for the pxst-widgets project
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Extension
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


__version__ = '0.0.1'

setup(
  name = 'pxst-widgets',
  version=__version__,
  description = 'libossia usefull Classes',
  long_description=long_description,
  url='https://github.com/PixelStereo/pxst-widgets',
  author = 'Pixel Stereo',
  license='GPLv3+',
  classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ],
  keywords='sample setuptools development',
  # You can just specify the packages manually here if your project is
  # simple. Or you can use find_packages().
  packages=find_packages(exclude=['3rdParty', 'examples', 'docs', 'tests']),
  install_requires=['pyossia'],
  extras_require={
    'test': ['coverage']
    },
  download_url = 'https://github.com/PixelStereo/pxst-widgets/tarball/' + __version__,
)
