# -*- coding: utf-8 -*-

import pandas as pd
from ..base import FactorTransformer
import copy


class FactorQuantile(FactorTransformer):
    def __init__(self, copy=True, out_container=False):
        super(FactorQuantile, self).__init__(copy=copy, out_container=out_container)

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
                #TODO
                calc_data = [0 for date_ in tiaocang_date]
                result = pd.concat(
                    [result, pd.DataFrame(data=calc_data, index=tiaocang_date, columns=[alpha + '_' + fwd])], axis=1)

        return result
