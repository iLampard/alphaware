# -*- coding: utf-8 -*-

from unittest import TestCase
from datetime import datetime as dt
from parameterized import parameterized
import pandas as pd
from pandas.util.testing import assert_frame_equal
from alphaware.selector import (BrutalSelector,
                                IndustryNeutralSelector,
                                Selector)
from alphaware.enums import (FactorType,
                             SelectionMethod)
from alphaware.preprocess import (Factor,
                                  FactorContainer)
from alphaware.const import (INDEX_FACTOR,
                             INDEX_INDUSTRY_WEIGHT)


class TestSelector(TestCase):
    @parameterized.expand(
        [(pd.Series([3, 2, 4, 5, 6], index=['001', '002', '003', '004', '005']),
          2,
          0.1,
          pd.DataFrame([50.0, 50.0], index=['005', '004'], columns=['weight'])),
         (pd.Series([3, 2, 4, -5, -6], index=['001', '002', '003', '004', '005']),
          2,
          0.1,
          pd.DataFrame([50.0, 50.0], index=['003', '001'], columns=['weight'])),
         (pd.Series([3, 2, 4, 5, 6], index=['001', '002', '003', '004', '005']),
          None,
          0.8,
          pd.DataFrame([25.0, 25.0, 25.0, 25.0], index=['005', '004', '003', '001'], columns=['weight']))])
    def test_brutal_selector(self, X, nb_select, prop_select, expected):
        calculated = BrutalSelector(nb_select, prop_select).fit_transform(X)
        assert_frame_equal(calculated, expected)

    @parameterized.expand([(pd.DataFrame({'score': [2, 3, 3, 8, 4, 5], 'industry_code': ['a', 'a', 'a', 'b', 'b', 'b']},
                                         index=['001', '002', '003', '004', '005', '006']),
                            pd.DataFrame({'weight': [0.5, 0.4, 0.1]}, index=['a', 'b', 'c']),
                            0.1,
                            2,
                            False,
                            pd.DataFrame({'industry_code': ['a', 'a', 'b', 'b'],
                                          'weight': [0.25, 0.25, 0.2, 0.2]},
                                         index=['002', '003', '004', '006'])
                            ),
                           (pd.DataFrame({'score': [2, 3, 3, 8, 4, 5, 2, 3, 1, 11],
                                          'industry_code': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c']},
                                         index=['001', '002', '003', '004', '005', '006', '007', '008', '009', '010']),
                            pd.DataFrame({'weight': [0.5, 0.4, 0.1]}, index=['a', 'b', 'c']),
                            0.6,
                            1,
                            True,
                            pd.DataFrame({'score': [8, 3, 5, 4, 3, 11],
                                          'industry_code': ['a', 'a', 'b', 'b', 'b', 'c'],
                                          'weight': [0.25, 0.25, 0.1333333333, 0.133333333333, 0.1333333333, 0.1]},
                                         index=['004', '002', '006', '005', '008', '010'])
                            )])
    def test_industry_neutral_selector(self,
                                       X,
                                       industry_weight,
                                       prop_select,
                                       min_select_per_industry,
                                       out_full,
                                       expected):
        calculated = IndustryNeutralSelector(industry_weight=industry_weight,
                                             min_select_per_industry=min_select_per_industry,
                                             prop_select=prop_select,
                                             out_full=out_full
                                             ).fit_transform(X)
        try:
            expected = expected[['score', 'industry_code', 'weight']]
        except KeyError:
            pass

        assert_frame_equal(calculated, expected)

    def test_selector(self):
        index_weight = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['a', 'b', 'other']],
                                                  names=INDEX_INDUSTRY_WEIGHT.full_index)
        industry_weight = pd.DataFrame([0.5, 0.4, 0.1, 0.5, 0.3, 0.2], index=index_weight)

        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003', '004', '005']],
                                           names=INDEX_FACTOR.full_index)
        X = pd.DataFrame({'score': [2, 3, 3, 8, 4, 5, 9, 11, 2, 0],
                          'industry_code': ['a', 'a', 'a', 'b', 'b', 'a', 'a', 'other', 'b', 'b']},
                         index=index)

        score = Factor(data=X['score'], name='score', property_dict={'type': FactorType.SCORE})
        industry_code = Factor(data=X['industry_code'], name='industry_code',
                               property_dict={'type': FactorType.INDUSTY_CODE})
        fc = FactorContainer(start_date='2014-01-30', end_date='2014-02-28')
        fc.add_factor(score)
        fc.add_factor(industry_code)

        calculated = Selector(industry_weight=industry_weight,
                              method=SelectionMethod.INDUSTRY_NEUTRAL).fit_transform(fc)
        print calculated
