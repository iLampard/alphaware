# -*- coding: utf-8 -*-


from WindAdapter import factor_load

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

# 加载MV和PB数据
data_pb = factor_load('2014-01-01', '2014-03-01', 'PB', sec_id='fullA', is_index=True, save_file='pb_test.csv')
data_mv = factor_load('2014-01-01', '2014-03-01', 'MV', sec_id='fullA', is_index=True,
                      save_file='mv_test.csv') / 100000000

# 创建Factor实例，储存数据以及相关参数
factor_pb = Factor(data=data_pb,
                   name='PB',
                   property_dict={'type': FactorType.ALPHA_FACTOR, 'norm_type': FactorNormType.Industry_Neutral})
factor_mv = Factor(data=data_mv,
                   name='MV',
                   property_dict={'type': FactorType.ALPHA_FACTOR_MV, 'norm_type': FactorNormType.Industry_Neutral})

# 加载月度收益数据
data_return = factor_load('2014-01-01', '2014-03-31', 'return', sec_id='fullA', is_index=True,
                          save_file='return_test.csv')
# 将数据改成未来1月收益
data_return = fwd_return(data_return)
factor_return = Factor(data=data_return, name='1_Fwd_Return', property_dict={'type': FactorType.FWD_RETURN})

# 加载行业数据(早年的wind的行业代码不太全，可能用其他数据源的数据更好，此处仅做示例用)
data_industry_code = factor_load('2014-01-01', '2014-03-01', 'SW_C1', sec_id='fullA', is_index=True,
                                 save_file='sw_test.csv')
factor_industry_code = Factor(data=data_industry_code,
                              name='industry_code',
                              property_dict={'type': FactorType.INDUSTY_CODE})

# 创建FactorContainer实例，加载所有的因子信息
fc = FactorContainer(start_date='2014-01-01',
                     end_date='2014-03-01',
                     factors=[factor_mv, factor_pb, factor_return, factor_industry_code])


print fc.alpha_factor_col

# 第一步，处理极个别N/A, 有中位数替换
fc = FactorImputer(numerical_strategy=NAStrategy.MEDIAN,
                   categorical_strategy=NAStrategy.CUSTOM,
                   custom_value='other',
                   out_container=True).fit_transform(fc)


# 第二部，去极值化
fc = FactorWinsorizer(quantile_range=(5, 95),
                      out_container=True).fit_transform(fc)

# 第三步，标准化
fc = FactorStandardizer(out_container=True).fit_transform(fc)

# 第四步，中性化
fc = FactorNeutralizer(out_container=True).fit_transform(fc)

# 第五步，求因子IC
ic = FactorIC().predict(fc)
print ic
