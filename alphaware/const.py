# -*- coding: utf-8 -*-


from collections import namedtuple

MULTI_INDEX_FACTOR = namedtuple('MULTI_INDEX_FACTOR', ['date_index', 'sec_index', 'full_index'])
MULTI_INDEX_FACTOR.date_index = 'tradeDate'
MULTI_INDEX_FACTOR.sec_index = 'secID'
MULTI_INDEX_FACTOR.full_index = ['tradeDate', 'secID']

MULTI_INDEX_INDUSTRY_WEIGHT = namedtuple('MULTI_INDEX_FACTOR', ['date_index', 'industry_index', 'full_index'])
MULTI_INDEX_INDUSTRY_WEIGHT.date_index = 'tradeDate'
MULTI_INDEX_INDUSTRY_WEIGHT.industry_index = 'industry'
MULTI_INDEX_INDUSTRY_WEIGHT.full_index = ['tradeDate', 'industry']

BENCHMARK_DATA = namedtuple('BENCHMARK_DATA', ['hist_return', 'industry_weight'])
