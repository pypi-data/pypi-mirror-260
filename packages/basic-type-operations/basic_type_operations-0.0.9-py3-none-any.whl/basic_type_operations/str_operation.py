# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : str_operation.py 
@PRODUCT_NAME : PyCharm 
"""
from rest_framework.exceptions import ParseError
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random, string, struct, binascii, datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# 中文转英文
import pinyin.cedict
from config import WKHMLTOPDF


class ValidateCode(object):
    _letter_cases = "abcdefhjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z ,g
    _upper_cases = _letter_cases.upper()  # 大写字母
    _numbers = ''.join(map(str, range(3, 10)))  # 数字
    init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

    # 生成验证码
    @staticmethod
    def create_validate_code(
            size=(120, 30),
            chars=init_chars,
            img_type="GIF",
            mode="RGB",
            bg_color=(255, 255, 255),
            fg_color=(0, 0, 255),
            font_size=18,
            font_type=WKHMLTOPDF,
            length=4,
            draw_lines=True,
            n_line=(1, 2),
            draw_points=True,
            point_chance=2):
        """
        @todo: 生成验证码图片
        @param size: 图片的大小，格式（宽，高），默认为(120, 30)
        @param chars: 允许的字符集合，格式字符串
        @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        """

        width, height = size  # 宽高
        # 创建图形
        img = Image.new(mode, size, bg_color)
        draw = ImageDraw.Draw(img)  # 创建画笔

        def get_chars():
            """生成给定长度的字符串，返回列表格式"""
            return random.sample(chars, length)

        def create_lines():
            """绘制干扰线"""
            line_num = random.randint(*n_line)  # 干扰线条数

            for i in range(line_num):
                # 起始点
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                # 结束点
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
            """绘制干扰点"""
            chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

            for w in range(width):
                for h in range(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
            """绘制验证码字符"""
            c_chars = get_chars()
            strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

            font = ImageFont.truetype(font_type, font_size)
            font_width, font_height = font.getsize(strs)

            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                      strs, font=font, fill=fg_color)

            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

        return img, strs

    """
    # pip3 install pillow
    from PIL import Image, ImageDraw, ImageFont
    import random
    from io import BytesIO, StringIO
    def get_random():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 图片验证相关
    def get_code(request):
        img_obj = Image.new('RGB', (310, 35), get_random())
        img_draw = ImageDraw.Draw(img_obj)  # 生成一个画笔对象
        img_font = ImageFont.truetype('static/font/111.ttf', 30)  # 字体样式

        # 生成随机验证码
        code = ''
        for i in range(5):
            random_upper = chr(random.randint(65, 90))
            random_lower = chr(random.randint(97, 122))
            random_int = str(random.randint(0, 9))
            temp = random.choice([random_upper, random_lower, random_int])
            # 将产生的随机字符写在图片上
            img_draw.text((i * 45 + 45, 0), temp, get_random(), img_font)
            code += temp

        print(code)
        # 将随机验证码存储起来，以便其它函数调用
        request.session['code'] = code

        io_obj = BytesIO()
        img_obj.save(io_obj, 'png')
        # return HttpResponse(io_obj.getvalue())


    """


# 字符串类工具
class StringOperation(ValidateCode):

    @staticmethod
    def random_psd(psd_length: int):
        """
            建议:psd_length 为 大于8的整数
        :param psd_length:
        :return:
        """
        if psd_length < 8:
            raise ParseError('密码不应小于8位')
        src_digits = string.digits  # string_数字
        src_uppercase = string.ascii_uppercase  # string_大写字母
        src_lowercase = string.ascii_lowercase  # string_小写字母
        # 随机生成数字、大写字母、小写字母的组成个数（可根据实际需要进行更改）
        digits_num = random.randint(1, 6)
        uppercase_num = random.randint(1, psd_length - digits_num - 1)
        lowercase_num = psd_length - (digits_num + uppercase_num)
        # 生成字符串
        password = random.sample(src_digits, digits_num) + random.sample(src_uppercase, uppercase_num) + random.sample(
            src_lowercase, lowercase_num)
        # 打乱字符串
        random.shuffle(password)
        # 列表转字符串
        new_password = ''.join(password)
        return new_password

    # <editor-fold desc="查看是否包含中文">
    @staticmethod
    def check_contain_zh_cn(file_name: str):
        """
            查看是否包含中文
        :param file_name:
        :return:
        """
        for ch in file_name:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        else:
            return False

    # </editor-fold>
    # <editor-fold desc="需要补0的数字">
    @staticmethod
    def autoFill0(e, t):
        """

        :param e:  需要补0的数字
        :param t:  需要补充到多少位
        :return:
        """
        i = ""
        e_str = str(e)
        # t = t ||  2;
        for o in range(t - len(e_str)):
            if o < t:
                i += "0"
        return i + e_str if e < 10 ** (t - 1) else e_str

    # </editor-fold>
    # <editor-fold desc="中文转换成拼音">
    @staticmethod
    def chinese_english(s):
        return pinyin.get(s, format="strip", delimiter="")

    # </editor-fold>
    # <editor-fold desc="字符串内拼接字符串">
    @staticmethod
    def str_concatenation(lis):
        """

        :param lis:
        :return: "'1','2','3'"
        """
        # lis = ['1', '2', '3', '4', '1', '2', '3', '4', '1', '2']
        lis1 = ",".join(["'%s'" for _ in range(len(lis))])
        str_ = f"""{lis1}""" % tuple(lis)
        return str_

    # </editor-fold>
    # <editor-fold desc="忽略顺序 非完全匹配 匹配俩个字符串的相似度">
    # 参考文档 ： https://mp.weixin.qq.com/s/hyJwYAHHHgfuk83DBls-3A
    @staticmethod
    def token_sort_ratio(str1, str2):
        """
        params: str1
        params: str1
        returns:int
        案例：
        fuzz.token_sort_ratio("西藏 自治区", "自治区 西藏")
        output：100
        """
        return fuzz.token_sort_ratio(str1, str2)

    # </editor-fold>
    # <editor-fold desc="在列表中找最佳匹配的多个字符串和相似度">
    @staticmethod
    def extract(str, lis, limit=1):
        """
      lis = ["河南省", "郑州市", "湖北省", "武汉市"]
      process.extract("郑州", lis, limit=2)
      output:[('郑州市', 90), ('河南省', 0)]
      """
        return process.extract(str, lis, limit=limit)

    # </editor-fold>
    # <editor-fold desc="在列表中找最佳匹配的字符串和相似度">
    @staticmethod
    def extractOne(str, lis):
        """
        lis = ["河南省", "郑州市", "湖北省", "武汉市"]
        process.extractOne("郑州", lis)
        output:('郑州市', 90)
        process.extractOne("北京", lis)
        output:('湖北省', 45)
        """
        return process.extractOne(str, lis)
    # </editor-fold>


# 引用 https://codeigo.com/python/printing-subscript-and-superscript/
class StrUpperLower(object):
    letter_big = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letter_small = "abcdefghijklmnopqrstuvwxyz"
    normal_num = "0123456789"
    upper_num = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    lower_num = "₀₁₂₃₄₅₆₇₈₉"
    upper_letter = "ⁱⁿ"
    lower_letter = "ₐₑₒₓₕₖₗₘₙₚₛₜ"
    other_upper_string = "⁺⁻⁼⁽⁾"
    other_lower_string = "₊₋₌₍₎"
    tem = '℃'
    temF = '℉'
    other1 = "^"
    other2 = " ‰  ₔ._α β χ δ ε η γ ι κ λ μ ν ω ο φ πψ ρ σ τ θ υ ξ ζ"

    def Uppercase(self, msg):
        #  Uppernum = '零一二三四五六七八九'
        dic = {
            0: "零",
            1: "一",
            2: "二",
            3: "三",
            4: "四",
            5: "五",
            6: "六",
            7: "七",
            8: "八",
            9: "九",
            10: "十",
        }
        return dic.get(msg)
        # import cn2an
        # print(cn2an.an2cn(121, 'low'))
        # print(cn2an.an2cn(121, 'up'))
        # print(cn2an.an2cn(121, 'direct'))
        # print(cn2an.an2cn(121, 'rmb'))

    # 反向遍历 3
    def backward_cn2an_three(self, inputs):
        # 数字映射
        number_map = {
            "零": 0,
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9
        }

        # 单位映射
        unit_map = {
            "十": 10,
            "百": 100,
            "千": 1000,
            "万": 10000,
            "亿": 100000000
        }
        output = 0
        unit = 1
        # 万、亿的单位
        ten_thousand_unit = 1
        num = 0
        for index, cn_num in enumerate(reversed(inputs)):
            if cn_num in number_map:
                # 数字
                num = number_map[cn_num]
                # 累加
                output = output + num * unit
            elif cn_num in unit_map:
                # 单位
                unit = unit_map[cn_num]
                # 判断出万、亿
                if unit % 10000 == 0:
                    # 万、亿
                    if unit > ten_thousand_unit:
                        ten_thousand_unit = unit
                    # 万亿
                    else:
                        ten_thousand_unit = unit * ten_thousand_unit
                        unit = ten_thousand_unit

                if unit < ten_thousand_unit:
                    unit = ten_thousand_unit * unit
            else:
                raise ValueError(f"{cn_num} 不在转化范围内")

        return output

    # 字母 大写
    def letter_big_to_small(self, msg):
        # 创建字符映射表
        maketrans = str.maketrans(StrUpperLower.letter_big, StrUpperLower.letter_small)
        return msg.translate(maketrans)

    def letter_small_to_big(self, msg):
        # 创建字符映射表
        maketrans = str.maketrans(StrUpperLower.letter_small, StrUpperLower.letter_big)
        return msg.translate(maketrans)

    def letter_lower(self, msg):
        # 创建字符映射表
        msg = msg.lower()
        maketrans = str.maketrans("aeoxhklmnpst", StrUpperLower.lower_letter)
        return msg.translate(maketrans)

    def letter_upper(self, msg):
        # 创建字符映射表
        msg = msg.lower()
        maketrans = str.maketrans("in", StrUpperLower.upper_letter)
        return msg.translate(maketrans)

    def num_lower(self, msg):
        # 创建字符映射表
        maketrans = str.maketrans(StrUpperLower.normal_num, StrUpperLower.lower_num)
        return msg.translate(maketrans)

    def num_upper(self, msg):
        # 创建字符映射表
        maketrans = str.maketrans(StrUpperLower.normal_num, StrUpperLower.upper_num)
        return msg.translate(maketrans)
    # def other_lower(self,msg):


"""
案例
# 要转换的字符串
formula = 'y=x3+2x2+3x+4'
# 匹配出要转换的表示次幂的字符
results = re.findall(r'x\d\+', formula)
# 依次替换成上标的格式
for s in results:
    # s[:-1]的目的是让结尾的加号(+)不参与替换操作，因为“+”与通配符有冲突
    formula = re.sub(s[:-1], s[:-1].translate(sup_map), formula)
