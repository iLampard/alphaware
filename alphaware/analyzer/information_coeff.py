# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from scipy import stats
from sklearn_pandas import DataFrameMapper
from argcheck import expect_types
from ..preprocess.factor_transformer import FactorTransformer


class FactorIC(FactorTransformer):
    def __init__(self, copy=True, out_container=False):
        super(FactorIC, self).__init__(copy=copy, out_container=out_container)

    def transform(self, factor_container):

        data_df = factor_container.data


        factor_container.data = data_df
        if self.out_container:
            return factor_container
        else:
            return factor_container.data

