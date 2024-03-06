# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : tuple_operation.py 
@PRODUCT_NAME : PyCharm 
"""


# <editor-fold desc="元组操作">
class TupleOperation(object):
    @staticmethod
    def tuple_to_list_key(data, key1, key2=None):
        lis = []
        if not key2:
            key2 = "label"
        for li in data:
            lis.append({
                key1: li[0],
                key2: li[1],
            })
        return lis

    @staticmethod
    def tuple_to_dict_key(data):
        return dict(data)
# </editor-fold>