print(formula)  # 输出：y=x³+2x²+3x+4

"""


# 进制 互转 binary 二进制
class BaseConversion(object):
    """
    bin() 将给的参数转换成二进制
    otc() 将给的参数转换成八进制
    hex() 将给的参数转换成十六进制
    str() 将数据转化成字符串
    bytes() 把字符串转化成bytes类型
    ord() 输入字符找带字符编码的位置,对表示单个 Unicode 字符的字符，返回代表它 Unicode 码点的整数。例如 ord(‘a’) 返回整数 97， ord(‘€’) （欧元符号）返回 8364
    chr() 输入位置数字找出对应的字符,返回 Unicode 码位为整数 i 的字符的字符格式。例如，chr(97) 返回字符 ‘a’，chr(8364) 返回字符 ‘€’
    ascii() 是ascii码中的返回该值 不是就返回u   ascii('A') 返回 A ,ascii('€') 返回 '\u20ac'
    repr() 返回一个对象的string形式
    """

    # <editor-fold desc="二进制转换">
    # 二进制转字符
    def bin_to_chr(self, msg):
        # x = '0b100111000000000'
        return chr(int(msg, 2))

    # 二进制转十进制
    def bin_to_int(self, msg):
        return int(msg, 2)

    # 二进制转八进制
    def bin_to_oct(self, msg):
        return oct(int(msg, 2))

    # 二进制转十六进制
    def bin_to_hex(self, msg):
        return hex(int(msg, 2))

    # </editor-fold>
    # <editor-fold desc="八进制转换">
    # 八进制转字符
    def oct_to_chr(self, msg):
        return chr(int(msg, 8))

    # 八进制转二进制
    def oct_to_bin(self, msg):
        return bin(int(msg, 8))

    # 八进制转十进制
    def oct_to_int(self, msg):
        return int(msg, 8)

    # 八进制转十六进制
    def oct_to_hex(self, msg):
        return hex(int(msg, 8))

    # </editor-fold>
    # <editor-fold desc="十进制转换">
    # 十进制转换字符
    def int_to_chr(self, msg):
        return chr(msg)

    # 转二进制
    def int_to_bin(self, msg):
        return bin(msg)

    # 转八进制
    def int_to_oct(self, msg):
        return oct(msg)

    # 十进制转16进制
    def int_to_hex(self, msg):
        return hex(msg)

    # </editor-fold>
    # <editor-fold desc="十六进制转换">
    # 十六进制转换字符
    def hex_to_chr(self, msg):
        return chr(int(msg, 16))

    # 16-二进制
    def hex_to_bin(self, msg):
        return bin(int(msg, 16))
        # data = ''
        # for i in range(int(len(msg) / 2)):
        #     c = int(msg[i * 2:(i + 1) * 2], 16)
        #     state_2 = '{:08b}'.format(c)
        #     data += state_2
        # return data

    # 16--八进制
    def hex_to_oct(self, msg):
        data = oct(int(msg, 16))
        return data

    # 16--int
    def hex_to_int(self, msg):
        data = int(msg, 16)
        return data

    # </editor-fold>
    # <editor-fold desc="字符转换">
    # 字符转二进制
    def chr_to_bin(self, msg):
        return bin(ord(msg))

    # 字符转八进制
    def chr_to_oct(self, msg):
        return oct(ord(msg))

    # 字符转十进制 /Unicode编码方法
    def chr_to_ord(self, msg):
        return ord(msg)

    #  # 字符转十六进制
    def chr_to_hex(self, msg):
        print(hex(ord(msg)))

    # </editor-fold>
    # <editor-fold desc="Unicode编码">
    # Unicode编码转化为字符方法
    def ord_to_chr(self, msg):
        return chr(msg)

    # </editor-fold>
    # <editor-fold desc="字符串与16进制互转">
    # 十六进制转换字符串 bytes
    def hex_to_str(self, msg, encoding="utf-8"):
        """
        msg = '46494E530000000C00000000000000000000006B'  # 16进制
        msg = b'46494E530000000C00000000000000000000006B'  # 16进制bytes类型
        return b'FINS\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00k'
        <class 'bytes'>
        binascii.unhexlify = binascii.a2b_hex
        从十六进制字符串msg返回二进制数据。是b2a_hex的逆向操作。
        msg必须包含偶数个十六进制数字（可以是大写或小写），否则报TypeError。
        """
        data = binascii.a2b_hex(msg)
        if encoding:
            return data.decode(encoding)
        return data

    # 字符串转16进制
    def str_to_hex(self, msg, encoding="utf-8"):
        """
        binascii.b2a_hex = msg.encode().hex()
        """
        if encoding:
            return binascii.b2a_hex(msg.encode(encoding))
        else:
            return binascii.b2a_hex(msg.encode())

    # </editor-fold>
    # <editor-fold desc="时间与16进制互转">
    # 时间转换成16进制
    def datetime_to_hex(self, date=None):
        if not date:
            date = datetime.datetime.now()
        year = date.year - 2000
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second
        bit = ''.join([self.int_to_hex(i) for i in [year, month, day, hour, minute, second]])
        return bit

    # 16进制转换成时间
    def hex_to_datetime(self, msg, bates_len=2):
        year = BaseConversion().hex_to_int('0x' + msg[:1 * bates_len]) + 2000
        mouth = BaseConversion().hex_to_int('0x' + msg[1 * bates_len:2 * bates_len])
        days = BaseConversion().hex_to_int('0x' + msg[2 * bates_len:3 * bates_len])
        hours = BaseConversion().hex_to_int('0x' + msg[3 * bates_len:4 * bates_len])
        minute = BaseConversion().hex_to_int('0x' + msg[4 * bates_len:5 * bates_len])
        second = BaseConversion().hex_to_int('0x' + msg[5 * bates_len:6 * bates_len])
        # 2019, 11, 21, 13, 29, 52
        dt = datetime.datetime(year, mouth, days, hours, minute, second)
        return dt

    # </editor-fold>
    # <editor-fold desc="float/double与16进制互转">
    # float 转16进制
    def float_to_hex(self, msg):
        return hex(struct.unpack('<I', struct.pack('<f', msg))[0])

    # 双浮点型转16进制
    def double_to_hex(self, msg):
        return hex(struct.unpack('<Q', struct.pack('<d', msg))[0])

    # 16进制转float
    def hex_to_float(self, msg, round_number=2):
        i = int(msg, 16)
        return round(struct.unpack('<f', struct.pack('<I', i))[0], round_number)

    # 16进制转 双进度 float
    def hex_to_double(self, msg):
        i = int(msg, 16)
        return struct.unpack('<d', struct.pack('<Q', i))[0]

    # </editor-fold>
    # <editor-fold desc="中文与16进制互转">
    # 中文转16进制
    def chinese_to_hex(self, data):
        return_dat = ''
        for c in data:
            if not ('\u4e00' <= c <= '\u9fa5'):
                st = c.encode().hex()
                return_dat += '00' + st
                # return False
            else:
                st = c.encode('raw_unicode_escape')
                st = st.decode("utf-8")
                st = st.replace("\\u", "")
                return_dat += st

        # return True
        return return_dat

    # 16进制转中文
    def hex_to_chinese(self, data):
        """
          l = len(data)
    jiange = 4
    n = int(l / 4)
    right = 0
    dat = []
    hanzi = ''
    for i in range(n):
        left = right
        right = jiange * (1 + i)
        dat.append(data[left:right])

    for da in dat:
        # 去掉十六进制前两位0x，替换为\\u开头的字符串
        h_t = "\\u" + da
        # 把字符串编码成utf-8
        h_st = h_t.encode('utf-8')
        # 最后用unicode解码，得到对应的汉字
        h_st = h_st.decode("unicode_escape")
        hanzi += h_st

        """
        return bytes.fromhex(data).decode('gbk')

    # </editor-fold>
    # <editor-fold desc="CRC校验">
    # from crc_itu import crc16 as crcITU

    # def crc16(data):
    #     # crc = 0xffff
    #     # for byte in (ord(c) for c in data):
    #     #     crc = ((crc >> 8) ^ my_table[(crc ^ byte) & 0xff])
    #     # return_h = (~crc) & 0xffff
    #     # return hex(return_h)[2:]
    #     return hex(crcITU(data.encode()))[2:]
    def crc16(self, value):
        my_table = (
            0X0000, 0X1189, 0X2312, 0X329B, 0X4624, 0X57AD, 0X6536, 0X74BF,
            0X8C48, 0X9DC1, 0XAF5A, 0XBED3, 0XCA6C, 0XDBE5, 0XE97E, 0XF8F7,
            0X1081, 0X0108, 0X3393, 0X221A, 0X56A5, 0X472C, 0X75B7, 0X643E,
            0X9CC9, 0X8D40, 0XBFDB, 0XAE52, 0XDAED, 0XCB64, 0XF9FF, 0XE876,
            0X2102, 0X308B, 0X0210, 0X1399, 0X6726, 0X76AF, 0X4434, 0X55BD,
            0XAD4A, 0XBCC3, 0X8E58, 0X9FD1, 0XEB6E, 0XFAE7, 0XC87C, 0XD9F5,
            0X3183, 0X200A, 0X1291, 0X0318, 0X77A7, 0X662E, 0X54B5, 0X453C,
            0XBDCB, 0XAC42, 0X9ED9, 0X8F50, 0XFBEF, 0XEA66, 0XD8FD, 0XC974,
            0X4204, 0X538D, 0X6116, 0X709F, 0X0420, 0X15A9, 0X2732, 0X36BB,
            0XCE4C, 0XDFC5, 0XED5E, 0XFCD7, 0X8868, 0X99E1, 0XAB7A, 0XBAF3,
            0X5285, 0X430C, 0X7197, 0X601E, 0X14A1, 0X0528, 0X37B3, 0X263A,
            0XDECD, 0XCF44, 0XFDDF, 0XEC56, 0X98E9, 0X8960, 0XBBFB, 0XAA72,
            0X6306, 0X728F, 0X4014, 0X519D, 0X2522, 0X34AB, 0X0630, 0X17B9,
            0XEF4E, 0XFEC7, 0XCC5C, 0XDDD5, 0XA96A, 0XB8E3, 0X8A78, 0X9BF1,
            0X7387, 0X620E, 0X5095, 0X411C, 0X35A3, 0X242A, 0X16B1, 0X0738,
            0XFFCF, 0XEE46, 0XDCDD, 0XCD54, 0XB9EB, 0XA862, 0X9AF9, 0X8B70,
            0X8408, 0X9581, 0XA71A, 0XB693, 0XC22C, 0XD3A5, 0XE13E, 0XF0B7,
            0X0840, 0X19C9, 0X2B52, 0X3ADB, 0X4E64, 0X5FED, 0X6D76, 0X7CFF,
            0X9489, 0X8500, 0XB79B, 0XA612, 0XD2AD, 0XC324, 0XF1BF, 0XE036,
            0X18C1, 0X0948, 0X3BD3, 0X2A5A, 0X5EE5, 0X4F6C, 0X7DF7, 0X6C7E,
            0XA50A, 0XB483, 0X8618, 0X9791, 0XE32E, 0XF2A7, 0XC03C, 0XD1B5,
            0X2942, 0X38CB, 0X0A50, 0X1BD9, 0X6F66, 0X7EEF, 0X4C74, 0X5DFD,
            0XB58B, 0XA402, 0X9699, 0X8710, 0XF3AF, 0XE226, 0XD0BD, 0XC134,
            0X39C3, 0X284A, 0X1AD1, 0X0B58, 0X7FE7, 0X6E6E, 0X5CF5, 0X4D7C,
            0XC60C, 0XD785, 0XE51E, 0XF497, 0X8028, 0X91A1, 0XA33A, 0XB2B3,
            0X4A44, 0X5BCD, 0X6956, 0X78DF, 0X0C60, 0X1DE9, 0X2F72, 0X3EFB,
            0XD68D, 0XC704, 0XF59F, 0XE416, 0X90A9, 0X8120, 0XB3BB, 0XA232,
            0X5AC5, 0X4B4C, 0X79D7, 0X685E, 0X1CE1, 0X0D68, 0X3FF3, 0X2E7A,
            0XE70E, 0XF687, 0XC41C, 0XD595, 0XA12A, 0XB0A3, 0X8238, 0X93B1,
            0X6B46, 0X7ACF, 0X4854, 0X59DD, 0X2D62, 0X3CEB, 0X0E70, 0X1FF9,
            0XF78F, 0XE606, 0XD49D, 0XC514, 0XB1AB, 0XA022, 0X92B9, 0X8330,
            0X7BC7, 0X6A4E, 0X58D5, 0X495C, 0X3DE3, 0X2C6A, 0X1EF1, 0X0F78)
        if isinstance(value, list):
            pass
        else:
            value = list(value)
        l = len(value)
        jiange = int(l / 2)
        right = 0
        data = []
        for i in range(jiange):
            left = right
            right = 2 * (1 + i)
            data.append('0x' + ''.join(value[left:right]))
        crc = 0xffff
        for byte in (int(c, 16) for c in data):
            crc = (crc >> 8) ^ my_table[(crc ^ byte) & 0xff]
        return_h = (~crc) & 0xffff
        dat1 = hex(return_h)[2:]
        if len(dat1) == 3:
            dat1 = "0" + dat1
        elif len(dat1) == 2:
            dat1 = '00' + dat1
        elif len(dat1) == 1:
            dat1 = '000' + dat1
        elif len(dat1) == 0:
            dat1 = '0000'
        return dat1

    # </editor-fold>
    # <editor-fold desc="经纬度转换">
    def lon_lat_transition(self, data):
        if data.startswith('0x'):
            pass
        else:
            data = '0x' + data
        latitude_int10 = BaseConversion().hex_to_int(data)
        latitude = int((latitude_int10 / 30000) / 60) + round(
            round((latitude_int10 / 30000) % 60, 4) / 60,
            6)
        return latitude

    # </editor-fold>


# 字符串判断
class StringJudge(object):
    # <editor-fold desc="所有字符都是数字或者字母">
    @staticmethod
    def isalnum(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isalnum()

    # </editor-fold>
    # <editor-fold desc="所有字符都是字母">
    @staticmethod
    def isalpha(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isalpha()

    # </editor-fold>
    # <editor-fold desc="所有字符都是数字">
    @staticmethod
    def isdigit(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isdigit()

    # </editor-fold>
    # <editor-fold desc="所有字符都是小写">
    @staticmethod
    def islower(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.islower()

    # </editor-fold>
    # <editor-fold desc="所有字符都是大写">
    @staticmethod
    def isupper(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isupper()

    # </editor-fold>
    # <editor-fold desc="所有单词都是首字母大写，像标题">
    @staticmethod
    def istitle(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.istitle()

    # </editor-fold>
    # <editor-fold desc="所有字符都是空白字符、\t、\n、\r">
    @staticmethod
    def isspace(str):
        """
        :param str: 字符串
        :return:True
        """
        return str.isspace()
    # </editor-fold>
