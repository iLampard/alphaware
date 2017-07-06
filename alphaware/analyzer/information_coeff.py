# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from scipy import stats
from argcheck import expect_types
from alphaware.preprocess.factor_transformer import FactorTransformer
import copy


class FactorIC(FactorTransformer):
    def __init__(self, copy=True, out_container=False):
        super(FactorIC, self).__init__(copy=copy, out_container=out_container)

    def transform(self, factor_container):
        if self.copy:
            factor_container = copy.deepcopy(factor_container)
        data_df = factor_container.data
        tiaocang_date = factor_container.tiaocang_date
        alpha_factor = data_df[factor_container.alpha_factor_col]
        fwd_return = data_df[factor_container.fwd_return_col]
        calc_data = [stats.spearmanr(fwd_return[date_].values, alpha_factor.loc[date_].values) for date_ in
                     tiaocang_date]
        return pd.DataFrame(data=calc_data, index=tiaocang_date)


if __name__ == '__main__':
    from unittest import TestCase
    import pandas as pd
    import numpy as np
    from pandas.util.testing import assert_frame_equal
    from datetime import datetime as dt
    from alphaware.preprocess import (Factor,
                                      FactorContainer)
    from alphaware.enums import (FactorType,
                                 OutputDataFormat,
                                 FreqType,
                                 FactorNormType)

    index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28', '2014-03-31'], ['001', '002']],
                                       names=['tradeDate', 'secID'])
    data1 = pd.DataFrame(index=index, data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    factor_test1 = Factor(data=data1, name='test1')
    test2_property = {'type': FactorType.FWD_RETURN,
                      'data_format': OutputDataFormat.MULTI_INDEX_DF,
                      'norm_type': FactorNormType.Null,
                      'freq': FreqType.EOM}

    data2 = pd.DataFrame(index=index, data=[3.0, 2.0, 3.0, 7.0, 8.0, 9.0])
    factor_test2 = Factor(data=data2, name='test2',property_dict=test2_property)

    fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test1, factor_test2])
    t = FactorIC()
    print t.transform(fc)
