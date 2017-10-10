# -*- coding: utf-8 -*-


from unittest import TestCase
import pandas as pd
import numpy as np
from pandas.util.testing import assert_series_equal
from datetime import datetime as dt
from ...preprocess import Benchmark
from ...enums import (FactorType,
                      OutputDataFormat,
                      FreqType,
                      FactorNormType)


class TestBenchmark(TestCase):
    def test_benchmark(self):
        index_industry = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28', '2014-03-31'], ['a', 'b']],
                                                    names=['trade_date', 'ticker'])
        industry_weight = pd.DataFrame(index=index_industry, data=[0.1, 0.2, 0.3, 0.2, 0.3, 0.3])

        index_return = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28', '2014-03-31'], ['001', '002']],
                                                  names=['trade_date', 'ticker'])
        hist_return = pd.DataFrame(index=index_return, data=[0.1, 0.05, 0.05, -0.05, 0.05, 0.06])
        benchmark = Benchmark(name='test', industry_weight=industry_weight, hist_return=hist_return)

        calculated = benchmark.get_industry_weight_on_date('2014-01-30')
        expected = pd.Series([0.1, 0.2, 99.7], index=pd.Index(['a', 'b', 'other'], name='industry_code'), name='weight')
        assert_series_equal(calculated, expected)
