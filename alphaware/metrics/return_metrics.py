# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from argcheck import (expect_types,
                      optional,
                      preprocess)
from ..enums import (FreqType,
                     FactorType,
                     OutputDataFormat)
from ..utils import (ensure_cumul_return,
                     ensure_noncumul_return,
                     ensure_pd_index_names,
                     group_by_freq,
                     fig_style)
from ..const import (SIMPLE_STAT_FUNCS,
                     FACTOR_STAT_FUNCS,
                     RETURN,
                     INDEX_RETURN,
                     INDEX_FACTOR)


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


@expect_types(ticker_return=pd.Series, weight=optional(pd.Series))
def calc_ptf_return(ticker_return, weight=None, cumul_return=True):
    """
    :param ticker_return: pd.DataFrame, multi-index, index=['trade_date', 'ticker']
    :param weight: optional, None. pd.DataFrame, multi-index, index=['trade_date', 'ticker']
    :param cumul_return: optional, True: cumul return, False: return non-cumul return
    :return: return weighted portfolio return
    """

    ticker_return_ = ensure_pd_index_names(ticker_return,
                                           data_format=OutputDataFormat.MULTI_INDEX_DF,
                                           valid_index=INDEX_FACTOR)
    if weight is not None:
        weight_ = ensure_pd_index_names(weight,
                                        data_format=OutputDataFormat.MULTI_INDEX_DF,
                                        valid_index=INDEX_FACTOR)
        ticker_return_ = pd.merge(ticker_return_, weight_, on=INDEX_FACTOR.full_index)
        weighted_return = ticker_return_[ticker_return.name] * ticker_return_[weight.name]
        ptf_return = weighted_return.groupby(INDEX_FACTOR.date_index).mean()
    else:
        ptf_return = ticker_return_.reset_index()
        ptf_return = ptf_return.groupby(INDEX_FACTOR.date_index).mean()
    if cumul_return:
        return ptf_return.apply(lambda x: 1 + x).cumprod()
    else:
        return ptf_return


@expect_types(unhedged_return=(RETURN, pd.Series), benchmark_return=(RETURN, pd.Series))
@preprocess(unhedged_return=ensure_cumul_return, benchmark_return=ensure_cumul_return)
def calc_alpha_return(unhedged_return, benchmark_return, rebalance_freq=FreqType.EOM):
    """
    :param unhedged_return:  RETURN namedtuple or pd.Series, 如果是 pd.Series则默认是cumul return
    :param benchmark_return: RETURN namedtuple or pd.Series, 如果是 pd.Series则默认是cumul return
    :param rebalance_freq: enum, FreqType
    :return:  pd.Series, 给定调仓频率的超额收益
    """

    merged_return = pd.concat([unhedged_return, benchmark_return], axis=1, join_axes=[unhedged_return.index])
    merged_return = pd.DataFrame(merged_return)
    merged_return.columns = [INDEX_RETURN.unhedged_return, INDEX_RETURN.benchmark_return]
    grouped_return = group_by_freq(merged_return, freq=rebalance_freq)

    base_return = merged_return.iloc[0]
    alpha_return = pd.Series()

    for name, group in grouped_return:
        # 计算超额收益 - 列
        excess_return = group[INDEX_RETURN.unhedged_return] / base_return[INDEX_RETURN.unhedged_return] \
                        - group[INDEX_RETURN.benchmark_return] / base_return[INDEX_RETURN.benchmark_return]
        # 检查是否要更新 基准收益
        base_nav = 1.0 if alpha_return.size == 0 else alpha_return.iloc[-1]
        base_return = group.iloc[-1]
        # 转换成累计收益，放入alpha_return的series
        alpha_return = alpha_return.append((1 + excess_return) * base_nav)
    alpha_return.name = INDEX_RETURN.hedged_return
    alpha_return.index.name = INDEX_RETURN.date_index
    return alpha_return


@expect_types(alpha_return=(RETURN, pd.Series), unhedged_return=(RETURN, pd.Series),
              benchmark_return=(RETURN, pd.Series))
def plot_alpha_return(alpha_return, unhedged_return, benchmark_return, **kwargs):
    """
    :param alpha_return: RETURN namedtuple or pd.Series, 如果是 pd.Series则默认是cumul return， 超额累计收益 
    :param unhedged_return:  同上，未对冲累计收益
    :param benchmark_return: 同上，标的累计收益
    :param kwargs: optional, 
                   save_file: bool, default=False, 是否要保存所有收益的数据 
    :return: 
    """
    data = pd.concat([alpha_return, unhedged_return, benchmark_return], axis=1, join_axes=[alpha_return.index])
    data = pd.DataFrame(data)
    # 如果缺失起始数据, 设置为1.0 （起始净值）
    data = data.fillna(1.0)
    data.columns = [u'策略对冲收益', u'策略未对冲收益', u'指数收益']
    ax = data.plot(figsize=(16, 6), title=u'策略收益演示图')
    fig_style(ax, [u'策略对冲净值', u'策略未对冲净值', u'指数收益'], x_label=u'交易日', y_label=u'净值',
              legend_loc='upper left')
    plt.show()

    save_file = kwargs.get('save_file', False)
    if save_file:
        data.to_csv('return_data.csv', date_format='%Y-%m-%d', encoding='gbk')

    return


@expect_types(strat_return=(pd.Series, RETURN), benchmark_return=optional(pd.Series))
@preprocess(strat_return=ensure_noncumul_return, benchmark_return=ensure_noncumul_return)
def _perf_stat(strat_return, benchmark_return=None, risk_free=0.0):
    """
    :param strat_return: pd.Series, daily non-cumul return of strategy 
    :param benchmark_return: pd.Series, daily non-cumul return of benchmark
    :param risk_free: float, risk free rate 
    :return: 
    """
    stat = pd.Series()

    for stat_func in SIMPLE_STAT_FUNCS.func:
        if stat_func.__name__ == 'sharpe_ratio':
            stat[stat_func.__name__] = stat_func(strat_return, risk_free)
        else:
            stat[stat_func.__name__] = stat_func(strat_return)

    if benchmark_return is not None:
        for stat_func in FACTOR_STAT_FUNCS.func:
            stat[stat_func.__name__] = stat_func(strat_return, benchmark_return, risk_free)

    return stat


@expect_types(strat_return=(pd.Series, RETURN))
@preprocess(strat_return=ensure_noncumul_return)
def group_perf_stat(strat_return, freq=FreqType.EOY, **kwargs):
    """
    :param strat_return: pd.Series, RETURN, 日频非累积收益率序列
    :param freq: enum, FreqType, default=EOY
    :param kwargs: optional, risk_free: float, risk free rate used in perf stat, default=0.0

    :return: 按照给定频率返回区间内收益序列的 年化收益，最大回撤，calmar比率，夏普比率，信息比率，beta，alpha等
    """
    risk_free = kwargs.get('risk_free', 0.0)
    group_return = group_by_freq(strat_return, freq=freq)
    stat = pd.DataFrame()
    for name, group in group_return:
        stat_ = _perf_stat(group[group.columns[0]], risk_free=risk_free)
        stat_.name = name
        stat = stat.append(stat_)

    return stat.dropna(axis=1).T
