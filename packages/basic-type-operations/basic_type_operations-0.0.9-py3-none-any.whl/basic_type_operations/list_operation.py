# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : list_operation.py 
@PRODUCT_NAME : PyCharm 
"""

import itertools
import math, random
import numpy as np
from basic_type_operations.number_operation import NumberOperation
from extra_utils.numpy_operations import NumpyBase


# 列表类工具
class ListOperation(NumpyBase):
    # <editor-fold desc="取数组的中位数">
    @staticmethod
    def get_median(lis):
        return NumberOperation.get_median(lis)

    # </editor-fold>
    # <editor-fold desc="列表的平均数">
    @staticmethod
    def avgList(lis, keep_decimal=2, integer=False):
        """uses floating-point division."""
        value = sum(lis) / len(lis)
        if integer:
            return round(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value
        # return round(sum(lis) / float(len(lis)), 2)

    # </editor-fold>
    # <editor-fold desc="列表最大值">
    @staticmethod
    def maxList(lis, keep_decimal=2, integer=False):
        value = max(lis)
        if integer:
            return math.ceil(value)  # 向上取整
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="列表最小值">
    @staticmethod
    def minList(lis, keep_decimal=2, integer=False):
        value = min(lis)
        if integer:
            return math.floor(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="二维数组求平均值">
    @staticmethod
    def avgList_two(lis, keep_decimal=2, integer=False):
        # SumValue = sum([sum(row) for row in lis])
        # numValue = len(lis[0]) * len(lis)
        # if numValue != 0:
        #     value = SumValue / numValue
        # else:
        #     value = SumValue
        value = np.array(lis).mean()
        if integer:
            return math.ceil(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="二维数组求最大值">
    @staticmethod
    def maxList_two(lis, keep_decimal=2, integer=False):
        value = np.array(lis).max()

        if integer:
            return math.ceil(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="二维数组求最小值">
    @staticmethod
    def minList_two(lis, keep_decimal=2, integer=False):
        # value = min([min(row) for row in lis])
        value = np.array(lis).min()
        if integer:
            return math.floor(value)
        if keep_decimal:
            return round(value, keep_decimal)
        return value

    # </editor-fold>
    # <editor-fold desc="区间内随机生成一个一维列表">
    @staticmethod
    def random_list(start, stop, length, keep_decimal=2, integer=False):
        if length >= 0:
            length = int(length)
            start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
            random_list = []
            if keep_decimal:
                for i in range(length):
                    # 整数
                    # random_list.append(random.randint(start, stop))
                    # 小数
                    # random_list.append(random.uniform(start, stop))
                    # 保留n位置小数
                    random_list.append(round(random.uniform(start, stop), keep_decimal))
            else:
                for i in range(length):
                    # 整数
                    random_list.append(random.randint(start, stop))
                    # 小数
                    # random_list.append(random.uniform(start, stop))
                    # 保留n位置小数
                    # random_list.append(round(random.uniform(start, stop), keep_decimal))
            return random_list

    # </editor-fold>
    # <editor-fold desc="不同长度的二维数组的转置">
    @staticmethod
    def list_T_differ(lis):
        try:
            max_len = max(len(i) for i in lis)
            b = [[] for _ in range(max_len)]  # 转置后列表
            if len(lis) > 0:
                for i in range(max_len):  # 行数
                    for ls in lis:
                        if i < ls.__len__():
                            b[i].append(ls[i])
                return b
            return None
        except:
            return None

    # </editor-fold>
    # <editor-fold desc="相同长度的二维数组的转置">
    @staticmethod
    def list_T(lis):
        try:
            li = np.array(lis)
            li = li.T
            li = li.tolist()
            return li
            # return None
        except:
            return None

    # </editor-fold>
    # <editor-fold desc="列表对应相除">
    @staticmethod
    def list_divide(lis1, lis2):
        num_len1 = len(lis1)
        num_len2 = len(lis2)
        num_len = num_len1
        if len(lis2) < num_len:
            num_len = num_len2
        lis3 = []
        for index in range(num_len):
            res = None
            if float(lis2[index]) == 0:
                res = 0
            else:
                res = round(float(lis1[index]) / float(lis2[index]), 2)
            lis3.append(res)
        return lis3

    # </editor-fold>
    # <editor-fold desc="列表随机返回n个元素">
    @staticmethod
    def lis_choices(lis, n):
        # lis = [i * 10 for i in range(10)]
        return random.choices(lis, k=n)

    # </editor-fold>
    # <editor-fold desc="数组过长-取100个点">
    @staticmethod
    def lis_get_points(lis, re_len=100):
        if len(lis) > re_len:
            yu_num = int(len(lis) / re_len)
            return [lis[i] for i in range(0, len(lis), yu_num)]
        else:
            return lis

    # </editor-fold>
    # <editor-fold desc="列表保留n位小数">
    @staticmethod
    def list_Keep_place(lis, decimal=0):
        """给出一个任意类型的数据列表，内部含有字符串，将数字转换为保留的小数"""
        if decimal == 0:
            for i in range(len(lis)):
                if isinstance(lis[i], str):
                    continue
                else:
                    lis[i] = NumberOperation.round_up(lis[i])
        else:
            for i in range(len(lis)):
                if isinstance(lis[i], str):
                    continue
                else:
                    lis[i] = NumberOperation.round_up(lis[i], decimal)

        return lis

    # </editor-fold>
    # <editor-fold desc="一维求每个元素的百分比">
    # str(round(res.count(1) / len(res), 2) * 100) + '%'
    @staticmethod
    def one_dimensional_percent(lis):
        count = len(lis)
        dic = dict()
        for i in lis:
            if dic.get(i):
                dic[i] += 1
            else:
                dic[i] = 1
        lis = list(dic.keys())
        # lis = list(set(lis))
        lis.sort()
        for i in lis:
            # str(round(res.count(1) / len(res), 2) * 100) + '%'
            dic[i] = str(round(dic[i] / count, 2) * 100) + "%"
        return dic

    # </editor-fold>
    # <editor-fold desc="不同长度的二维数组合并一维数组">
    @staticmethod
    def dimensional_list_two_marge(lis):
        len_a = len(lis)
        new_list = []
        for i in range(len_a):
            new_list = list(itertools.chain(new_list, lis[i]))
        return new_list

    # </editor-fold>
    # <editor-fold desc="一维列表元素按指定个数分组">
    @staticmethod
    def list_group(lis, n):
        """n: 一组多少条数据
        """
        return [lis[i:i + n] for i in range(0, len(lis), n)]

    # </editor-fold>
    # <editor-fold desc="list分成多少组">
    @staticmethod
    def lis_groups(lis, n):
        # n: 组数
        m = int(math.ceil(len(lis) / float(n)))
        sp_lis = []
        for i in range(n):
            sp_lis.append(lis[i * m:(i + 1) * m])
        return sp_lis
        # 可以不使用math模块

    @staticmethod
    def lis_groups1(lis, n):
        if len(lis) % n != 0:
            m = (len(lis) // n) + 1
        else:
            m = len(lis) // n
        sp_lis = []
        for i in range(n):
            sp_lis.append(lis[i * m:(i + 1) * m])
        return sp_lis

    @staticmethod
    def lis_groups2(lis, n):
        length = len(lis)
        sp_lis = []
        for i in range(n):
            sp_lis.append(
                lis[math.floor(i / n * length):math.floor((i + 1) / n * length)]
            )
        return sp_lis

    # </editor-fold>
    # <editor-fold desc="列表中大于一个数的个数">
    @staticmethod
    def greater_num_list(lis: list, num):
        lis = [i for i in lis if i > num]
        return lis, len(lis)

    # </editor-fold>
    # <editor-fold desc="列表中的字典按某个字段排序">
    @staticmethod
    def list_order(lis: list, fields=None, reverse=False):
        """
        :param lis:
        :param value:list 传入 索引  字典传入keys
        :return: list
        """
        if fields:
            lis: list = sorted(lis, key=lambda k: k[fields], reverse=reverse)
        else:
            lis: list = sorted(lis, reverse=reverse)
        return lis

    # </editor-fold>
    # <editor-fold desc="取出两者之间的数据">
    @staticmethod
    def between(lis, min_value=None, max_value=None):
        if max_value and min_value:
            l2 = [i for i in lis if i >= min_value and i <= max_value]
        elif min_value:
            l2 = [i for i in lis if i >= min_value]
        elif max_value:
            l2 = [i for i in lis if i <= max_value]
        else:
            l2 = []
        return l2

    # </editor-fold>
    # <editor-fold desc="二维数据进行等比区间分组-固定组数-求个数">
    @staticmethod
    def no_grouping_equivalent_interval(lis, n):
        """
        :param a: lis
        :param n: 个数
        :return:
        """
        dimensional_lis = ListOperation.list_T(lis)
        lis = dimensional_lis[0]
        lis1 = dimensional_lis[1]
        l = len(lis)
        interval = (max(lis) - min(lis)) / n  # 区间长度
        section = []  # 每个区间的范围
        # 横坐标
        x_section = []
        for i in range(n):
            section.append([min(lis) + i * interval, min(lis) + (i + 1) * interval])
            x_section.append(str(round(min(lis) + i * interval, 2)))
            # x_section.append(str(round(min(lis) + i * interval, 2)) + '~' + str(round(min(lis) + (i + 1) * interval, 2)))
        divided_list = [[] for i in range(n)]
        for i in range(l):
            for j in range(n):
                if section[j][0] <= lis[i] <= section[j][1]:
                    divided_list[j].append(lis1[i])
        y_section = []
        dic = {}
        for index, value in enumerate(divided_list):
            dic[x_section[index]] = round(len(value) / len(lis1), 2)
        return dic

    # </editor-fold>
    # <editor-fold desc="二维数据中，各个数据所占的百分比">
    @staticmethod
    def all_np_fen(lis):
        # 拼接数组函数
        List = list(itertools.chain.from_iterable(lis))
        arr = np.array(List)
        key = np.unique(arr)
        result = {}
        for k in key:
            mask = (arr == k)
            arr_new = arr[mask]
            v = arr_new.size
            result[k] = v
        key_list = list(result.keys())
        num_count = arr.shape[0]
        return_result = {}
        for keys in key_list:
            dat = result[keys] / num_count
            return_result[str(keys)] = NumberOperation.decimal_to_percentage(dat)
        return return_result
    # </editor-fold>
