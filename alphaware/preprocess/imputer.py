# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import copy
from argcheck import expect_element
from sklearn.preprocessing import Imputer
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from sklearn.utils.validation import check_is_fitted
from sklearn_pandas import (CategoricalImputer,
                            DataFrameMapper)
from argcheck import (preprocess,
                      coerce)
from ..enums import (NAStrategy,
                     FactorType)
from .factor_container import (Factor,
                               ensure_factor_container)


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


class FactorImputer(BaseEstimator, TransformerMixin):
    def __init__(self,
                 missing_value='NaN',
                 numerical_strategy=NAStrategy.MEAN,
                 axis=0,
                 verbose=0,
                 copy=True,
                 custom_value=None,
                 categorical_strategy=NAStrategy.MOST_FREQ,
                 **kwargs):
        self.missing_values = missing_value
        self.copy = copy
        self.numerical_strategy = numerical_strategy
        self.categorical_strategy = categorical_strategy
        self.axis = axis
        self.verbose = verbose
        self.copy = copy
        self.custom_value = custom_value
        self.mapper = None
        self.groupby_date = kwargs.get('groupby_date', True)  # do the imputation based on grouped date
        self.df_mapper = None

    @preprocess(factor_containter=coerce(type(Factor), ensure_factor_container))
    def fit(self, factor_container):
        self.df_mapper = self._build_imputer_mapper(factor_container)
        return self

    def _build_imputer_mapper(self, factor_container):
        """
        https://github.com/pandas-dev/sklearn-pandas/blob/master/sklearn_pandas/dataframe_mapper.py 
        """
        data = factor_container.data
        data_mapper = [([factor_name], self._get_imputer(factor_container.property[factor_name]['type']))
                       for factor_name in data.columns]
        return DataFrameMapper(data_mapper)

    def _get_imputer(self, factor_type):
        if factor_type == FactorType.INDUSTY_CODE:
            return ExtCategoricalImputer(strategy=self.categorical_strategy,
                                         custom_value=self.custom_value)
        elif factor_type == FactorType.ALPHA_FACTOR or factor_type == FactorType.RETURN:
            return Imputer(missing_values=self.missing_values,
                           strategy=self.numerical_strategy,
                           axis=self.axis,
                           verbose=self.verbose,
                           copy=self.copy)

    @preprocess(factor_containter=coerce(type(Factor), ensure_factor_container))
    def transform(self, factor_container):
        if self.copy:
            factor_container = copy.deepcopy(factor_container)
        if not self.groupby_date:
            imputer_data_agg = self.df_mapper.fit_transform(factor_container.data)
        else:
            tiaocang_date = factor_container.tiaocang_date
            imputer_data = [self.df_mapper.fit_transform(factor_container.data.ix[date_])
                            for date_ in range(len(tiaocang_date))]
            imputer_data_agg = np.vstack(imputer_data)
        factor_container.data = pd.DataFrame(imputer_data_agg,
                                             index=factor_container.data.index,
                                             columns=factor_container.data.columns)
        return factor_container.data
