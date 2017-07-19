# -*- coding: utf-8 -*-

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
data_mv = load_factor_data_from_csv('mv.csv') / 100000000
data_pb = load_factor_data_from_csv('pb.csv')

# 创建Factor实例，储存数据以及相关参数
factor_pb = Factor(data=data_pb,
                   name='PB',
                   property_dict={'type': FactorType.ALPHA_FACTOR, 'norm_type': FactorNormType.Industry_Neutral})
factor_mv = Factor(data=data_mv,
                   name='MV',
                   property_dict={'type': FactorType.ALPHA_FACTOR_MV, 'norm_type': FactorNormType.Industry_Neutral})

# 加载行业数据
# 此csv数据最早是用WindAdapter从wind读取，早年的wind的行业代码不太全，可能用其他数据源的数据更好，此处仅做示例用
data_industry_code = load_factor_data_from_csv('sw.csv')
factor_industry_code = Factor(data=data_industry_code,
                              name='industry_code',
                              property_dict={'type': FactorType.INDUSTY_CODE})

# 加载月度收益数据
data_return = load_factor_data_from_csv('return.csv')
# 将数据改成未来1月收益
data_return = fwd_return(data_return)
factor_return = Factor(data=data_return,
                       name='1_Fwd_Return',
                       property_dict={'type': FactorType.FWD_RETURN, 'norm_type': FactorNormType.Industry_Neutral})

# 创建FactorContainer实例，加载所有的因子信息
fc = FactorContainer(start_date='2014-01-01',
                     end_date='2014-03-10',
                     factors=[factor_mv, factor_pb, factor_return, factor_industry_code])

# pipeline
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

# 第五步，求因子IC
step_5 = ('ic', FactorIC())

pipeline = AlphaPipeline([step_1, step_2, step_3, step_4, step_5])
ic = pipeline.fit_predict(fc)

print ic
