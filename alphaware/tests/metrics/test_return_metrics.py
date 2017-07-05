# -*- coding: utf-8 -*-

import os
from unittest import TestCase
import pandas as pd
from pandas.util.testing import (assert_series_equal,
                                 assert_frame_equal)
from alphaware.metrics import (calc_alpha_return,
                               group_perf_stat)
from alphaware.const import (INDEX_RETURN,
                             RETURN)
from alphaware.enums import (FreqType,
                             ReturnType)


class TestReturnMetrics(TestCase):
    def setUp(self):
        dir_name = os.path.dirname(os.path.abspath(__file__))
        return_data = pd.read_csv(dir_name + '//data//performance.csv')
        return_data.columns = ['tradeDate', 'benchmark', 'strategy']
        return_data['tradeDate'] = pd.to_datetime(return_data['tradeDate'], format='%Y/%m/%d')
        return_data.set_index('tradeDate', inplace=True)

        self.strategy = RETURN(data=return_data['strategy'], type=ReturnType.Cumul)
        self.benchmark = RETURN(data=return_data['benchmark'], type=ReturnType.Cumul)

        result = pd.read_csv(dir_name + "//data//result.csv")
        result.columns = ['tradeDate', 'result1', 'result2', 'result3']
        result['tradeDate'] = pd.to_datetime(result['tradeDate'], format='%Y/%m/%d')
        result.set_index('tradeDate', inplace=True)
        self.result = result

    def test_calc_alpha_return(self):
        calculated = calc_alpha_return(unhedged_return=self.strategy,
                                       benchmark_return=self.benchmark,
                                       rebalance_freq=FreqType.EOM)
        expected = self.result['result1']
        expected.name = INDEX_RETURN.hedged_return
        assert_series_equal(calculated, expected)

    def test_group_perf_stat(self):
        calculated = group_perf_stat(self.strategy, risk_free=0.02, freq=FreqType.EOQ)
        print calculated
        #assert_frame_equal(calculated, expected)
