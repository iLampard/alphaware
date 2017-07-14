# alphaware
tools for alpha research

## Summary

*alphaware*提供了多因子研究的算法接口以及工具合集

*算法接口* 整体继承和模仿了scikit-learn
- 通过自定义的Factor/FactorContainer类，清理和存储原始因子数据以及属性特征等
- 提供了进行因子预处理、打分、筛选、计算IC等模块化运算的接口：接口的风格与scikit-learn的transformer/estimator类似，易于理解或者由用户自行拓展
- 继承了sklearn的流水线(pipeline)功能：用户可自行组合各个步骤，放入pipeline中流水线式执行

另外还提供了一些常用的工具函数
- 调仓日的计算（给定周期，起始日期，根据交易日日历来计算）
- 收益率的转换（累计与非累计），评价（各种比率）以及对冲收益率的计算、绘图等

## Quick Start

##### Factor

*Factor*类用以保存因子的三个相关信息： 数据(data)， 名称(name)和属性字典(property_dict)
- 数据是默认Multi-Index DataFrame格式， index是两列(date和secID)，因子值作为列
- 名称是赋予因子的名字，会作为作为数据的列名
- 属性字典保存了因子的属性
    * 本文提到因子实际上是广义的因子，所以需要进一步分别因子的类型，如alpha因子、行业代码、价格、当期收益、下期收益、因子得分等；还有比如进行中性化的方法，是使用行业中性还是行业市值中性。
    * 因子的类型、数据格式、中性化方法以及数据频率作为因子的必要属性，如果用户还有额外的属性也可以自定添加，最终形成一个属性字典储存在Factor实例中，具体可以见代码[Factor](https://github.com/iLampard/alphaware/blob/master/alphaware/base/factor_container.py)

##### FactorContainer

*FactorContainer*是存储若干*Factor*实例的容器，其具体作用是
- 根据调仓日统一储存所有因子数据以及属性信息, 所有数据拼成一个若干列的Multi-Index DataFrame，方便后续处理
- 提供了各种成员函数，返回有用的信息：如某类alpha因子的名称、列名、数据
- 提供了*add_factor/remove_factor* 方法， 用以调整存储的Factor因子实例

##### FactorTransformer

*FactorTransformer*的构造和使用类似于scikit-learn中的*transfomer*，主要包含三个方法
- fit: 训练算法，设置内部参数
- transform: 对因子数据进行转换(按_不同调仓日_分别转换，然后拼合结果)
- fit_transform: 合并fit和transform方法

*fit *和*transform*方法接受的入参为*FactorContainer*实例，返回类型可以是*FactorContainer*实例，也可以是纯因子数据(FactorContainer.data)

##### FactorEstimator
*FactorEstimator*的构造和使用类似于scikit-learn中的*estimator*，和*FactorTransformer*的区别
- fit: 训练算法，设置内部参数
- estimate: 对因子数据进行转换(按_不同调仓日_分别转换，然后拼合结果)


##### AlphaPipeline
TODO

下面以一些例子来说明*alphaware*中这几个类的用法。

> 第一步，导入两个alpha因子的数据，此处以[WindAdapter](https://github.com/iLampard/WindAdapter)作为数据源，用户也可以自定义其他数据源或者是从csv等数据文件中读取
``` python
import pandas as pd
from WindAdapter import factor_load
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.enums import FactorType

# 提取原始因子数据(全市场股票的月频PB, 市值因子）
data_pb = factor_load('2014-01-01', '2014-03-10', 'PB', sec_id='fullA', is_index=True, save_file='pb.csv')
data_mv = factor_load('2014-01-01', '2014-03-10', 'MV', sec_id='fullA', is_index=True, save_file='mv.csv')

# 如果是从csv文件导入的话，假设前两列为时间和股票代码，最后一列为因子数值
# data_pb = pd.read_csv('pb.csv', encoding='gbk')
# data_mv = pd.read_csv('mv.csv', encoding='gbk')
# data_pb['date'] = pd.to_datetime(data_pb['date'])
# data_mv['date'] = pd.to_datetime(data_mv['date'])
# data_pb.set_index(['date', ' secID'], inplace=True)
# data_mv.set_index(['date', ' secID'], inplace=True)
```

> 第二步，把提取的因子数据以及性质保存在Factor实例中
``` python
# 创建Factor实例，储存数据以及相关参数
factor_pb = Factor(data=data_pb, name='PB', property_dict={'type': FactorType.ALPHA_FACTOR, 'norm_type': FactorNormType.Industry_Neutral})
factor_mv = Factor(data=data_mv, name='MV', property_dict={'type': FactorType.ALPHA_FACTOR_MV})

```


> 第三步，创建FactorContainer实例，设置好起始日期（或者调仓日期），加载所有的因子信息
``` python
# 创建FactorContainer实例，加载Factor
fc = FactorContainer(start_date='2014-01-01', end_date='2014-03-10')
fc.add_factor(factor_pb)
fc.add_factor(factor_mv)

# 也可以一次性加载所有因子
# fc = FactorContainer(start_date='2014-01-01', end_date='2014-03-10', factors=[factor_pb, factor_mv])

# 返回调仓日
fc.tiaocang_date
# [datetime.datetime(2014, 1, 30, 0, 0), datetime.datetime(2014, 2, 28, 0, 0)]

# 返回alpha因子的列名
fc.alpha_factor_col
# ['PB', 'MV']

```

> 第四步，再次加载行业信息，然后对alpha因子进行缺失值填充和中性化处理(去极值化和标准化类似)
``` python
# 提取行业数据
data_industry_code = factor_load('2014-01-01', '2014-03-10', 'SW_C1', sec_id='fullA', is_index=True, save_file='sw.csv')

# 加载进FactorContainer
factor_industry_code = Factor(data=data_industry_code, name='industry_code',
                              property_dict={'type': FactorType.INDUSTY_CODE})
fc.add_factor(factor_industry_code)

# 使用FactorImputer对缺失数据进行填充
# numerical_strategy=NAStrategy.MEDIAN: 对数字缺失使用中位数填充 
# categorical_strategy=NAStrategy.CUSTOM, custom_value='other': 对文字缺失使用自定义('other')进行填充
# out_container=True: 返回FactorContainer实例
fc = FactorImputer(numerical_strategy=NAStrategy.MEDIAN,
                   categorical_strategy=NAStrategy.CUSTOM,
                   custom_value='other', 
                   out_container=True).fit_transform(fc)
                   
# 使用FactorNeutralizer对alpha因子进行中性化处理
# FactorNeutralizer会辨认出alpha因子以及对应的中性化方法（从因子属性property中），对每个alpha因子分别进行中性化处理
# 同时保持非alpha因子（如行业代码）不变
# 此处对PB因子进行市值和行业中性化，因为PB因子的property_dict={'norm_type'：FactorNormType.Industry_Neutral}
# MV因子不做变化，因为MV因子的'norm_type'取默认值Null
fc = FactorNeutralizer(out_container=True).fit_transform(fc)

```



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
