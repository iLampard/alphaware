# -*- coding: utf-8 -*-


from collections import namedtuple

MULTI_INDEX_FACTOR = namedtuple('MULTI_INDEX_FACTOR', ['date_index', 'sec_index', 'full_index'])
MULTI_INDEX_FACTOR.date_index = 'tradeDate'
MULTI_INDEX_FACTOR.sec_index = 'secID'
MULTI_INDEX_FACTOR.full_index = ['tradeDate', 'secID']

MULTI_INDEX_INDUSTRY_WEIGHT = namedtuple('MULTI_INDEX_FACTOR', ['date_index', 'industry_index', 'full_index', 'col_name'])
MULTI_INDEX_INDUSTRY_WEIGHT.date_index = 'tradeDate'
MULTI_INDEX_INDUSTRY_WEIGHT.industry_index = 'industry'
MULTI_INDEX_INDUSTRY_WEIGHT.full_index = ['tradeDate', 'industry']
MULTI_INDEX_INDUSTRY_WEIGHT.col_name = ['weight']

MULTI_INDEX_SELECTOR = namedtuple('MULTI_INDEX_SELECTOR', ['date_index', 'sec_index', 'col_name'])
MULTI_INDEX_SELECTOR.date_index = 'tradeDate'
MULTI_INDEX_SELECTOR.sec_index = 'secID'
MULTI_INDEX_SELECTOR.col_name = ['weight']


SW_INDUSTRY_MAP = {
    '801190.SI': '金融服务',
    '801200.SI': '商业贸易',
    '801210.SI': '休闲服务',
    '801220.SI': '信息服务',
    '801230.SI': '综合',
    '801170.SI': '交通运输',
    '801160.SI': '公用事业',
    '801150.SI': '医药生物',
    '801140.SI': '轻工制造',
    '801130.SI': '纺织服装',
    '801120.SI': '食品饮料',
    '801110.SI': '家用电器',
    '801100.SI': '信息设备',
    '801090.SI': '交运设备',
    '801080.SI': '电子',
    '801070.SI': '机械设备',
    '801010.SI': '农林牧渔',
    '801020.SI': '采掘',
    '801030.SI': '化工',
    '801040.SI': '钢铁',
    '801050.SI': '有色金属',
    '801060.SI': '建筑建材',
    '801180.SI': '房地产',
    '801880.SI': '汽车',
    '801790.SI': '非银金融',
    '801780.SI': '银行',
    '801770.SI': '通信',
    '801760.SI': '传媒',
    '801750.SI': '计算机',
    '801740.SI': '国防军工',
    '801730.SI': '电气设备',
    '801720.SI': '建筑装饰',
    '801710.SI': '建筑材料',
    '801890.SI': '机械设备',
    'other': '无行业'
}