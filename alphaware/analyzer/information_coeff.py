# -*- coding: utf-8 -*-


import pandas as pd
from scipy import stats
from ..base import FactorEstimator
import copy


class FactorIC(FactorEstimator):
    def __init__(self):
        super(FactorIC, self).__init__()

    def estimate(self, factor_container):

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
                    [result, pd.DataFrame(data=calc_data, index=tiaocang_date, columns=[alpha + '_' + fwd])], axis=1)

        return result
