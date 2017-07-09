# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.enums import (FactorType,
                             OutputDataFormat,
                             FreqType,
                             FactorNormType)
from alphaware.analyzer import FactorIC
from pandas.util.testing import assert_frame_equal


class TestFactorIC(TestCase):
    def test_factor_ic(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28', '2014-03-31'], ['001', '002']],
                                           names=['tradeDate', 'secID'])
        data1 = pd.DataFrame(index=index, data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        factor_test1 = Factor(data=data1, name='alpha1')
        factor_test3 = Factor(data=data1, name='alpha2')
        test2_property = {'type': FactorType.FWD_RETURN,
                          'data_format': OutputDataFormat.MULTI_INDEX_DF,
                          'norm_type': FactorNormType.Null,
                          'freq': FreqType.EOM}

        data2 = pd.DataFrame(index=index, data=[3.0, 2.0, 3.0, 7.0, 8.0, 9.0])
        factor_test2 = Factor(data=data2, name='fwd_return1', property_dict=test2_property)
        factor_test4 = Factor(data=data2, name='fwd_return2', property_dict=test2_property)

        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test1, factor_test2, factor_test3, factor_test4])
        t = FactorIC()
        calculate = t.transform(fc)
        expected = pd.DataFrame(data=[[-1.0, -1.0, -1.0, -1.0], [1.0, 1.0, 1.0, 1.0]],
                                index=pd.DatetimeIndex(['2014-01-30', '2014-02-28'], freq=None),
                                columns=['alpha1_fwd_return1', 'alpha2_fwd_return1', 'alpha1_fwd_return2',
                                         'alpha2_fwd_return2'])
        assert_frame_equal(calculate, expected)
