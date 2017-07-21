# -*- coding: utf-8 -*-

import pandas as pd
from copy import deepcopy
from PyFin.Utilities import pyFinAssert
from ..base import (Factor,
                    FactorTransformer)
from ..utils import weighted_rank
from ..const import INDEX_FACTOR
from ..enums import FactorType


class FactorSimpleRank(FactorTransformer):
    def __init__(self, factor_name=None, weight=None, ascend_order=None):
        super(FactorSimpleRank, self).__init__()
        self.factor_name = factor_name
        self.weight = weight
        self.ascend_order = ascend_order

    def fit(self, factor_container, **kwargs):
        self.factor_name = factor_container.alpha_factor_col if self.factor_name is None else self.factor_name
        pyFinAssert(self.factor_name in factor_container.alpha_factor_col, ValueError,
                    'factor_name must be one of alpha factors in factor container')
        nb_factor = len(self.factor_name)
        self.weight = [1.0 / nb_factor] * nb_factor if self.weight is None else self.weight
        self.ascend_order = [1] * nb_factor if self.ascend_order is None else self.ascend_order
        return self

    def _build_mapper(self, factor_container):
        pass

    def transform(self, factor_container):
        if self.copy:
            factor_container = deepcopy(factor_container)
        data_factor = factor_container.data[self.factor_name]
        tiaocang_date = factor_container.tiaocang_date
        rank_df = pd.DataFrame()
        for date in tiaocang_date:
            rank_date = weighted_rank(data_factor.loc[date],
                                      weight=self.weight,
                                      ascend_order=self.ascend_order,
                                      out_df=True)
            rank_df = pd.concat([rank_df, rank_date], axis=1)

        rank_factor = Factor(data=rank_df, name=INDEX_FACTOR.col_score , property_dict={'type': FactorType.SCORE})
        factor_container.add_factor(rank_factor, overwrite=True)
        if self.out_container:
            return factor_container
        else:
            return factor_container.data
