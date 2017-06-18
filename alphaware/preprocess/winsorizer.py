# -*- coding: utf-8 -*-

import numpy as np
from PyFin.Utilities import pyFinAssert
from argcheck import (coerce,
                      preprocess)
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from .factor_container import (Factor,
                               ensure_factor_container)


def winsorize(x, quantile_range=(2.5, 97.5)):
    """ 
    :param x: pd.Series, 原始数据(如截面因子)
    :param quantile_range: tuple (q_min, q_max), 0.0 < q_min < q_max < 100.0, 去掉分位数在(q_min, q_max)的数据
    :return: pd.Series, 去极值化后的数据
    """
    q_min, q_max = quantile_range
    pyFinAssert(0.0 <= q_min < q_max <= 100.0, ValueError, 'Invalid quantile range: %s' % str(quantile_range))
    q = np.percentile(x, quantile_range, axis=0)
    ret = x[x <= q[1]]
    ret = ret[ret >= q[0]]
    return ret


class FactorWinsorizer(BaseEstimator, TransformerMixin):
    def __init__(self, quantile_range=(2.5, 97.5), copy=True):
        self.quantile_range = quantile_range
        self.copy = copy

    @preprocess(factor_containter=coerce(type(Factor), ensure_factor_container))
    def fit(self, factor_containter):
        pass

    @preprocess(factor_containter=coerce(type(Factor), ensure_factor_container))
    def transform(self, factor_containter):
        pass
