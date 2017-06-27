# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from copy import deepcopy
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from sklearn_pandas import DataFrameMapper
from PyFin.Utilities import pyFinAssert
from argcheck import expect_types
from .preprocess import FactorTransformer
from .enums import (FactorType,
                    SelectionMethod)
from .const import MULTI_INDEX_SELECTOR


class IndustryNeutralSelector(BaseEstimator, TransformerMixin):
    def __init__(self, industry_weight, prop_select=0.1, ascend_order=True, min_select_per_industry=2):
        self.industry_weight = industry_weight
        self.prop_select = prop_select
        self.min_select_per_industry = min_select_per_industry
        self.ascend_order = ascend_order
        self.score = None
        self.industry_code = None

    def fit(self, X, col_score='score', col_industry_code='industry_code'):
        self.score = X[col_score]
        self.industry_code = X[col_industry_code]
        return self

    def transform(self, X):
        """
        :param X: pd.DataFrame
        :return: 
        """

        ret = pd.DataFrame()
        for name, group in X.groupby(self.industry_code.name):
            if self.industry_weight[name] == 0:
                continue
            nb_select = int(max(len(X) * self.prop_select, self.min_select_per_industry))
            nb_select = len(group) if nb_select > len(group) else nb_select
            largest_score = group.nlargest(n=nb_select, columns=self.score)
            largest_score['weight'] = [self.industry_weight[name] / nb_select] * nb_select

            ret = pd.concat([ret, largest_score[[self.score, 'weight']]], axis=0)

        return ret


class BrutalSelector(BaseEstimator, TransformerMixin):
    def __init__(self, nb_select=10, prop_select=0.1):
        self.nb_select = nb_select
        self.prop_select = prop_select

    def fit(self, X):
        return self

    @expect_types(X=pd.Series)
    def transform(self, X):
        """
        :param X: pd.Series
        :return: 
        """

        ret = pd.DataFrame()
        nb_select = self.nb_select if self.nb_select is not None else int(len(X) * self.prop_select)
        largest_score = X.nlargest(n=nb_select)
        weight = [100.0 / nb_select] * nb_select
        ret = pd.concat([ret, pd.Series(weight, index=largest_score.index)], axis=0)
        ret.columns = MULTI_INDEX_SELECTOR.col_name
        return ret


class Selector(FactorTransformer):
    def __init__(self,
                 industry_weight=None,
                 method=SelectionMethod.INDUSTRY_NEUTRAL,
                 nb_select=10,
                 prop_select=0.1,
                 ascend_order=True,
                 copy=True,
                 groupby_date=True,
                 out_container=False):
        super(Selector, self).__init__(copy=copy, groupby_date=groupby_date, out_container=out_container)
        self.method = method
        self.nb_select = nb_select
        self.prop_select = prop_select
        self.ascend_order = ascend_order
        self.industry_weight = industry_weight

    def _build_mapper(self, factor_container):
        data = factor_container.data
        data_mapper = [([factor_name], self._get_mapper(factor_type=factor_container.property[factor_name]['type']))
                       for factor_name in data.columns]
        return DataFrameMapper(data_mapper)

    def _get_mapper(self, factor_type):
        if factor_type == FactorType.SCORE:
            if self.method == SelectionMethod.INDUSTRY_NEUTRAL:
                pyFinAssert(self.industry_weight is not None, ValueError, 'industry weight has not been given')
                return IndustryNeutralSelector(industry_weight=self.industry_weight)
            else:
                return BrutalSelector(nb_select=self.nb_select,
                                      prop_select=self.prop_select)
        else:
            return None
