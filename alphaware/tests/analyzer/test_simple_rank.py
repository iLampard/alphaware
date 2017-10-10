# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
import numpy as np
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.analyzer import FactorSimpleRank
from pandas.util.testing import assert_series_equal
from datetime import datetime as dt


class TestFactorSimpleRank(TestCase):
    def test_factor_simple_rank_1(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003']],
                                           names=['trade_date', 'ticker'])
        data1 = pd.DataFrame(index=index, data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

        factor_test = Factor(data=data1, name='alpha1')
        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test])
        t = FactorSimpleRank()
        t.fit(fc)
        calculate = t.transform(fc)['score']
        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['001', '002', '003']],
                                           names=['trade_date', 'ticker'])

        expected = pd.Series(index=index,
                             data=[0.0, 1.0, 2.0, 0.0, 1.0, 2.0], name='score')
        assert_series_equal(calculate, expected)

    def test_factor_simple_rank_2(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003']],
                                           names=['trade_date', 'ticker'])
        data1 = pd.DataFrame(index=index, data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        data2 = pd.DataFrame(index=index, data=[7.0, 2.0, 3.0, 9.0, 5.0, 6.0])
        factor_test_1 = Factor(data=data1, name='alpha1')
        factor_test_2 = Factor(data=data2, name='alpha2')
        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test_1, factor_test_2])
        t = FactorSimpleRank(factor_name=['alpha2'], out_container=True)
        t.fit(fc)
        calculate = t.transform(fc).data['score']
        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['001', '002', '003']],
                                           names=['trade_date', 'ticker'])

        expected = pd.Series(index=index,
                             data=[1.0, 2.0, 0.0, 1.0, 2.0, 0.0], name='score')
        assert_series_equal(calculate, expected)
