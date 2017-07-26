# -*- coding: utf-8 -*-

from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.enums import (FactorType,
                             FactorNormType,
                             NAStrategy,
                             SelectionMethod)
from alphaware.utils import (fwd_return,
                             load_factor_data_from_csv)
from alphaware.analyzer import FactorSimpleRank
from alphaware.preprocess import (FactorNeutralizer,
                                  FactorStandardizer,
                                  FactorWinsorizer,
                                  FactorImputer)
from alphaware.selector import Selector
from alphaware.pipeline import AlphaPipeline

# 加载MV和PB数据
data_pb = load_factor_data_from_csv('pb.csv')
data_mv = load_factor_data_from_csv('mv.csv') / 100000000

# 创建Factor实例，储存数据以及相关参数
factor_pb = Factor(data=data_pb,
                   name='PB',
                   property_dict={'type': FactorType.ALPHA_FACTOR, 'norm_type': FactorNormType.Industry_Neutral})
factor_mv = Factor(data=data_mv,
                   name='MV',
                   property_dict={'type': FactorType.ALPHA_FACTOR_MV, 'norm_type': FactorNormType.Industry_Neutral})

# 加载月度收益数据
data_return = load_factor_data_from_csv('return.csv')
# 将数据改成未来1月收益
data_return = fwd_return(data_return)
factor_return = Factor(data=data_return, name='1_Fwd_Return', property_dict={'type': FactorType.FWD_RETURN})

# 加载行业数据(早年的wind的行业代码不太全，可能用其他数据源的数据更好，此处仅做示例用)
data_industry_code = load_factor_data_from_csv('sw.csv')
factor_industry_code = Factor(data=data_industry_code,
                              name='industry_code',
                              property_dict={'type': FactorType.INDUSTY_CODE})

# 创建FactorContainer实例，加载所有的因子信息
fc = FactorContainer(start_date='2014-01-01',
                     end_date='2014-03-01',
                     factors=[factor_mv, factor_pb, factor_return, factor_industry_code])

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


# 第五步，按照因子排序打分，使用最简单的方法 - 等权求和
# 市值越小分数越高，PB越小分数越高
step_5 = ('rank', FactorSimpleRank(ascend_order=[-1, -1], out_container=True))

# 第六步，行业中性选股，选取每个行业的前10%
# 要读取一个行业权重比例的数据
industry_weight = load_factor_data_from_csv('industry_weight.csv')
step_6 = ('select', Selector(industry_weight=industry_weight, method=SelectionMethod.INDUSTRY_NEUTRAL))

pipeline = AlphaPipeline([step_1, step_2, step_3, step_4, step_5, step_6])
ptf = pipeline.fit_predict(fc)

print (ptf)
