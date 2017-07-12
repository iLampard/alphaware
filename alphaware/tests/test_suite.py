# -*- coding: utf-8 -*-

import os
import sys
import unittest
from alphaware.tests import (base,
                             metrics,
                             pipeline,
                             preprocess,
                             utils,
                             test_selector,
                             analyzer)

thisFilePath = os.path.abspath(__file__)
sys.path.append(os.path.sep.join(thisFilePath.split(os.path.sep)[:-2]))


def test():
    print('Python ' + sys.version)
    suite = unittest.TestSuite()
    tests = unittest.TestLoader().loadTestsFromTestCase(base.TestFactorContainer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(metrics.TestReturnMetrics)
    suite.addTest(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(pipeline.TestPipeline)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(preprocess.TestBenchmark)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(preprocess.TestFactorImputer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(preprocess.TestExtCategoricalImputer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(preprocess.TestNeutralizer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(preprocess.TestStandardizer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(preprocess.TestWinsorizer)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(utils.TestDateUtils)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(utils.TestInputValidation)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(utils.TestNumpyUtils)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(utils.TestPandasUtils)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(test_selector.TestSelector)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(analyzer.TestFactorIC)
    suite.addTest(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(analyzer.TestFactorQuantile)
    suite.addTest(tests)

    res = unittest.TextTestRunner(verbosity=3).run(suite)
    if len(res.errors) >= 1 or len(res.failures) >= 1:
        sys.exit(-1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test()
