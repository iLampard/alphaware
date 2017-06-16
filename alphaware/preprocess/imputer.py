# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from argcheck import expect_element
from sklearn.utils.validation import check_is_fitted
from sklearn_pandas import (CategoricalImputer,
                            DataFrameMapper)
from ..enums import NAStrategy


def _get_mask(X, value):
    """
    Compute the boolean mask X == missing_values.
    """
    if value == 'NaN' or value is None or (isinstance(value, float) and np.isnan(value)):
        return pd.isnull(X)
    else:
        return X == value


class ExtCategoricalImputer(CategoricalImputer):
    """
    ref: https://github.com/pandas-dev/sklearn-pandas/blob/master/sklearn_pandas/categorical_imputer.py
    """

    @expect_element(strategy=(NAStrategy.CUSTOM, NAStrategy.MOST_FREQ))
    def __init__(self, missing_value='NaN', copy=True, custom_value=None, strategy=NAStrategy.MOST_FREQ):
        super(ExtCategoricalImputer, self).__init__(missing_values=missing_value, copy=copy)
        self.missing_values = missing_value
        self.copy = copy
        self.strategy = strategy
        self.custom_value = custom_value
        self.fill_ = None

    def fit(self, X, y=None):
        if self.strategy == NAStrategy.MOST_FREQ:
            return super(ExtCategoricalImputer, self).fit(X, y)
        elif self.strategy == NAStrategy.CUSTOM:
            self.fill_ = self.custom_value
            return self

    def transform(self, X):
        if self.strategy == NAStrategy.MOST_FREQ:
            return super(ExtCategoricalImputer, self).transform(X)

        if self.copy:
            X = X.copy()

        check_is_fitted(self, 'fill_')

        mask = _get_mask(X, self.missing_values)
        X[mask] = self.fill_

        return np.asarray(X)