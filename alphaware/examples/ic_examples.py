# -*- coding: utf-8 -*-

import pandas as pd
# from WindAdapter import factor_load
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.enums import FactorType
from alphaware.utils import (fwd_return,
                             load_factor_data_from_csv)
from alphaware.analyzer import FactorIC

# 加载MV数据
# data_mv = factor_load('2014-01-01', '2014-02-28', 'MV', sec_id='fullA', is_index=True, save_file='mv.csv')
data_mv = load_factor_data_from_csv('mv.csv')
factor_mv = Factor(data=data_mv, name='MV', property_dict={'type': FactorType.ALPHA_FACTOR_MV})

# 加载月度收益数据
# data_return = factor_load('2014-01-01', '2014-03-31', 'return', sec_id='fullA', is_index=True, freq='M',
# save_file='return.csv')
data_return = load_factor_data_from_csv('return.csv')
# 将数据改成未来1月收益
data_return = fwd_return(data_return)
factor_return = Factor(data=data_return, name='1_Fwd_Return', property_dict={'type': FactorType.FWD_RETURN})

# 创建FactorContainer实例，加载所有的因子信息
fc = FactorContainer(start_date='2014-01-01', end_date='2014-03-10', factors=[factor_mv, factor_return])
print fc.data

# 求因子IC系数
ic = FactorIC().predict(fc)
print ic

