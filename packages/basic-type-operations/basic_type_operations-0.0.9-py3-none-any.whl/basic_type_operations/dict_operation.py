# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : dict_operation.py 
@PRODUCT_NAME : PyCharm 
"""
from collections import Counter
from munch import Munch  ## munch-2.5.0


# <editor-fold desc="字典类工具">
class DictOperation(object):
    # <editor-fold desc="相同的key value相加 value是数值">
    @staticmethod
    def dict_value_add(*args):
        dict_new = Counter()
        for i in args:
            dict_new += Counter(i)
        return dict(dict_new)

    # </editor-fold>
    # <editor-fold desc="取出列表内所有字典的value值">
    @staticmethod
    def list_dict_value(lis):
        """
        :param lis:
        :return:
        """
        res = [item[key] for item in lis for key in item]
        return res

    # </editor-fold>
    # <editor-fold desc="取出列表内所有字典的keys值">
    @staticmethod
    def list_dict_keys(lis):
        """
        :param lis:
        :return:
        """
        res = [key for item in lis for key in item]
        return res

    # </editor-fold>
    # <editor-fold desc="字典组成的数组怎么进行去重">
    @staticmethod
    def delete_duplicate_remove(data):  # 适用一般情况
        # data = reduce(lambda x, y: x + [y] if y not in x else x, [[], ] + data)#
        data = [dict(t) for t in set([tuple(d.items()) for d in data])]
        return data

    @staticmethod
    def delete_duplicate_str(data):  # 适用这种情况如： data2 = [{"a": {"b": "c"}}, {"a": {"b": "c"}}]
        immutable_dict = set([str(item) for item in data])
        data = [eval(i) for i in immutable_dict]
        return data

    # </editor-fold>
    # <editor-fold desc="列表中的字典按某个字段排序">
    @staticmethod
    def list_order(data: list, fields=None, reverse=False):
        """
        :param data:
        :param value:list 传入 索引  字典传入keys
        :return: list
        """
        if fields:
            data: list = sorted(data, key=lambda k: k[fields], reverse=reverse)
        else:
            data: list = sorted(data, reverse=reverse)
        return data
    # </editor-fold>


# </editor-fold>
# Munch的使用
"""
from munch import Munch

profile = Munch()
print(isinstance(profile, dict))
# 并实现了点式赋值与访问，profile.name 与 profile['name'] 是等价的
profile.name = "iswbm"
print(profile)
profile.name = "iswbm1111"
print(profile)
print(Munch({'name': 'iswbm', 'age': 18, 'gender': 'male'}))
# 删除元素
profile.setdefault('gender')
print(profile)
# 转换成 JSON
munch_obj = Munch(foo=Munch(lol=True), bar=100, msg='hello')
#
"""
