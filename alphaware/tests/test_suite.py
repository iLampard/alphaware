# -*- coding: utf-8 -*-

import os
import sys
import unittest
from alphaware.tests.base import TestFactorContainer
from alphaware.tests.metrics import TestReturnMetrics
from alphaware.tests.pipeline import TestPipeline
from alphaware.tests.preprocess import (TestBenchmark,
                                        TestFactorImputer,
                                        TestExtCategoricalImputer,
                                        TestNeutralizer,
                                        TestStandardizer,
                                        TestWinsorizer)
from alphaware.tests.utils import (TestDateUtils,
                                   TestInputValidation,
                                   TestNumpyUtils,
                                   TestPandasUtils)
from alphaware.tests.test_selector import TestSelector
from alphaware.tests.analyzer import (TestFactorIC,
                                      TestFactorQuantile)

thisFilePath = os.path.abspath(__file__)
sys.path.append(os.path.sep.join(thisFilePath.split(os.path.sep)[:-3]))


def test():
    print('Python ' + sys.version)
    suite = unittest.TestSuite()
    tests = unittest.TestLoader().loadTestsFromTestCase(TestFactorContainer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestReturnMetrics)
    suite.addTest(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestPipeline)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestBenchmark)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestFactorImputer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestExtCategoricalImputer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestNeutralizer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestStandardizer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestWinsorizer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestDateUtils)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestInputValidation)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestNumpyUtils)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestPandasUtils)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestSelector)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestFactorIC)
    suite.addTest(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(TestFactorQuantile)
    suite.addTest(tests)

    res = unittest.TextTestRunner(verbosity=3).run(suite)
    if len(res.errors) >= 1 or len(res.failures) >= 1:
        sys.exit(-1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test()
