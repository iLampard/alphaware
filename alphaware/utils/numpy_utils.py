# -*- coding: utf-8 -*-


def index_n_largest(array, n):
    return array.argsort()[-n:][::-1]


def index_n_smallest(array, n):
    return array.argsort()[:n]
