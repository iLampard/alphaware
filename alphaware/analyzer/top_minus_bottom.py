# -*- coding: utf-8 -*-

import pandas as pd
from alphaware.base import FactorEstimator


class TopMinusBottom(FactorEstimator):
    def __init__(self, quantiles=5):
        super(TopMinusBottom, self).__init__()
        self.quantiles = quantiles

    def _top_minus_bottom_calc(self, score, fwd_return, tiaocang_date):
        result = pd.DataFrame()
        for date_ in tiaocang_date:
            factor = pd.DataFrame(pd.concat([score[date_], fwd_return[date_]], axis=1))
            factor.sort_values(by=score.name, inplace=True)
            result_top_minus_bottom = {}
            result_top_minus_bottom[score.name + '_' + fwd_return.name] = factor[fwd_return.name][int(
                self.quantiles - 1 * len(factor) / self.quantiles):].mean() - factor[fwd_return.name][
                                                                              :int(len(factor) / self.quantiles)].mean()
            result = pd.concat([result, pd.DataFrame(result_top_minus_bottom, index=[date_])], axis=0)
        return result

    def predict(self, factor_container):
        data_df = factor_container.data
        tiaocang_date = factor_container.tiaocang_date
        result = pd.DataFrame()
        for fwd in factor_container.fwd_return_col:
            fwd_return = data_df[fwd]
            for alpha in factor_container.alpha_factor_col:
                alpha_factor = data_df[alpha]
                calc_data = self._top_minus_bottom_calc(alpha_factor, fwd_return, tiaocang_date)
                result = pd.concat([result, calc_data], axis=1)

        return result
