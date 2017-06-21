# -*- coding: utf-8 -*-

# In py3, mock is included with the unittest standard library
# In py2, it's a separate package
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from unittest import TestCase
from datetime import datetime as dt
import pandas as pd
from pandas.util.testing import assert_series_equal
from alphaware.pipeline import (AlphaPipeline,
                                _call_fit)


class NoTransformT(object):
    """Transformer without transform method.
    """

    def fit(self, x):
        return self


class NoFitT(object):
    """Transformer without fit method.
    """

    def transform(self, x):
        return self


class Trans(object):
    """
    Transformer with fit and transform methods
    """

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return self


def func_x_y(x, y, kwarg='kwarg'):
    """
    Function with required x and y arguments
    """
    return


def func_x(x, kwarg='kwarg'):
    """
    Function with required x argument
    """
    return


def func_raise_type_err(x, y, kwarg='kwarg'):
    """
    Function with required x and y arguments,
    raises TypeError
    """
    raise TypeError


class TestPipeline(TestCase):

    def test_call_fit_error(self):
        with self.assertRaises(TypeError):
            _call_fit(Trans().fit, 'X', 'y', kwarg='kwarg')



