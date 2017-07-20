# -*- coding: utf-8 -*-

from alphaware import (analyzer,
                       base,
                       metrics,
                       pipeline,
                       preprocess,
                       utils,
                       selector,
                       tests)

__all__ = ['version',
           'analyzer',
           'base',
           'metrics',
           'pipeline',
           'preprocess',
           'utils',
           'selector',
           'tests']


def version():
    return __version__


__version__ = '0.2.0'
