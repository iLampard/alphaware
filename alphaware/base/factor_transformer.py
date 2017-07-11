# -*- coding: utf-8 -*-

import copy
import numpy as np
import pandas as pd
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from argcheck import (preprocess,
                      expect_types)
from .factor_container import ensure_factor_container


class FactorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, copy=True, out_container=False):
        self.copy = copy
        self.df_mapper = None
        self.out_container = out_container

    @expect_types(out=bool)
    def set_out_container(self, out):
        self.out_container = out

    @preprocess(factor_container=ensure_factor_container)
    def fit(self, factor_container, **kwargs):
        self.df_mapper = self._build_mapper(factor_container)
        return self

    def _build_mapper(self, factor_container):
        raise NotImplementedError

    @preprocess(factor_container=ensure_factor_container)
    def transform(self, factor_container):
        if self.copy:
            factor_container = copy.deepcopy(factor_container)
        tiaocang_date = factor_container.tiaocang_date
        calc_data = [self.df_mapper.fit_transform(factor_container.data.loc[date_]) for date_ in
                     tiaocang_date]
        calc_data_agg = np.vstack(calc_data)
        factor_container.data = pd.DataFrame(calc_data_agg,
                                             index=factor_container.data.index,
                                             columns=factor_container.data.columns)
        if self.out_container:
            return factor_container
        else:
            return factor_container.data











