# -*- coding: utf-8 -*-
from sklearn.pipeline import (_name_estimators,
                              Pipeline)
from sklearn.utils import tosequence
import six
from sklearn_pandas.pipeline import _call_fit
from ..base import FactorContainer


class AlphaPipeline(Pipeline):
    """
    https://github.com/pandas-dev/sklearn-pandas/blob/master/sklearn_pandas/pipeline.py
    """

    def __init__(self, steps, **kwargs):
        super(AlphaPipeline, self).__init__(steps)
        self._benchmark = kwargs.get('benchmark', None)

    def _pre_transform(self, factor_container, y=None, **fit_params):
        fit_params_steps = dict((step, {}) for step, _ in self.steps)
        for pname, pval in six.iteritems(fit_params):
            step, param = pname.split('__', 1)
            fit_params_steps[step][param] = pval
        fc = factor_container
        for name, transform in self.steps[:-1]:
            if hasattr(transform, "fit_transform"):
                fc_fit = _call_fit(transform.fit_transform,
                                   fc, y, **fit_params_steps[name])
            else:
                fc_fit = _call_fit(transform.fit,
                                   fc, y, **fit_params_steps[name]).transform(fc)
            if not isinstance(fc_fit, FactorContainer):
                try:
                    fc.replace_data(fc_fit)
                except ValueError:
                    raise ValueError(
                        'Failed in chain step {0}, please set out_container=True explicitly'.format(transform))
            else:
                fc = fc_fit

        return fc, fit_params_steps[self.steps[-1][0]]

    def fit(self, factor_container, y=None, **fit_params):
        fc_fit, fit_params = self._pre_transform(factor_container, y, **fit_params)
        _call_fit(self.steps[-1][-1].fit, factor_container, y, **fit_params)
        return self

    def fit_transform(self, factor_container, y=None, **fit_params):
        fc_fit, fit_params = self._pre_transform(factor_container, y, **fit_params)
        if hasattr(self.steps[-1][-1], "fit_transform"):
            return _call_fit(self.steps[-1][-1].fit_transform,
                             fc_fit, y, **fit_params)
        else:
            return _call_fit(self.steps[-1][-1].fit,
                             fc_fit, y, **fit_params).transform(fc_fit)

    def predict(self, factor_container, y=None, **fit_params):
        fc_fit, fit_params = self._pre_transform(factor_container, y, **fit_params)
        return self.steps[-1][-1].predict(fc_fit)

    def fit_predict(self, factor_container, y=None, **fit_params):
        fc_fit, fit_params = self._pre_transform(factor_container, y, **fit_params)
        if hasattr(self.steps[-1][-1], "fit_predict"):
            return _call_fit(self.steps[-1][-1].fit_predict,
                             fc_fit, y, **fit_params)
        else:
            return _call_fit(self.steps[-1][-1].fit,
                             fc_fit, y, **fit_params).predict(fc_fit)


def make_alpha_pipeline(*steps):
    return AlphaPipeline(_name_estimators(steps))
