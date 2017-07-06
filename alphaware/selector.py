# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import copy
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from sklearn_pandas import DataFrameMapper
from PyFin.Utilities import pyFinAssert
from argcheck import preprocess
from itertools import chain
from alphaware.preprocess import (ensure_factor_container,
                                  FactorTransformer)
from alphaware.enums import (FactorType,
                             SelectionMethod)
from alphaware.const import (INDEX_SELECTOR,
                             INDEX_FACTOR,
                             INDEX_INDUSTRY_WEIGHT)
from alphaware.utils import ensure_pd_series, top


class IndustryNeutralSelector(BaseEstimator, TransformerMixin):
    @preprocess(industry_weight=ensure_pd_series)
    def __init__(self, industry_weight, prop_select=0.1, min_select_per_industry=2, reset_index=False):
        self.industry_weight = industry_weight
        self.prop_select = prop_select
        self.min_select_per_industry = min_select_per_industry
        self.score = None
        self.industry_code = None
        self.reset_index = reset_index

    def fit(self, X, **kwargs):
        try:
            col_score = kwargs.get('col_score', 'score')
            col_industry_code = kwargs.get('col_score', 'industry_code')
            self.score = X[col_score]
            self.industry_code = X[col_industry_code]
        except KeyError:
            raise KeyError('Fail to retrieve data: please either use default col names or reset them')
        return self

    def transform(self, X):
        """
        :param X: pd.DataFrame
        :return: 
        """

        ret = pd.DataFrame()
        for name, group in X.groupby(self.industry_code.name):
            try:
                weight = self.industry_weight[name]
            except KeyError:
                continue
            if weight == 0:
                continue

            nb_select = int(max(len(group) * self.prop_select, min(self.min_select_per_industry, len(group))))
            largest_score = top(group, n=nb_select, column=self.score.name)
            weight_append = pd.DataFrame({INDEX_SELECTOR.col_name: [weight / nb_select] * nb_select,
                                          self.industry_code.name: [name] * nb_select},
                                         index=largest_score.index)

            ret = pd.concat([ret, pd.concat([largest_score[self.score.name], weight_append], axis=1)],
                            axis=0)

        return ret.reset_index() if self.reset_index else ret


class BrutalSelector(BaseEstimator, TransformerMixin):
    def __init__(self, nb_select=10, prop_select=0.1, reset_index=False):
        self.nb_select = nb_select
        self.prop_select = prop_select
        self.reset_index = reset_index

    def fit(self, X):
        return self

    @preprocess(X=ensure_pd_series)
    def transform(self, X):
        """
        :param X: pd.Series
        :return: 
        """

        ret = pd.DataFrame()
        nb_select = self.nb_select if self.nb_select is not None else int(len(X) * self.prop_select)
        largest_score = top(X, n=nb_select)
        weight = [100.0 / nb_select] * nb_select
        weight_append = pd.DataFrame({INDEX_SELECTOR.col_name: weight}, index=largest_score.index)
        weight_append = pd.concat([largest_score, weight_append], axis=1)
        ret = pd.concat([ret, weight_append], axis=0)

        return ret.reset_index() if self.reset_index else ret


