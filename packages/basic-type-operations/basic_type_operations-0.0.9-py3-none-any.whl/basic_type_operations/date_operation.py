# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : date_operation.py 
@PRODUCT_NAME : PyCharm 
"""
# from django.utils import timezone
import datetime, calendar, time, pytz
from dateutil.relativedelta import relativedelta
from .number_operation import NumberOperation


# <editor-fold desc="日期类工具">
class DateOperation(object):
    @staticmethod
    def isVaildDate(date):
        try:
            if ":" in date:
                time.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(date, "%Y%m%d")
            return True
        except:
            return False

    # <editor-fold desc="判断是否满足时间格式">
    @staticmethod
    def valid_date(date, formatstr):
        """
            判断是否满足时间格式
        :param date:
        :param formatstr:格式串
        :return:
        """
        try:
            datetime.datetime.strptime(date, formatstr)
            return True
        except Exception as e:
            return False

    # </editor-fold>
    # <editor-fold desc="计算">
    # <editor-fold desc="计算整分钟，整小时，整天的时间">
    @staticmethod
    def get_hourly_chime(dt, step=0, rounding_level="s"):
        """
        计算整分钟，整小时，整天的时间
        :param step: 往前或往后跳跃取整值，默认为0，即当前所在的时间，正数为往后，负数往前。
                    例如：
                    step = 0 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:21
                    step = 1 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:22
                    step = -1 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:20
        :param rounding_level: 字符串格式。
                    "s": 按秒取整；"min": 按分钟取整；"hour": 按小时取整；"days": 按天取整
        :return: 整理后的时间
        """
        if rounding_level == "days":  # 整天
            td = datetime.timedelta(days=-step, seconds=dt.second, microseconds=dt.microsecond, milliseconds=0,
                                    minutes=dt.minute,
                                    hours=dt.hour, weeks=0)
            new_dt = dt - td
        elif rounding_level == "hour":  # 整小时
            td = datetime.timedelta(days=0, seconds=dt.second, microseconds=dt.microsecond, milliseconds=0,
                                    minutes=dt.minute,
                                    hours=-step, weeks=0)
            new_dt = dt - td
        elif rounding_level == "min":  # 整分钟
            td = datetime.timedelta(days=0, seconds=dt.second, microseconds=dt.microsecond, milliseconds=0,
                                    minutes=-step,
                                    hours=0,
                                    weeks=0)
            new_dt = dt - td
        elif rounding_level == "s":  # 整秒
            td = datetime.timedelta(days=0, seconds=-step, microseconds=dt.microsecond, milliseconds=0, minutes=0,
                                    hours=0,
                                    weeks=0)
            new_dt = dt - td
        else:
            new_dt = dt
        # timestamp = new_dt.timestamp()  # 对于 python 3 可以直接使用 timestamp 获取时间戳
        # timestamp = (new_dt - datetime.fromtimestamp(0)).total_seconds()  # Python 2 需手动换算
        return new_dt

    # </editor-fold>
    # <editor-fold desc="计算时间间隔 f"{hours}时{minute}分"">
    @staticmethod
    def time_differ(end, start):
        if end and start:
            seconds = (end - start).seconds
            hours = int(seconds / 60 / 60)
            minute = int(seconds / 60) - 60 * hours
            hours += (end - start).days * 24
            return f"{hours}时{minute}分"
        else:
            return f"{0}时{0}分"

    # </editor-fold>
    # <editor-fold desc="某年的开始和结束">
    @staticmethod
    def year_top_tail(date=None):
        if not date:
            date = datetime.datetime.now()
        if isinstance(date, int):
            date = datetime.datetime(year=date, month=1, day=1)
        _, last_month_of_days = calendar.monthrange(date.year, 12)
        first_day_year = datetime.date(year=date.year, month=1, day=1).strftime("%Y-%m-%d")
        last_day_year = datetime.date(year=date.year, month=12, day=last_month_of_days).strftime("%Y-%m-%d")
        return first_day_year, last_day_year

    # </editor-fold>
    # <editor-fold desc="近几年开始和结束">
    @staticmethod
    def near_year_top_tail(last_date=None, near_type=1):
        """
            :param date:
            :param near_type: 1 近一年 ，2 近2年，1/2 近半年
            :return:
            """
        if not last_date:
            last_date = datetime.datetime.now().replace(microsecond=0)
        # month = last_date.month
        if isinstance(near_type, int):
            first_day_year = last_date - relativedelta(years=near_type)
        elif isinstance(near_type, float):
            years, months = NumberOperation.divmoddef(near_type)
            first_day_year = last_date - relativedelta(years=years, months=int(months * 12))
        return first_day_year, last_date

    # </editor-fold>
    # <editor-fold desc="某季度开始和结束">
    @staticmethod
    def quarter_top_tail(date=None):
        # 获取本季度第一天和最后一天
        if not date:
            date = datetime.datetime.now()
        month = date.month
        if month in [1, 2, 3]:
            quarter_start = datetime.date(date.year, 1, 1).strftime("%Y-%m-%d")
            quarter_end = (datetime.date(date.year, 4, 1) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        elif month in [4, 5, 6]:
            quarter_start = datetime.date(date.year, 4, 1).strftime("%Y-%m-%d")
            quarter_end = (datetime.date(date.year, 7, 1) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        elif month in [7, 8, 9]:
            quarter_start = datetime.date(date.year, 7, 1).strftime("%Y-%m-%d")
            quarter_end = (datetime.date(date.year, 10, 1) - datetime.timedelta(days=1)).strftime(
                "%Y-%m-%d")
        elif month in [10, 11, 12]:
            quarter_start = datetime.date(date.year, 10, 1).strftime("%Y-%m-%d")
            quarter_end = (datetime.date(date.year + 1, 1, 1) - datetime.timedelta(days=1)).strftime(
                "%Y-%m-%d")
        else:
            raise ValueError(f"The month {month} is incorrect")
        return quarter_start, quarter_end

    # </editor-fold>
    # <editor-fold desc="某月开始和结束日期">
    @staticmethod
    def month_top_tail(date=None):
        if not date:
            date = datetime.date.today()
        month = date.month
        year = date.year
        # 获取当月第一天的星期和当月的总天数
        firstDayWeekDay, monthRange = calendar.monthrange(year, month)
        # 获取当月的第一天
        firstDay = datetime.date(year=year, month=month, day=1)
        lastDay = datetime.date(year=year, month=month, day=monthRange)
        return firstDay, lastDay

    # </editor-fold>
    # <editor-fold desc="某天开始和结束">
    @staticmethod
    def day_top_tail(date=None, days=1):
        if not date:
            date = datetime.datetime.now()
        days = days - 1
        date = date - datetime.timedelta(days=days)
        data_start = date.replace(hour=0, second=0, minute=0, microsecond=0)
        data_end = date.replace(hour=23, second=59, minute=59, microsecond=0) + datetime.timedelta(days=days)
        return data_start, data_end

    # </editor-fold>
    # <editor-fold desc="某周的开始和结束">
    @staticmethod
    def week_top_tail(date=None):
        # 获取当前周第一天和最后一天
        if not date:
            date = datetime.datetime.now()
        week_start = (date - datetime.timedelta(days=date.weekday())).strftime("%Y-%m-%d")
        week_end = (date + datetime.timedelta(days=6 - date.weekday())).strftime("%Y-%m-%d")
        return week_start, week_end

    # </editor-fold>
    # <editor-fold desc="当前时间第几年第几周的计算">
    @staticmethod
    def getYearWeek(date=None):
        """

        :param date:
        :return: 当前日期执行的结果为(2014, 35, 4) 分别代表2014年第35周星期4
        """
        if not date:
            date = datetime.datetime.now()
        NowYearWeek = date.isocalendar()
        return NowYearWeek
        # </editor-fold>

    # </editor-fold>
    # <editor-fold desc="某月的天数">
    @staticmethod
    def month_days(date=None):
        if not date:
            date = datetime.date.today()
        # 获取当月第一天的星期和当月的总天数
        month = date.month
        year = date.year
        firstDayWeekDay, monthRange = calendar.monthrange(year, month)
        return monthRange

    # </editor-fold>
    # <editor-fold desc="开始和结束相差的天数">
    @staticmethod
    def two_time_days(start_time, end_time):
        days = (end_time - start_time).days
        return days

    # </editor-fold>
    # <editor-fold desc="当前时间的整点时间">
    @staticmethod
    def times_now_hour():
        date = datetime.datetime.now().replace(minute=0, second=0)
        return date

    # </editor-fold>
    # <editor-fold desc="返回指定时间">
    @staticmethod
    def input_year_now(year=2021, month=3, day=23, hour=2, minute=0, second=0, microsecond=0, fold=0):
        date = datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            # fold=fold
        )
        return date

    # </editor-fold>
    # <editor-fold desc="判断闰年">
    @staticmethod
    def determine_leap_year(year):
        '''
        输入年份，判断是否是闰年。闰年判断方法：能被4整除，但不能被100整除；或者能被 400 整除。需要用到算术运算符和逻辑运算符
        :param year:
        :return:
        '''
        is_leap = year % 4 == 0 and year % 100 != 0 or year % 400 == 0
        return is_leap

    # </editor-fold>
    # <editor-fold desc="间隔相同天数时间">
    @staticmethod
    def datetime_interval_same_day(start_time, days):
        now_time = datetime.datetime.now()
        return now_time - datetime.timedelta(days=(now_time - start_time).days % days)

    # </editor-fold>
    # <editor-fold desc="距离 某时 多少分钟前">
    @staticmethod
    def how_minutes_before_to_now(date=None, minutes=10):
        if not date:
            date = datetime.datetime.now()
        data_start = date - datetime.timedelta(minutes=minutes)
        data_end = date
        return data_start, data_end

    # </editor-fold>
    # <editor-fold desc="加8个小时">
    @staticmethod
    def add_time_hours(date=None, hours=8, ):
        if not date:
            date = datetime.datetime.now()
        return date + datetime.timedelta(hours=hours)

    # </editor-fold>
    # <editor-fold desc="加几天">
    @staticmethod
    def add_time_days(date=None, days=0, ):
        if not date:
            date = datetime.datetime.now()
        return date + datetime.timedelta(days=days)

    # </editor-fold>
    # <editor-fold desc="休眠时间">
    @staticmethod
    def sleeptime(days=0, hour=0, min=0, sec=0):
        return days * 24 * 3600 + hour * 3600 + min * 60 + sec

    # </editor-fold>
    # <editor-fold desc="今天开始到现在共多少秒">
    @staticmethod
    def today_top_now_second(date=None, ):
        if not date:
            date = datetime.datetime.now()
        second = date.second
        hour = date.hour
        minute = date.minute
        return hour * 60 * 60 + minute * 60 + second

    # </editor-fold>
    # <editor-fold desc="判断在不在当前的时间段之中附近">
    @staticmethod
    def how_minutes_between(date=None, days=0, hours=0, minutes=0, seconds=0):
        if not date:
            date = datetime.datetime.now()
        now_data_time = datetime.datetime.now()
        data_start = now_data_time - datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        data_end = now_data_time + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        if date >= data_start and date <= data_end:
            return True
        else:
            return False

    # </editor-fold>
    # <editor-fold desc="判断时间是在开始时间和结束时间的位置">
    @staticmethod
    def judge_date_range(date: datetime.datetime, start_time: datetime.datetime, end_time: datetime.datetime):
        """
        :param date:
        :param start_time:
        :param end_time:
        :return: 0  date 小于时间段
                  1   data 再时间段中间
                  2  data  大于时间段
        """
        if date < start_time:
            return 0
        elif date < end_time:
            return 1
        else:
            return 2

    # </editor-fold>
    # <editor-fold desc="时间返回year month days hours minute sec">
    @staticmethod
    def time_all_args(date):
        year = date.year
        month = date.month
        days = date.day
        hours = date.hour
        minutes = date.minute
        second = date.second
        if str(month).__len__() == 1:
            month = '0' + str(month)
        if str(days).__len__() == 1:
            days = '0' + str(days)
        if str(minutes).__len__() == 1:
            minutes = '0' + str(minutes)
        if str(hours).__len__() == 1:
            hours = '0' + str(hours)
        if str(second).__len__() == 1:
            second = '0' + str(second)
        return year, month, days, hours, minutes, second

    # </editor-fold>
    # <editor-fold desc="单个时间转时间区间 - 往前推三天">
    @staticmethod
    def time_to_interval(list_date):
        # 原序去重
        list_date = list({}.fromkeys(list_date).keys())
        return [[date - datetime.timedelta(days=3), date] for date in list_date]

    # </editor-fold>

    # </editor-fold>
    # <editor-fold desc="时间格式   转   字符串格式">
    # <editor-fold desc="返回年2020">
    @staticmethod
    def times_year(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y}'.format(date)

    # </editor-fold>
    # <editor-fold desc="返回年月2020-10">
    @staticmethod
    def times_year_month(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y-%m}'.format(date)

    # </editor-fold>
    # <editor-fold desc="返回年月日2020-10-10">
    @staticmethod
    def times_year_days(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y-%m-%d}'.format(date)

    # </editor-fold>
    # <editor-fold desc="返回年月日 时2020-10-10 10">
    @staticmethod
    def times_year_hours(date=None, format='{:%Y-%m-%d %H}'):
        if not date:
            date = datetime.datetime.now()
        return format.format(date)

    # </editor-fold>
    # <editor-fold desc="年月日时分2020-10-10 10:10">
    @staticmethod
    def times_year_minute(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y-%m-%d %H:%M:%S}'.format(date)

    # </editor-fold>
    # <editor-fold desc="年月日时分秒2020-10-10 10:10:10">
    @staticmethod
    def times_year_second(date=None, ):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y-%m-%d %H:%M:%S}'.format(date)

    # </editor-fold>
    # <editor-fold desc="年月日时分秒20201010101010">
    @staticmethod
    def times_year_second_K(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y%m%d%H%M%S}'.format(date)

    # </editor-fold>
    # <editor-fold desc="年月日时分秒20201010-101010">
    @staticmethod
    def times_year_second_joinK(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y%m%d-%H%M%S}'.format(date)

    # </editor-fold>
    # <editor-fold desc="返回月-日10-10">
    @staticmethod
    def times_nouth_day(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%m-%d}'.format(date)

    # </editor-fold>
    # <editor-fold desc="返回月-秒10-10 10:10:10">
    @staticmethod
    def times_month_second(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%m-%d %H:%M:%S}'.format(date)

    # </editor-fold>
    # <editor-fold desc="返回时分10:10">
    @staticmethod
    def times_hour_minute(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%H:%M}'.format(date)

    # </editor-fold>
    # <editor-fold desc="返回时分秒10:10:10">
    @staticmethod
    def times_hour_second(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%H:%M:%S}'.format(date)

    # </editor-fold>
    # <editor-fold desc="返回时分秒10:10:10.56789">
    @staticmethod
    def times_hour_second_f(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%H:%M:%S.%f}'.format(date)

    # </editor-fold>
    # <editor-fold desc="时间返回全部2020-10-10T10:10:10.56789">
    @staticmethod
    def times_year_T_f(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y-%m-%dT%H:%M:%S.%f}'.format(date)

    # </editor-fold>
    # <editor-fold desc="时间返回全部2020-10-10 10:10:10.56789Z">
    @staticmethod
    def times_year_f_Z(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y-%m-%d %H:%M:%S.%fZ}'.format(date)

    # </editor-fold>
    # <editor-fold desc="时间返回全部2020-10-10T10:10:10.56789Z">
    @staticmethod
    def times_year_T_f_Z(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y-%m-%dT%H:%M:%S.%fZ}'.format(date)

    # </editor-fold>
    # <editor-fold desc="时间返回全部2020-10-10 10:10:10.56789">
    @staticmethod
    def times_year_f(date=None):
        if not date:
            date = datetime.datetime.now()
        return '{:%Y-%m-%d %H:%M:%S.%f}'.format(date)

    # </editor-fold>
    # </editor-fold>
    # <editor-fold desc="字符串格式  转   时间格式">
    # <editor-fold desc="2019-02-13T07:57:10.276212">
    @staticmethod
    def string_year_second_f(date_str):
        UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
        utcTime = datetime.datetime.strptime(date_str, UTC_FORMAT)
        localtime = '{:%Y-%m-%d %H:%M:%S}'.format(utcTime)
        # return localtime
        return DateOperation.string_year_second(localtime)

    # </editor-fold>
    # <editor-fold desc="2019-02-13T07:57:10.276212Z">
    @staticmethod
    def string_year_second_fZ(date_str):
        UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        utcTime = datetime.datetime.strptime(date_str, UTC_FORMAT)
        localtime = '{:%Y-%m-%d %H:%M:%S}'.format(utcTime)
        return DateOperation.string_year_second(localtime)

    # </editor-fold>
    # <editor-fold desc="2021-02-01 10:10:10">
    @staticmethod
    def string_year_second(date_str):
        # print("2.把字符串转成datetime: ", datetime.strptime(st, "%Y:%m:%d %H:%M:%S"))
        if isinstance(date_str, datetime.datetime):
            return date_str
        else:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # </editor-fold>
    # <editor-fold desc="接受的格式为2021-02-03">
    @staticmethod
    def string_year_days(date_str, params=True):
        if isinstance(date_str, datetime.datetime):
            return date_str
        else:
            # 某天开始的时间
            if params:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d")
            # 某天结束的时间
            else:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d") + datetime.timedelta(
                    days=1) - datetime.timedelta(
                    seconds=1)

    # </editor-fold>
    # <editor-fold desc="2021-02">
    @staticmethod
    def string_year_month(date_str):
        if isinstance(date_str, datetime.datetime):
            return date_str
        else:
            return datetime.datetime.strptime(date_str, "%Y-%m")

    # </editor-fold>
    # <editor-fold desc="2021-03-03 17:01:59.416260">
    @staticmethod
    def string_year_second_f_string(date_str: str):
        return date_str.split(' ')[1][:5]

    # print(string_year_second_f_string('2021-03-03 17:01:59.416260'))
    # </editor-fold>
    # </editor-fold>
    # <editor-fold desc="整形转时间">
    @staticmethod
    def xldate_as_datetime(xldate, datemode):
        """
        示例 xldate_as_datetime(44863, 0)
        :param xldate:
        :param datemode:
        :return:
        """
        epoch_1904 = datetime.datetime(1904, 1, 1)
        epoch_1900 = datetime.datetime(1899, 12, 31)
        epoch_1900_minus_1 = datetime.datetime(1899, 12, 30)
        # Set the epoch based on the 1900/1904 datemode.
        if datemode:
            epoch = epoch_1904
        else:
            if xldate < 60:
                epoch = epoch_1900
            else:
                # Workaround Excel 1900 leap year bug by adjusting the epoch.
                epoch = epoch_1900_minus_1

        # The integer part of the Excel date stores the number of days since
        # the epoch and the fractional part stores the percentage of the day.
        days = int(xldate)
        fraction = xldate - days

        # Get the the integer and decimal seconds in Excel's millisecond resolution.
        seconds = int(round(fraction * 86400000.0))
        seconds, milliseconds = divmod(seconds, 1000)

        return epoch + datetime.timedelta(days, seconds, 0, milliseconds)

    # </editor-fold>
    # <editor-fold desc="国际时间转换">
    # <editor-fold desc="格林威治时间-转-北京时间 '2022-03-22T06:00:44.528Z'-> 2022-03-22 14:00:44">
    @staticmethod
    def UTC2BJS(UTC):

        UTC_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        BJS_format = "%Y-%m-%d %H:%M:%S"
        UTC = datetime.datetime.strptime(UTC, UTC_format)
        # 格林威治时间+8小时变为北京时间
        BJS = UTC + datetime.timedelta(hours=8)
        BJS = BJS.strftime(BJS_format)
        return BJS

    # </editor-fold>
    # <editor-fold desc="BJS2UTC 北京时间-转 格林威治时间">
    @staticmethod
    def BJS2UTC(BJS):
        UTC_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        BJS_format = "%Y-%m-%d %H:%M:%S"
        BJS = datetime.datetime.strptime(BJS, BJS_format)
        # 北京时间-8小时变为格林威治时间
        UTC = BJS - datetime.timedelta(hours=8)
        UTC = UTC.strftime(UTC_format)
        return UTC

    # </editor-fold>
    # <editor-fold desc=" UTC 获取格林威治时间  2022-01-18T06:23:01+0000 2022-01-18 06:23:01.733507+00:00 格式">
    @staticmethod
    def UTCISOTime():
        utc_tz = pytz.timezone('UTC')
        # datetime.datetime.now(tz=utc_tz)
        utcnow = datetime.datetime.now(tz=utc_tz)
        # utc_date =(utcnow-) .isoformat()
        return utcnow.strftime('%Y-%m-%dT%H:%M:%S%z')

    # </editor-fold>
    # <editor-fold desc="UTC 2021-12-23T11:13:24+0000 -转换成 2021-12-23T11:13:24 ">
    @staticmethod
    def utc_local_date(utc_data1):
        t = utc_data1[:19]
        utc_date2 = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S")
        local_date = utc_date2 + datetime.timedelta(hours=8)
        return local_date

    # </editor-fold>
    # </editor-fold>
    # <editor-fold desc="把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'">
    @staticmethod
    def TimeStampToTime(timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    # </editor-fold>
    def timeOffsetAndStruct(self, strtimes, format="%Y-%m-%d %H:%M:%S", offset=0):
        return time.localtime(time.mktime(time.strptime(strtimes, format)) + offset)

    # <editor-fold desc="获取两个日期之间的月份列表">
    @staticmethod
    def get_month_range(start_day: datetime.date, end_day: datetime.date):
        """
            start_day 开始日期
            end_day   结束日期

            return: List
                例：['2016-1','2016-2','2016-3','2016-4','2016-5','2016-6']
        """
        months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
        month_range = ['%s-%s' % (start_day.year + mon // 12, mon % 12 + 1)
                       for mon in range(start_day.month - 1, start_day.month + months)]
        return month_range

    # </editor-fold>
    # <editor-fold desc="获取两个日期之间的日期列表">
    @staticmethod
    def get_day_range(begin_date: datetime.date, end_date: datetime.date):
        """
            start_day 开始日期
            end_day   结束日期

            return: List
                例：['2016-10-01','2016-10-02',....]
        """
        date_list = []
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    # </editor-fold>
    # <editor-fold desc="获取两个日期之间的日期列表">
    @staticmethod
    def get_week_range(begin_date: datetime.date, end_date: datetime.date):
        """
            start_day 开始日期
            end_day   结束日期

            return: List   format: '%Y-%W'
                例：['2016-30','2016-31',....]
        """
        week_list = []
        while begin_date <= end_date:
            week_str = begin_date.strftime("%Y-%W")
            week_list.append(week_str)
            begin_date += datetime.timedelta(days=7)
        return week_list
    # </editor-fold>
# </editor-fold>
