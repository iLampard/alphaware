# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from copy import deepcopy
from PyFin.Utilities import pyFinAssert
from alphaware.base import FactorTransformer


class FactorSimpleRank(FactorTransformer):
    def __init__(self, factor_name=None, weight=None, rank_order=None):
        super(FactorSimpleRank, self).__init__()
        self.factor_name = factor_name
        self.weight = weight
        self.rank_order = rank_order

    def fit(self, factor_container, **kwargs):
        self.factor_name = factor_container.alpha_factor_col if self.factor_name is None else self.factor_name
        pyFinAssert(self.factor_name in factor_container.alpha_factor_col, ValueError,
                    'factor_name must be one of alpha factors in factor container')
        nb_factor = len(self.factor_name)
        self.weight = [1.0 / nb_factor] * nb_factor if self.weight is None else self.weight
        self.rank_order = [1] * nb_factor if self.rank_order is None else self.rank_order
        return self

    def transform(self, factor_container):
        if self.copy:
            factor_container = deepcopy(factor_container)
        data_factor = factor_container.data[self.factor_name]
        tiaocang_date = factor_container.tiaocang_date
        for date in tiaocang_date:
            rank = data_factor.loc[date]
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