class Selector(FactorTransformer):
    def __init__(self,
                 industry_weight=None,
                 method=SelectionMethod.INDUSTRY_NEUTRAL,
                 nb_select=10,
                 prop_select=0.1,
                 copy=True,
                 out_container=False,
                 **kwargs):
        super(Selector, self).__init__(copy=copy,out_container=out_container)
        self.method = method
        self.nb_select = nb_select
        self.prop_select = prop_select
        self.industry_weight = industry_weight
        self.min_select_per_industry = kwargs.get('min_select_per_industry', 2)

    def _build_mapper(self, factor_container):
        data_mapper_by_date = pd.Series()
        industry_code = factor_container.industry_code
        score = factor_container.score
        for date in factor_container.tiaocang_date:
            if self.method == SelectionMethod.INDUSTRY_NEUTRAL:
                pyFinAssert(self.industry_weight is not None, ValueError, 'industry weight has not been given')
                industry_weight = self.industry_weight.loc[date]
                data_mapper = [([score.name, industry_code.name],
                                IndustryNeutralSelector(industry_weight=industry_weight,
                                                        prop_select=self.prop_select,
                                                        min_select_per_industry=self.min_select_per_industry,
                                                        reset_index=True))]
            else:
                data_mapper = [(score.name, BrutalSelector(nb_select=self.nb_select,
                                                           prop_select=self.prop_select,
                                                           reset_index=True))]
            data_mapper_by_date[date] = DataFrameMapper(data_mapper, input_df=True, df_out=True)

        return data_mapper_by_date

    @preprocess(factor_container=ensure_factor_container)
    def transform(self, factor_container, **kwargs):
        if self.copy:
            factor_container = copy.deepcopy(factor_container)
        tiaocang_date = factor_container.tiaocang_date
        selector_data = [self.df_mapper[date_].fit_transform(factor_container.data.loc[date_]) for date_ in
                             tiaocang_date]
        date_list = [[tiaocang_date[i]] * len(selector_data[i]) for i in range(len(selector_data))]
        date_agg = list(chain.from_iterable(date_list))
        selector_data_ = np.vstack(selector_data)
        selector_data_agg = np.column_stack((date_agg, selector_data_))

        data_df = pd.DataFrame(selector_data_agg)
        data_df.columns = [INDEX_FACTOR.date_index,
                           INDEX_FACTOR.sec_index,
                           INDEX_FACTOR.col_score,
                           INDEX_INDUSTRY_WEIGHT.industry_index,
                           INDEX_SELECTOR.col_name]
        data_df.set_index([data_df.columns[0], data_df.columns[1]], inplace=True)

        factor_container.data = data_df
        if self.out_container:
            return factor_container
        else:
            return factor_container.data


if __name__ == "__main__":
    from unittest import TestCase
    from datetime import datetime as dt
    from parameterized import parameterized
    import pandas as pd
    from pandas.util.testing import assert_frame_equal
    from alphaware.selector import (BrutalSelector,
                                IndustryNeutralSelector,
                                Selector)
    from alphaware.enums import (FactorType,
                             SelectionMethod)
    from alphaware.preprocess import (Factor,
                                  FactorContainer)
    from alphaware.const import (INDEX_FACTOR,
                             INDEX_INDUSTRY_WEIGHT)


    index_weight = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['a', 'b', 'other']],
                                              names=INDEX_INDUSTRY_WEIGHT.full_index)
    industry_weight = pd.DataFrame([0.5, 0.4, 0.1, 0.5, 0.3, 0.2], index=index_weight)

    index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003', '004', '005']],
                                       names=INDEX_FACTOR.full_index)
    X = pd.DataFrame({'score': [2, 3, 3, 8, 4, 5, 9, 11, 2, 0],
                      'industry_code': ['a', 'a', 'a', 'b', 'b', 'a', 'a', 'other', 'b', 'b']},
                     index=index)

    score = Factor(data=X['score'], name='score', property_dict={'type': FactorType.SCORE})
    industry_code = Factor(data=X['industry_code'], name='industry_code',
                           property_dict={'type': FactorType.INDUSTY_CODE})
    fc = FactorContainer(start_date='2014-01-30', end_date='2014-02-28')
    fc.add_factor(score)
    fc.add_factor(industry_code)

    calculated = Selector(industry_weight=industry_weight,
                          method=SelectionMethod.INDUSTRY_NEUTRAL).fit_transform(fc)

    index_exp = pd.MultiIndex.from_arrays(
        [[dt(2014, 1, 30), dt(2014, 1, 30), dt(2014, 1, 30), dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 2, 28),
          dt(2014, 2, 28), dt(2014, 2, 28), dt(2014, 2, 28)],
         ['002', '003', '004', '005', '002', '001', '004', '005', '003']], names=['tradeDate', 'secID'])
    expected = pd.DataFrame({'score': [3, 3, 8, 4, 9, 5, 2, 0, 11],
                             'industry_code': ['a', 'a', 'b', 'b', 'a', 'a', 'b', 'b', 'other'],
                             'weight': [0.25, 0.25, 0.2, 0.2, 0.25, 0.25, 0.15, 0.15, 0.2]},
                            index=index_exp, dtype=object)
    print calculated

    expected = expected[['score', 'industry_code', 'weight']]
