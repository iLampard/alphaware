# -*- coding: utf-8 -*-

import io
import sys
import numpy as np
from setuptools import find_packages
from setuptools import setup

PACKAGE = 'alphaware'
NAME = 'alphaware'
VERSION = '0.2.3'
DESCRIPTION = 'alpha research tools'
AUTHOR = 'iLampard, RoxanneYang, MarkSh714'
URL = 'https://github.com/iLampard/alphaware'
LICENSE = 'MIT'

if sys.version_info > (3, 0, 0):
    requirements = "requirements/py3.txt"
else:
    requirements = "requirements/py2.txt"

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      url=URL,
      include_package_data=False,
      packages=find_packages(),
      install_requires=io.open(requirements, encoding='utf8').read(),
      include_dirs=[np.get_include()],
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'])
