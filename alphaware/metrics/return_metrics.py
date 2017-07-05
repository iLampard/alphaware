# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from argcheck import (expect_types,
                      optional,
                      preprocess)
from ..enums import (FreqType)
from ..utils import (ensure_cumul_return,
                     ensure_noncumul_return,
                     group_by_freq,
                     fig_style)
from ..const import (SIMPLE_STAT_FUNCS,
                     FACTOR_STAT_FUNCS,
                     RETURN)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


@expect_types(unhedged_return=(RETURN, pd.Series), benchmark_return=(RETURN, pd.Series))
@preprocess(unhedged_return=ensure_cumul_return, benchmark_return=ensure_cumul_return)
def calc_alpha_return(unhedged_return, benchmark_return, rebalance_freq=FreqType.EOM):
    """
    :param unhedged_return:  RETURN namedtuple or pd.Series, 如果是 pd.Series则默认是cumul return
    :param benchmark_return: RETURN namedtuple or pd.Series, 如果是 pd.Series则默认是cumul return
    :param rebalance_freq: enum, FreqType
    :return:  pd.Series, 给定调仓频率的超额收益
    """

    merged_return = unhedged_return.join(benchmark_return, how='left')
    merged_return.columns = ['unhedged_return', 'benchmark_return']
    grouped_return = group_by_freq(merged_return, freq=rebalance_freq)

    base_return = merged_return.iloc[0]
    alpha_return = pd.Series()
    for name, group in grouped_return:
        # 计算超额收益 - 列
        excess_return = group['unhedged_return'] / base_return['unhedged_return'] \
                        - group['benchmark_return'] / base_return['benchmark_return']
        # 转换成累计收益
        base_nav = 1.0 if alpha_return.iloc[-1] is None else alpha_return.iloc[-1]
        alpha_return_append = (1 + excess_return) * base_nav
        # 放入alpha_return的series
        alpha_return.append(alpha_return_append)
    return alpha_return
