# -*- coding: utf-8 -*-

import os
from unittest import TestCase
import pandas as pd
from pandas.util.testing import (assert_series_equal,
                                 assert_frame_equal)
from alphaware.metrics import (calc_ptf_return,
                               calc_alpha_return,
                               group_perf_stat)
from alphaware.const import (INDEX_RETURN,
                             RETURN)
from alphaware.enums import (FreqType,
                             ReturnType)


class TestReturnMetrics(TestCase):
    def setUp(self):
        dir_name = os.path.dirname(os.path.abspath(__file__))
        return_data = pd.read_csv(dir_name + '//data//performance.csv')
        return_data.columns = ['trade_date', 'benchmark', 'strategy']
        return_data['trade_date'] = pd.to_datetime(return_data['trade_date'], format='%Y/%m/%d')
        return_data.set_index('trade_date', inplace=True)

        self.strategy = RETURN(data=return_data['strategy'], type=ReturnType.Cumul)
        self.benchmark = RETURN(data=return_data['benchmark'], type=ReturnType.Cumul)

        result = pd.read_csv(dir_name + "//data//result.csv")
        result.columns = ['trade_date', 'result1', 'result2', 'result3']
        result['trade_date'] = pd.to_datetime(result['trade_date'], format='%Y/%m/%d')
        result.set_index('trade_date', inplace=True)
        self.result = result

    def test_calc_ptf_return(self):
        index = pd.MultiIndex.from_product([['2014-02-27', '2014-02-28'], ['001', '002']],
                                           names=['trade_date', 'ticker'])
        ticker_return = pd.Series([0.05, 0.06, 0.08, 0.08], index=index, name='return')

        calculated = calc_ptf_return(ticker_return=ticker_return)
        expected = pd.DataFrame({'return': [1.055, 1.1394]},
                                index=pd.Index(['2014-02-27', '2014-02-28'], name='trade_date'))
        assert_frame_equal(calculated, expected)

    def test_calc_alpha_return(self):
        calculated = calc_alpha_return(unhedged_return=self.strategy,
                                       benchmark_return=self.benchmark,
                                       rebalance_freq=FreqType.EOM)
        expected = self.result['result1']
        expected.name = INDEX_RETURN.hedged_return
        assert_series_equal(calculated, expected)

    def test_group_perf_stat(self):
        calculated = group_perf_stat(self.strategy, risk_free=0.02, freq=FreqType.EOQ)
        expected = pd.DataFrame(
            data=[[-0.194346, -0.391711, 0.439566, -0.126527], [-1.313148, -2.160582, 3.146201, -1.187699],
                  [-0.148000, -0.181299, -0.139713, -0.106531], [-24.203418, -18.283650, -16.019707, -25.555582]],
            index=['annual_return', 'calmar_ratio', 'max_drawdown', 'sharpe_ratio'],
            columns=pd.DatetimeIndex(['2005-03-31', '2005-06-30', '2005-09-30', '2005-12-31'], dtype='datetime64[ns]',
                                     freq=None))
        assert_frame_equal(calculated, expected)
        calculated = group_perf_stat(self.strategy, risk_free=0.04, freq=FreqType.EOY)
        expected = pd.DataFrame(data=[-0.101456, -0.295517, -0.343317, -39.591727],
                                index=['annual_return', 'calmar_ratio', 'max_drawdown', 'sharpe_ratio'],
                                columns=pd.DatetimeIndex(['2005-12-31'], dtype='datetime64[ns]', freq=None))
        assert_frame_equal(calculated, expected)
