# -*- coding: utf-8 -*-
import datetime

import pytz
from django import template

from utils.calverter import Calverter, JALALI_WEEKDAYS, gregorian_to_jalalimonthday, \
    gregorian_to_jalali, gregorian_to_jalaliyearmonth, gregorian_to_jalaliyearmonthday, gregorian_to_jalaliyear

register = template.Library()


@register.filter
def persian_date(date):
    date_converter = Calverter()
    jd = date_converter.gregorian_to_jd(date.year, date.month, date.day)
    sh_date = date_converter.jd_to_jalali(jd)
    week_day = date_converter.jwday(jd)
    day_name = JALALI_WEEKDAYS[week_day]
    st = str(sh_date[0]) + "/" + str(sh_date[1]) + "/" + str(sh_date[2])
    return "امروز، %s %s" % (day_name, st)


@register.filter
def pdate(date):
    if not date:
        return ''
    # if isinstance(date, datetime.datetime):
    #     date = datetime.datetime.now()
    return gregorian_to_jalali(date)


@register.filter
def ptime(date):
    if not date:
        return ''

    date = date.astimezone(pytz.timezone("Asia/Tehran"))

    return date.strftime('%H:%M')


@register.filter
def pdate_daymonth(date):
    return gregorian_to_jalalimonthday(date)


@register.simple_tag
def get_current_date_time():
    date = datetime.datetime.now()
    date_converter = Calverter()
    jd = date_converter.gregorian_to_jd(date.year, date.month, date.day)
    sh_date = date_converter.jd_to_jalali(jd)
    week_day = date_converter.jwday(jd)
    day_name = JALALI_WEEKDAYS[week_day]
    st = str(sh_date[0]) + "/" + str(sh_date[1]) + "/" + str(sh_date[2])
    return "اکنون، %s %s ساعت %s و %s دقیقه" % (day_name, st, date.time().hour, date.time().minute)


@register.filter
def pdate_year_month(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalaliyearmonth(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value


@register.filter
def pdate_year_month_day(value, sep=' '):
    if isinstance(value, datetime.date):
        return gregorian_to_jalaliyearmonthday(value, sep)
    if value is None or value == 'None' or value == '':
        return '---'
    return value


@register.filter
def pdate_if_date(value, default='---'):
    if isinstance(value, datetime.date):
        return gregorian_to_jalali(value)
    if value is None or value == 'None' or value == '':
        return default
    return value


@register.filter
def pdate_if_date_with_time(value):
    if isinstance(value, datetime.datetime):
        persian_date = gregorian_to_jalali(value)
        persian_time = ptime(value)
        # if persian_time:
        #     persian_time = persian_time.strftime("%H:%M")
        return str(persian_time) + ' ' + persian_date
    if value is None or value == 'None' or value == '':
        return '---'
    return value


@register.filter
def pdate_year(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalaliyear(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value
