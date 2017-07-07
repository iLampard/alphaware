# -*- coding: utf-8 -*-

import os
import sys
import unittest
import alphaware.tests.metrics as metrics
import alphaware.tests.pipeline as pipeline
import alphaware.tests.preprocess as preprocess
import alphaware.tests.utils as utils
import alphaware.tests.test_selector as test_selector

thisFilePath = os.path.abspath(__file__)
sys.path.append(os.path.sep.join(thisFilePath.split(os.path.sep)[:-2]))


def test():
    print('Python ' + sys.version)
    suite = unittest.TestSuite()
    tests = unittest.TestLoader().loadTestsFromTestCase(metrics.TestReturnMetrics)
    suite.addTest(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(pipeline.TestPipeline)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(preprocess.TestBenchmark)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(preprocess.TestFactorContainter)
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

    res = unittest.TextTestRunner(verbosity=3).run(suite)
    if len(res.errors) >= 1 or len(res.failures) >= 1:
        sys.exit(-1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test()
