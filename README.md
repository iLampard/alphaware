# alphaware
tools for alpha research

<table>

<tr>
  <td>Latest Release</td>
  <td><img src="https://img.shields.io/pypi/v/alphaware.svg" alt="latest release" /></td>
</tr>

<tr>
  <td>Python version</td>
  <td><img src="https://img.shields.io/badge/python-2.7-blue.svg"/>   <img src="https://img.shields.io/badge/python-3.5-blue.svg"/></td>
  </tr>

<tr>
  <td>Build Status</td>
  <td><img src="https://travis-ci.org/iLampard/alphaware.svg?branch=master" alt="build status" /></td>
</tr>
</table>


* [项目概况](https://github.com/ilampard/alphaware/blob/master/README.md#项目概况)
* [如何安装](https://github.com/ilampard/alphaware/blob/master/README.md#如何安装)
* [开始使用](https://github.com/ilampard/alphaware/blob/master/README.md#开始使用)
    * 核心类以及函数介绍
        * *Factor*：保存单个因子信息的类
        * *FactorContainer*： 保存所有因子信息的类 
        * *FactorTransformer*： 类似于scikit-learn的transformer
        * *FactorEstimator*： 类似于scikit-learn的estimator
        * *AlphaPipeline*： 类似于scikit-learn的pipeline
        * *date utilities*: 提供调仓日计算等功能
        * *metrics utilities*： 提供超额收益计算等功能
    * 示例一： 流程化计算因子IC
    * 示例二： 流程化因子选股
* [依赖库](https://github.com/ilampard/alphaware/blob/master/README.md#依赖库)
* [更多示例](https://github.com/ilampard/alphaware/blob/master/README.md#更多示例)
* [关于项目](https://github.com/ilampard/alphaware/blob/master/README.md#关于项目)

# 项目概况

*alphaware*提供了多因子研究的算法接口以及工具合集

*算法接口* 整体继承和模仿了scikit-learn
- 通过自定义的Factor/FactorContainer类，清理和存储原始因子数据以及属性特征等
- 提供了进行因子预处理、打分、筛选、计算IC等模块化运算的接口：接口的风格与scikit-learn的transformer/estimator类似，易于理解或者由用户自行拓展
- 继承了scikit-learn的流水线(pipeline)功能：用户可自行组合各个步骤，放入pipeline中流水线式执行

另外还提供了一些常用的工具函数
- 调仓日的计算（给定周期，起始日期，根据交易日日历来计算）
- 收益率的转换（累计与非累计），评价（各种比率）以及对冲收益率的计算、绘图等


# 如何安装

``` python
pip install alphaware
```

# 开始使用

### 核心类以及函数介绍

##### Factor

*Factor*类用以保存因子的三个相关信息： 数据(data)， 名称(name)和属性字典(property_dict)
- 数据是默认Multi-Index DataFrame格式， index是两列(date和secID)，因子值作为列
- 名称是赋予因子的名字，会作为作为数据的列名
- 属性字典保存了因子的属性
    * 本文提到因子实际上是广义的因子，所以需要进一步分别因子的类型，如alpha因子、行业代码、价格、当期收益、下期收益、因子得分等；还有比如进行中性化的方法，是使用行业中性还是行业市值中性。
    * 因子的类型、数据格式、中性化方法以及数据频率作为因子的必要属性，如果用户还有额外的属性也可以自定添加，最终形成一个属性字典储存在Factor实例中，具体可以见代码[Factor](https://github.com/iLampard/alphaware/blob/master/alphaware/base/factor_container.py)



``` python
from alphaware.base import Factor
from alphaware.enums import (OutputDataFormat,
                             FreqType,
                             FactorType,
                             FactorNormType)
                             
# 假设data_roe为提取好的因子数据，格式为Multi-Index DataFrame
# 把数据、名称、属性传入Factor类，创建实例
# porperty_dict有若干默认item，可覆盖也可以与自定义的item合并
factor_roe = Factor(data=data_roe, 
                    name='ROE', 
                    property_dict={'type': FactorType.ALPHA_FACTOR,
                                   'data_format': OutputDataFormat.MULTI_INDEX_DF,
                                   'norm_type': FactorNormType.Industry_Neutral,
                                   'freq': FreqType.EOM})



```

##### FactorContainer

*FactorContainer*是存储若干*Factor*实例的容器，其具体作用是
- 根据调仓日统一储存所有因子数据以及属性信息, 所有数据拼成一个若干列的Multi-Index DataFrame，方便后续处理
- 提供了各种成员函数，返回有用的信息：如某类alpha因子的名称、列名、数据
- 提供了*add_factor/remove_factor* 方法， 用以调整存储的Factor因子实例



``` python
from alphaware.base import FactorContainer

fc = FactorContainer(start_date='2010-01-01', end_date='2010-03-01')
fc.add_factor(factor_roe)
fc.remove_factor(factor_roe)

```

##### FactorTransformer

*FactorTransformer*的构造和使用类似于scikit-learn中的*transfomer*，主要包含三个方法
- fit: 训练算法，设置内部参数
- transform: 对因子数据进行转换(按_不同调仓日_分别转换，然后拼合结果)
- fit_transform: 合并fit和transform方法

*fit *和* transform*方法接受的入参为*FactorContainer*实例，返回类型可以是*FactorContainer*实例，也可以是纯因子数据(FactorContainer.data)

``` python
# 对FactorContainer携带的因子进行去极值化
quantile_range = (0.01, 0.99)
fc = FactorWinsorizer(quantile_range, out_container=True).fit_transform(fc)
fc_data = FactorWinsorizer(quantile_range, out_container=False).fit_transform(fc)
```        
        
已经实现的*FactorTransformer*有
``` python
FactorImputer       # 缺失数据填充（数值型和字符串型均可）
FactorNeutralizer   # 因子中性化
FactorStandardizer  # 因子标准化
FactorWinsorizer    # 因子去极值化
```
##### FactorEstimator
*FactorEstimator*的构造和使用类似于scikit-learn中的*estimator*，和*FactorTransformer*的区别在于有*predict*方法
- predict: 为了继承*pipeline*方便，此方法与scikit-learn中的*predict*方法同名
    * 实际中主要用于处理计算相关的问题，并且计算的结果无法再载入*FactorContainer*中，比如计算因子IC（结果不再是Multi-Index DataFrame)
    * 并不一定是实现’预测‘的功能


``` python
# 对FactorContainer携带的因子求IC系数
# 处理极个别N/A, 有中位数替换
fc = FactorImputer(numerical_strategy=NAStrategy.MEDIAN,
                   out_container=True).fit_transform(fc)

# 求因子IC系数
ic = FactorIC().predict(fc)
``` 
代码可参见[FactorIC_example](https://github.com/iLampard/alphaware/blob/master/alphaware/examples/ic_examples.py)

已经实现的*FactorEstimator*有
``` python
FactorQuantile      # 根据因子分组后对应组别的累计收益
FactorIC            # 求因子IC系数
Selector            # 根据得分选股（可选择是否按照行业比例挑选）
```


##### AlphaPipeline

*AlphaPipeline* 继承自scikit-learn的pipeline，用法与*pipeline*非常相似，可以将各个步骤流程化处理，如计算因子IC的例子可以改写成

``` python
# 第一步，处理极个别N/A, 有中位数替换
# 第二部，求因子IC系数
pipeline = AlphaPipeline([('imputer', FactorImputer(numerical_strategy=NAStrategy.MEDIAN)),
                         ('ic', FactorIC())])
ic = pipeline.fit_predict(fc)

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
                                       
*Utilities*函数具体实现请见[utilities_example](https://github.com/iLampard/alphaware/blob/master/alphaware/examples/utils_func.py) 和[metrics单元测试](https://github.com/iLampard/alphaware/blob/master/alphaware/tests/metrics/test_return_metrics.py)



### 示例一： 流程化计算因子IC

下面以流程化的计算因子IC的例子来说明*alphaware*的用法。

> 第一步，导入两个alpha因子，此处以[WindAdapter](https://github.com/iLampard/WindAdapter)作为数据源，用户也可以自定义其他数据源或者是从csv等数据文件中读取
``` python
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.enums import (FactorType,
                             FactorNormType,
                             NAStrategy)
from alphaware.utils import (fwd_return,
                             load_factor_data_from_csv)
from alphaware.analyzer import FactorIC
from alphaware.preprocess import (FactorNeutralizer,
                                  FactorStandardizer,
                                  FactorWinsorizer,
                                  FactorImputer)
from alphaware.pipeline import AlphaPipeline

# 加载MV和PB数据
# 利用WindAdapter提取
data_pb = factor_load('2014-01-01', '2014-03-10', 'PB', sec_id='fullA', is_index=True, save_file='pb.csv')
data_mv = factor_load('2014-01-01', '2014-03-10', 'MV', sec_id='fullA', is_index=True, save_file='mv.csv') / 100000000

# 如果是从csv文件导入的话，假设前两列为时间和股票代码，最后一列为因子数值
# data_mv = load_factor_data_from_csv('mv.csv') / 100000000
# data_pb = load_factor_data_from_csv('pb.csv')

# 创建Factor实例，储存数据以及相关参数
factor_pb = Factor(data=data_pb,
                   name='PB',
                   property_dict={'type': FactorType.ALPHA_FACTOR, 'norm_type': FactorNormType.Industry_Neutral})
factor_mv = Factor(data=data_mv,
                   name='MV',
                   property_dict={'type': FactorType.ALPHA_FACTOR_MV, 'norm_type': FactorNormType.Industry_Neutral})



```

> 第二步，以及月度收益数据以及行业代码
``` python

# 加载收益率数据
data_return = load_factor_data_from_csv('return.csv')
# 将数据改成未来1月收益
data_return = fwd_return(data_return)
factor_return = Factor(data=data_return, name='1_Fwd_Return', property_dict={'type': FactorType.FWD_RETURN})

# 加载行业数据(早年的wind的行业代码不太全，可能用其他数据源的数据更好，此处仅做示例用)
data_industry_code = factor_load('2014-01-01', '2014-03-01', 'SW_C1', sec_id='fullA', is_index=True,
                                 save_file='sw_test.csv')
factor_industry_code = Factor(data=data_industry_code,
                              name='industry_code',
                              property_dict={'type': FactorType.INDUSTY_CODE})

```


> 第三步，创建FactorContainer实例，设置好起始日期（或者调仓日期），加载所有的因子信息
``` python
fc = FactorContainer(start_date='2014-01-01',
                     end_date='2014-03-01',
                     factors=[factor_mv, factor_pb, factor_return, factor_industry_code])


# 也可以分步加载所有因子
# fc = FactorContainer(start_date='2014-01-01', end_date='2014-03-10', factors=[factor_pb, factor_mv])
# fc.add_factor(factor_mv)
# fc.add_factor(factor_pb)
# fc.add_factor(factor_return)
# fc.add_factor(factor_industry_code)

# 返回调仓日
fc.tiaocang_date
# [datetime.datetime(2014, 1, 30, 0, 0), datetime.datetime(2014, 2, 28, 0, 0)]

# 返回alpha因子的列名
fc.alpha_factor_col
# ['MV', 'PB']

```

> 第四步，对alpha因子进行缺失值填充以及去极值化、标准化、中性化
``` python

# 使用FactorImputer对缺失数据进行填充
# numerical_strategy=NAStrategy.MEDIAN: 对数字缺失使用中位数填充 
# categorical_strategy=NAStrategy.CUSTOM, custom_value='other': 对文字缺失使用自定义('other')进行填充
# out_container=True: 返回FactorContainer实例
fc = FactorImputer(numerical_strategy=NAStrategy.MEDIAN,
                   categorical_strategy=NAStrategy.CUSTOM,
                   custom_value='other', 
                   out_container=True).fit_transform(fc)
# 去极值化
fc = FactorWinsorizer(quantile_range=(5, 95), 
                      out_container=True).fit_transform(fc)

# 标准化
fc = FactorStandardizer(out_container=True).fit_transform(fc)
                   
# 中性化
# FactorNeutralizer会辨认出alpha因子以及对应的中性化方法（从因子属性property中），对每个alpha因子分别进行中性化处理
# 同时保持非alpha因子（如行业代码）不变
# 此处对MV和PB因子进行行业中性化，因为PB因子的property_dict={'norm_type'：FactorNormType.Industry_Neutral}
fc = FactorNeutralizer(out_container=True).fit_transform(fc)
```

> 第五步，计算因子IC 
```python
# FactorEstimator返回的是DataFrame
ic = FactorIC().predict(fc)
```

代码可参见[ic_windadapter](https://github.com/iLampard/alphaware/blob/master/alphaware/examples/ic_windadapter.py)

> 所有上面的步骤可以用AlphaPipeline流程化解决
```python
# pipeline
# 第一步，处理极个别N/A, 有中位数替换
step_1 = ('imputer', FactorImputer(numerical_strategy=NAStrategy.MEDIAN,
                                   categorical_strategy=NAStrategy.CUSTOM,
                                   custom_value='other'))
# 第二部，去极值化
step_2 = ('winsorize', FactorWinsorizer(quantile_range=(5, 95)))

# 第三步，标准化
step_3 = ('std', FactorStandardizer())

# 第四步，中性化
step_4 = ('neutralize', FactorNeutralizer())

# 第五步，求因子IC
step_5 = ('ic', FactorIC())

pipeline = AlphaPipeline([step_1, step_2, step_3, step_4, step_5])
ic = pipeline.fit_predict(fc)

# result
            MV_1_Fwd_Return  PB_1_Fwd_Return
2014-01-30        -0.235823        -0.108877
2014-02-28        -0.092717        -0.204371
```
代码可参见[ic_pipeline](https://github.com/iLampard/alphaware/blob/master/alphaware/examples/ic_pipeline.py)


### 示例二: 流程化因子选股

本例说明如何使用*alphaware*进行因子选股

加载市值和PB因子和示例一中的步骤完全一致，此时直接使用pipeline
- 此处使用最简单的选股策略，仅作为示例用
- 用户可自行定义RankTransformer实现复杂的选股模型，只要从基类FactorTransfomer继承即可

```python
# 第一步，处理极个别N/A, 有中位数替换
step_1 = ('imputer', FactorImputer(numerical_strategy=NAStrategy.MEDIAN,
                                   categorical_strategy=NAStrategy.CUSTOM,
                                   custom_value='other'))
# 第二部，去极值化
step_2 = ('winsorize', FactorWinsorizer(quantile_range=(0.05, 0.95)))

# 第三步，标准化
step_3 = ('std', FactorStandardizer())

# 第四步，中性化
step_4 = ('neutralize', FactorNeutralizer())


# 第五步，按照因子排序打分，使用最简单的方法 - 等权求和
# 市值越小分数越高，PB越小分数越高
step_5 = ('rank', FactorSimpleRank(ascend_order=[-1, -1], out_container=True))

# 第六步，行业中性选股，选取每个行业的前10%
# 要读取一个行业权重比例的数据
industry_weight = load_factor_data_from_csv('industry_weight.csv')
step_6 = ('select', Selector(industry_weight=industry_weight, method=SelectionMethod.INDUSTRY_NEUTRAL))

pipeline = AlphaPipeline([step_1, step_2, step_3, step_4, step_5, step_6])
ptf = pipeline.fit_predict(fc)

# result
                       score industry_code    weight
date       secID                                    
2014-01-30 002696.SZ  2433.5     801010.SI  0.331429
           000798.SZ  2416.5     801010.SI  0.331429
           000911.SZ    2337     801010.SI  0.331429
           002567.SZ  2079.5     801010.SI  0.331429
           300119.SZ    2048     801010.SI  0.331429
           300106.SZ  2045.5     801010.SI  0.331429
           002688.SZ  2037.5     801010.SI  0.331429
           601808.SH  2118.5     801020.SI     0.288
           300084.SZ    2038     801020.SI     0.288
           601918.SH    2036     801020.SI     0.288
           601898.SH  1940.5     801020.SI     0.288
           000933.SZ    1905     801020.SI     0.288
           300121.SZ    2480     801030.SI  0.333913
```
代码可参见[selector_pipeline](https://github.com/iLampard/alphaware/blob/master/alphaware/examples/selector_pipeline.py)

# 依赖库
``` python
numpy
pandas
finance-python
argcheck
empyrical
```

# 更多示例

* 请参考[examples folder](https://github.com/iLampard/alphaware/tree/master/alphaware/examples)

# 关于项目

* 欢迎大家使用及提出意见