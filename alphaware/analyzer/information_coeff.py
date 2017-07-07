# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from scipy import stats
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
        result = pd.DataFrame()
        for fwd in factor_container.fwd_return_col:
            fwd_return = data_df[fwd]
            for alpha in factor_container.alpha_factor_col:
                alpha_factor = data_df[alpha]
                calc_data = [stats.spearmanr(fwd_return.loc[date_], alpha_factor.loc[date_])[0] for date_ in
                             tiaocang_date]
                result = pd.concat(
                    [result, pd.DataFrame(data=calc_data, index=tiaocang_date, columns=[alpha + '-' + fwd])], axis=1)

        return result



