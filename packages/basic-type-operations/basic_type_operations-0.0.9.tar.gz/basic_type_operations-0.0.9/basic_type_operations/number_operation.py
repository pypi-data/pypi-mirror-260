# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : number_operation.py 
@PRODUCT_NAME : PyCharm 
"""
import random
import struct
# https://docs.python.org/zh-cn/3/library/struct.html#examples
import decimal


# <editor-fold desc="数值类工具">
class NumberOperation(object):
    # <editor-fold desc="判断是否为数字">
    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # </editor-fold>
    # <editor-fold desc="四舍五入">
    @staticmethod
    def round_up(number, power=0):
        """
        实现精确四舍五入，包含正、负小数多种场景
        :param number: 需要四舍五入的小数
        :param power: 四舍五入位数，支持0-∞
        :return: 返回四舍五入后的结果
        """
        digit = 10 ** power
        num2 = float(int(number * digit))
        # 处理正数，power不为0的情况
        if number >= 0 and power != 0:
            tag = number * digit - num2 + 1 / (digit * 10)
            if tag >= 0.5:
                return (num2 + 1) / digit
            else:
                return num2 / digit
        # 处理正数，power为0取整的情况
        elif number >= 0 and power == 0:
            tag = number * digit - int(number)
            if tag >= 0.5:
                return int((num2 + 1) / digit)
            else:
                return int(num2 / digit)
        # 处理负数，power为0取整的情况
        elif power == 0 and number < 0:
            tag = number * digit - int(number)
            if tag <= -0.5:
                return int((num2 - 1) / digit)
            else:
                return int(num2 / digit)
        # 处理负数，power不为0的情况
        else:
            tag = number * digit - num2 - 1 / (digit * 10)
            if tag <= -0.5:
                return (num2 - 1) / digit
            else:
                return num2 / digit

    # </editor-fold>
    # <editor-fold desc="小数转换位 百分比 0.123---12.30">
    @staticmethod
    def decimal_to_percentage(decimal, percentage=False, decimal_num=2):
        # decimal = 0.3214523
        if decimal_num:
            decimal = round(float("%.2f" % (decimal * 100)), decimal_num)
        if percentage:
            decimal = "%.2f%%" % (decimal)
        return decimal

    # </editor-fold>
    # <editor-fold desc="百分数转小数">
    @staticmethod
    def percentage_to_decimal(percentage):
        # s = '20%'  # 默认要转换的百分比是字符串,例如
        aa = float(percentage.strip('%'))  # 去掉s 字符串中的 %
        bb = aa / 100.0  # 运行环境是Python2.7   其中Python2.X  与 python 3X中的除法是有区别
        return round(bb, 4)  # 输出结果是 0.2

    # </editor-fold>
    # <editor-fold desc="分隔浮点数的整数部分和小数部分1.23----[1,0.23]">
    @staticmethod
    def divmoddef(num):
        # math.modf(3.25)
        def chuli(num):
            data = list(divmod(num, 1))
            r_len = str(num).split('.')[1].__len__()
            data[0] = int(data[0])
            data[1] = round(data[1], r_len)
            return data

        if num > 0:
            data = chuli(num)
            return data
        elif num < 0:
            num = -num
            data = chuli(num)
            data[0] = -data[0]
            return data
        else:
            return [0, 0]

    # </editor-fold>
    # <editor-fold desc="摄氏度与华氏度互换">
    @staticmethod
    def Celsius_interchangeable_with_Fahrenheit(number, trans_type):
        """

        :param number:
        :param trans_type: 1 华氏度    2  摄氏度
        :return:
        """
        """
        摄氏度与华氏度互换
        """

        # trans_type = input('输入转摄氏度还是华氏度：')

        if trans_type == 1:  # 执行华氏度转摄氏度的逻辑
            # f = float(input('输入华氏温度：'))
            c = (number - 32) / 1.8
            return c
        elif trans_type == 2:  # 执行摄氏度转华氏度的逻辑
            # c = float(input('输入摄氏温度：'))
            f = number * 1.8 + 32
            return f
        else:
            return None

    # </editor-fold>
    # <editor-fold desc="是否构成三角形">
    @staticmethod
    def triangle_true(a, b, c):
        """
        是否构成三角形
        """
        if a + b > c and a + c > b and b + c > a:
            return True
        else:
            return False

    # </editor-fold>
    # <editor-fold desc="是否是素数">
    @staticmethod
    def prime_number(num):
        """
            是否是素数
        输入一个正整数，判断是否是素数。素数定义：大于1的自然数中，只能被1和它本身整除的自然数。如：3、5、7

        判断是否是素数
        """

        end = int(num // 2) + 1  #

        is_prime = True
        for x in range(2, end):
            if num % x == 0:
                is_prime = False
                break
        if is_prime and num != 1:
            return True
        else:
            return False

    # </editor-fold>
    # <editor-fold desc="水仙花数">
    @staticmethod
    def narcissistic_number(num):
        """
            水仙花数
        水仙花数是一个3位数，该数字每个位上数字的立方和正好等于它本身，例如：

        水仙花数
        """
        low = num % 10
        mid = num // 10 % 10
        high = num // 100
        if num == low ** 3 + mid ** 3 + high ** 3:
            return True
        else:
            return False

    # </editor-fold>
    # <editor-fold desc="阿拉伯数字转换成中文">
    # 12 -->  一二
    @staticmethod
    def num_to_char(num):
        """数字转中文"""
        num = str(num)
        num_dict = {"0": u"零", "1": u"一", "2": u"二", "3": u"三", "4": u"四", "5": u"五", "6": u"六", "7": u"七", "8": u"八",
                    "9": u"九"}
        listnum = list(num)
        shu = []
        for i in listnum:
            shu.append(num_dict[i])
        new_str = "".join(shu)
        return new_str

    # </editor-fold>
    # <editor-fold desc="要产生a~b的随机数小数">
    @staticmethod
    def random_a_to_b(a, b):
        return random.random() * (b - a) + a

    # </editor-fold>
    # <editor-fold desc="取固定范围的一个整数">
    @staticmethod
    def random_int_num(start, end):
        """
        :param start:开始值-整数
        :param end: 结束值整数
        :return:
        """
        return random.randint(start, end)

    # </editor-fold>
    # <editor-fold desc="取固定范围的一个小数，并保留小数位数">
    @staticmethod
    def random_float_num(start, end, decimal_num=2):
        """

        :param start: 开始值
        :param end: 结束值
        :param decimal_num: 小数保留位数
        :return:
        """
        return round(random.uniform(start, end), decimal_num)

    # </editor-fold>
    # <editor-fold desc="取数组的中位数">
    @staticmethod
    def get_median(data):
        data.sort()
        half = len(data) // 2  # x//2  ==   int(x/2)
        return (data[half] + data[~half]) / 2  # x[-3]  ==  x[~2]

    # </editor-fold>

# </editor-fold>
