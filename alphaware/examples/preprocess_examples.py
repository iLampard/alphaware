# -*- coding: utf-8 -*-

import pandas as pd
from WindAdapter import factor_load
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.enums import (NAStrategy,
                             FactorType,
                             FactorNormType)
from alphaware.preprocess import (FactorImputer,
                                  FactorNeutralizer)

# 提取原始因子数据(全市场股票的月频PB, 市值因子）
data_pb = factor_load('2014-01-01', '2014-03-10', 'PB', sec_id='fullA', is_index=True, save_file='pb.csv')
data_mv = factor_load('2014-01-01', '2014-03-10', 'MV', sec_id='fullA', is_index=True, save_file='mv.csv')

# data_pb = pd.read_csv('pb.csv', encoding='gbk')
# data_mv = pd.read_csv('mv.csv', encoding='gbk')
# data_pb['date'] = pd.to_datetime(data_pb['date'])
# data_mv['date'] = pd.to_datetime(data_mv['date'])
# data_pb.set_index(['date', ' secID'], inplace=True)
# data_mv.set_index(['date', ' secID'], inplace=True)

# 创建Factor实例，储存数据以及相关参数
factor_pb = Factor(data=data_pb, name='PB',
                   property_dict={'type': FactorType.ALPHA_FACTOR, 'norm_type': FactorNormType.Industry_Neutral})
factor_mv = Factor(data=data_mv, name='MV', property_dict={'type': FactorType.ALPHA_FACTOR_MV})

# 创建FactorContainer实例，加载所有的因子信息
fc = FactorContainer(start_date='2014-01-01', end_date='2014-03-10')
fc.add_factor(factor_pb)
fc.add_factor(factor_mv)

# 也可以一次性加载所有因子
# # fc = FactorContainer(start_date='2014-01-01', end_date='2014-03-10', factors=[factor_pb, factor_mv])
# print fc.tiaocang_date
# # [datetime.datetime(2014, 1, 30, 0, 0), datetime.datetime(2014, 2, 28, 0, 0)]
# print fc.alpha_factor_col
# # ['PB', 'MV']


# 提取行业数据
data_industry_code = factor_load('2014-01-01', '2014-03-10', 'SW_C1', sec_id='fullA', is_index=True, save_file='sw.csv')

# data_industry_code = pd.read_csv('sw.csv', encoding='gbk')
# data_industry_code['date'] = pd.to_datetime(data_industry_code['date'])
# data_industry_code.set_index(['date', ' secID'], inplace=True)
factor_industry_code = Factor(data=data_industry_code,
                              name='industry_code',
                              property_dict={'type': FactorType.INDUSTY_CODE})
fc.add_factor(factor_industry_code)

fc = FactorImputer(numerical_strategy=NAStrategy.MEDIAN,
                   categorical_strategy=NAStrategy.CUSTOM,
                   custom_value='other', out_container=True).fit_transform(fc)

fc_neu = FactorNeutralizer(out_container=True).fit_transform(fc)


