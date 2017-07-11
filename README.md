# alphaware
tools for alpha research

## Summary

*alphaware*提供了多因子研究的算法接口以及工具合集

*算法接口*整体继承和模仿了scikit-learn
- 通过自定义的FactorContainer类，清理和存储原始因子数据以及属性特征等
- 提供了进行因子预处理、打分、筛选、计算IC等模块化运算的接口：接口的风格与scikit-learn的transformer/estimator类似，易于理解或者由用户自行拓展
- 继承了sklearn的流水线(pipeline)功能：用户可自行组合各个步骤，放入pipeline中流水线式执行

另外还提供了一些常用的工具函数
- 调仓日的计算（给定周期，起始日期，根据交易日日历来计算）
- 收益率的转换（累计与非累计），评价（各种比率）以及对冲收益率的计算、绘图等

## Quick Start
TODO 





## Requirement
``` python
numpy
pandas
finance-python
```


## Install

``` python
pip install alphaware
```
