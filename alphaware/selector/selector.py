# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from ..preprocess import FactorTransformer


class Selector(FactorTransformer):
    def __init__(self, copy=True, groupby_date=True, out_container=False):
        super(Selector, self).__init__(copy=copy, groupby_date=groupby_date, out_container=out_container)
