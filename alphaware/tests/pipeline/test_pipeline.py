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
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from alphaware.preprocess import (Factor,
                                  FactorContainer)
from alphaware.pipeline import AlphaPipeline
from alphaware.enums import (FactorType,
                             FactorNormType)


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


class TransDiv4(BaseEstimator, TransformerMixin):
    """
    Transformer with fit and transform methods
    """

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x.data / 4


class TransMulti2(BaseEstimator, TransformerMixin):
    """
    Transformer with fit and transform methods
    """

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x.data * 2


class TestPipeline(TestCase):
    def setUp(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003', '004']],
                                           names=['tradeDate', 'secID'])
        data1 = pd.DataFrame(index=index, data=[1.0, 1.0, 1.2, 2.0, 0.9, 5.0, 5.0, 5.1])
        factor_test1 = Factor(data=data1, name='test1',
                              property_dict={'norm_type': FactorNormType.Industry_Cap_Neutral})

        data2 = pd.DataFrame(index=index, data=[2.6, 2.5, 2.8, 2.9, 2.7, 1.9, 5.0, 2.1])
        factor_test2 = Factor(data=data2, name='test2', property_dict={'type': FactorType.ALPHA_FACTOR_MV})

        data3 = pd.DataFrame(index=index, data=['a', 'b', 'a', 'a', 'a', 'b', 'c', 'b'])
        factor_test3 = Factor(data=data3, name='test3', property_dict={'type': FactorType.INDUSTY_CODE})

        data4 = pd.DataFrame(index=index, data=[1.0, 1.0, 1.2, 2.0, 0.9, 5.0, 5.0, 5.1])
        factor_test4 = Factor(data=data4, name='test4', property_dict={'norm_type': FactorNormType.Industry_Neutral})

        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test1, factor_test2, factor_test3, factor_test4])

        self.factor_container = fc

    def test_error_raise(self):
        with self.assertRaises(TypeError):
            AlphaPipeline([('no_transform', NoTransformT())])

        with self.assertRaises(TypeError):
            AlphaPipeline([('no_fit', NoFitT())])

    def test_factor_tranformer(self):
        pipeline = AlphaPipeline([('multi', TransMulti2()),
                                    ('div', TransDiv4())])
        calculated = pipeline.fit_transform(self.factor_container)
        print calculated
