# -*- coding: utf-8 -*-

import copy
import numpy as np
import pandas as pd
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from argcheck import preprocess
from .factor_container import ensure_factor_container


class FactorEstimator(BaseEstimator, TransformerMixin):
    def __init__(self, copy=True, groupby_date=True):
        self.groupby_date = groupby_date
        self.copy = copy
        self.df_mapper = None

    @preprocess(factor_container=ensure_factor_container)
    def fit(self, factor_container, **kwargs):
        self.df_mapper = self._build_imputer_mapper(factor_container, **kwargs)
        return self

    def _build_imputer_mapper(self, factor_container, **kwargs):
        """
        https://github.com/pandas-dev/sklearn-pandas/blob/master/sklearn_pandas/dataframe_mapper.py 
        """
        raise NotImplementedError

    @preprocess(factor_container=ensure_factor_container)
    def transform(self, factor_container):
        if self.copy:
            factor_container = copy.deepcopy(factor_container)
        if not self.groupby_date:
            imputer_data_agg = self.df_mapper.fit_transform(factor_container.data)
        else:
            tiaocang_date = factor_container.tiaocang_date
            imputer_data = [self.df_mapper.fit_transform(factor_container.data.loc[date_]) for date_ in
                            tiaocang_date]
            imputer_data_agg = np.vstack(imputer_data)
        factor_container.data = pd.DataFrame(imputer_data_agg,
                                             index=factor_container.data.index,
                                             columns=factor_container.data.columns)
        return factor_container.data
