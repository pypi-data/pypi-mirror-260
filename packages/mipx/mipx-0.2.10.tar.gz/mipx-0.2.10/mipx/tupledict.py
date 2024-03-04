# -*- coding: utf-8 -*-
# @Time    : 2023/4/1 10:39
# @Author  : luyi
from functools import reduce
from typing import Dict
from .utilx import tuple_fuzz_match_list, is_list_or_tuple, get_length
from .tuplelist import tuplelist
from .interface_ import ITupledict


class tupledict(ITupledict):
    """
    tupledict is a subclass of dict where
      the keys are a tuplelist.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if is_list_or_tuple(value):  # 不复杂化，，仅支持为一个参数。一般为变量var
            raise ValueError("tupledict的value值应为单一对象")
        super().__setitem__(key, value)

    def prod(self, coeff: Dict, *pattern):
        """
        coeff为一个dict类型，指定待计算的元素的系数。coeff的key要与待计算的集合中的key能对应
        :param coeff:
        :param pattern:
        :return:
        """
        tList = tuplelist(self.keys())
        tl = tList.select(*pattern)
        if len(tl) == 0:
            return 0
        pl = []
        for key in tl:
            ok, k = tuple_fuzz_match_list(key, coeff.keys())
            if ok:
                pl.append(self[key] * coeff[k])
        return reduce(lambda a, b: a + b, pl)

    def select(self, *pattern):
        tlist = tuplelist(self.keys())
        keys = tlist.select(*pattern)
        return [self[key] for key in keys]

    def sum(self, *pattern, **kwargs):
        v = self.select(*pattern)
        if len(v) == 0:
            return 0
        return reduce(lambda a, b: a + b, v)


def multidict(data: Dict):
    """

    :param data:
    :return:
    """
    """
    ROUTINE:
        multidict(data)
      PURPOSE:
        Split a single dictionary into multiple dictionaries.
      ARGUMENTS:
        data: A dictionary that maps each key to a list of 'n' values.
      RETURN VALUE:
        A list of the shared keys, followed by individual tupledicts.
      EXAMPLE:
        keys, [dict1, dict2] = multidict( {
                 'key1': [1, 2],
                 'key2': [1, 3],
                 'key3': [1, 4] } )
    """
    t_list = tuplelist(data.keys())
    num = None
    for key, items in data.items():
        _num = get_length(items)
        if num is None:
            num = _num
        else:
            if num != _num:
                raise ValueError("length of values should be same")
    if num is None:
        raise ValueError("multidict error")
    t_dicts = [tupledict({key: data[key][i] if is_list_or_tuple(data[key]) else data[key] for key in t_list})
               for i in range(num)]
    if num == 1:
        return t_list, t_dicts[0]
    return t_list, *t_dicts
