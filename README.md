# alphaware
tools for alpha research

## Summary

*alphaware*提供了多因子研究的算法接口以及工具合集

*算法接口* 整体继承和模仿了scikit-learn
- 通过自定义的FactorContainer类，清理和存储原始因子数据以及属性特征等
- 提供了进行因子预处理、打分、筛选、计算IC等模块化运算的接口：接口的风格与scikit-learn的transformer/estimator类似，易于理解或者由用户自行拓展
- 继承了sklearn的流水线(pipeline)功能：用户可自行组合各个步骤，放入pipeline中流水线式执行

另外还提供了一些常用的工具函数
- 调仓日的计算（给定周期，起始日期，根据交易日日历来计算）
- 收益率的转换（累计与非累计），评价（各种比率）以及对冲收益率的计算、绘图等

## Quick Start
TODO
##### FactorContainer

##### FactorTransformer

##### FactorEstimator

##### AlphaPipeline

##### Utilities

- 调仓日计算： 默认的日历为天朝上交所交易日日历（引用自[Finance-Python](https://github.com/wegamekinglc/Finance-Python)），可根据起始日期，频率等计算调仓日期
    
``` python
from alphaware.utils import get_tiaocang_date
from alphaware.enums import FreqType

# 获取 2016-01-01 至 2016-3-31的月度调仓日
get_tiaocang_date(start_date='2016-01-01', end_date='2016-3-31', freq=FreqType.EOM)

# [datetime.datetime(2016, 1, 29, 0, 0), datetime.datetime(2016, 2, 29, 0, 0), datetime.datetime(2016, 3, 31, 0, 0)]

# 获取 2017-01-01 至 2017-2-1的周度调仓日
get_tiaocang_date(start_date='2017/1/1', end_date='2017/2/1', freq=FreqType.EOW, date_format='%Y/%m/%d')

# [datetime.datetime(2017, 1, 6, 0, 0), datetime.datetime(2017, 1, 13, 0, 0), datetime.datetime(2017, 1, 20, 0, 0),
#  datetime.datetime(2017, 1, 26, 0, 0)]
```

- 累积与非累积收益率快捷转换


``` python
import pandas as pd
from argcheck import preprocess
from alphaware.utils import (ensure_noncumul_return,
                             ensure_cumul_return)
from alphaware.const import RETURN
from alphaware.enums import ReturnType

# 定义一个累积收益率序列
ret = RETURN(data=pd.Series([1.0, 1.0, 1.05, 1.1],
                            index=['2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05']), type=ReturnType.Cumul)


# 假如要使用日频收益序列，只要结合argcheck.preprocess和ensure_noncumul_return即可
@preprocess(data=ensure_noncumul_return)
def mean_return(data):
    return data.mean()

mean_return(ret)
0.0325396825397
```

- 收益率测算工具函数

计算对冲收益率函数
``` python
@expect_types(unhedged_return=(RETURN, pd.Series), benchmark_return=(RETURN, pd.Series))
@preprocess(unhedged_return=ensure_cumul_return, benchmark_return=ensure_cumul_return)
def calc_alpha_return(unhedged_return, benchmark_return, rebalance_freq=FreqType.EOM):
    """
    :param unhedged_return:  RETURN namedtuple or pd.Series, 如果是 pd.Series则默认是cumul return
    :param benchmark_return: RETURN namedtuple or pd.Series, 如果是 pd.Series则默认是cumul return
    :param rebalance_freq: enum, FreqType
    :return:  pd.Series, 给定调仓频率的超额收益
    """
```

区间收益率评价函数合集
``` python
@expect_types(strat_return=(pd.Series, RETURN))
@preprocess(strat_return=ensure_noncumul_return)
def group_perf_stat(strat_return, freq=FreqType.EOY, **kwargs):
    """
    :param strat_return: pd.Series, RETURN, 日频非累积收益率序列
    :param freq: enum, FreqType, default=EOY
    :param kwargs: optional, risk_free: float, risk free rate used in perf stat, default=0.0

    :return: 按照给定频率返回区间内收益序列的 年化收益，最大回撤，calmar比率，夏普比率，信息比率，beta，alpha等
    """
```                                     
                                       
本节具体实现请见[utilities_example](/example/utils_funcs.py) 和[metrics单元测试](/tests/metrics/test_return_metrics.py)


## Requirement
``` python
numpy
pandas
finance-python
argcheck
empyrical
```


## Install

``` python
pip install alphaware
```
