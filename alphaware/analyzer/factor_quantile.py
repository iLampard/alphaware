# -*- coding: utf-8 -*-

import pandas as pd
from alphaware.base import FactorTransformer
import copy
from alphaware.utils import quantile_calc


class FactorQuantile(FactorTransformer):
    def __init__(self, copy=True,quantiles=5,bins=None,out_container=False):
        super(FactorQuantile, self).__init__(copy=copy, out_container=out_container)
        self.quantiles = quantiles
        self.bins = bins

    def _quantile_calc(self, score, fwd_return, tiaocang_date):
        for date_ in tiaocang_date:
            factor = pd.concat([score[date_], fwd_return[date_]], axis=1)





    def transform(self, factor_container):
        if self.copy:
            factor_container = copy.deepcopy(factor_container)
        data_df = factor_container.data
        tiaocang_date = factor_container.tiaocang_date
        result = pd.DataFrame()
        for fwd in factor_container.fwd_return_col:
            fwd_return = data_df[fwd]
            for alpha in factor_container.alpha_factor_col:
                alpha_factor = data_df[alpha]
                self._quantile_calc(alpha_factor,fwd_return,tiaocang_date)

                calc_data = [0 for date_ in tiaocang_date]
                result = pd.concat(
                    [result, pd.DataFrame(data=calc_data, index=tiaocang_date, columns=[alpha + '_' + fwd])], axis=1)

        return result


if __name__ == "__main__":
    import pandas as pd
    from alphaware.base import (Factor,
                                FactorContainer)
    from alphaware.enums import (FactorType,
                                 OutputDataFormat,
                                 FreqType,
                                 FactorNormType)

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
    t = FactorQuantile()
    calculate = t.transform(fc)
