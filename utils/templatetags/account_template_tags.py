# -*- coding:utf-8 -*-
import datetime
import math

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import stringfilter
from django.utils import formats
from django.utils.html import avoid_wrapping

# from account.menus import MenuHandler
# from messaging.models import MessageThread
# from product.models import StaticPage
from utils.calverter import gregorian_to_jalaliyear
from utils.text import text_to_price



register = template.Library()


@register.filter
def get_dict(input_dict, key):
    return input_dict.get(key)


@register.simple_tag
def welcome_st(user):
    overall_name = u"%s %s" % (user.first_name, user.last_name) if (
            user.first_name and user.last_name) else u"%s" % user.username
    return u"%s خوش آمدید." % overall_name


# @register.filter
# def user_menus(user):
#     return MenuHandler.get_user_menus(user)


@register.filter
def is_false(value):
    return value is False or value == 'False'


@register.filter
def is_true(value):
    return value is True


@register.filter
def get_field(instance, name):
    return getattr(instance, name).all()


@register.filter
def show_m2m(value):
    return u', '.join([str(d) for d in value.all()])


@register.filter
def filename(file_val):
    import os
    if not file_val:
        return ''
    return os.path.basename(file_val.name)


@register.filter
def get_verbose_name_by_name(instance, name):
    return instance._meta.get_field(name).verbose_name


@register.filter(is_safe=True)
def filesizeformat_persian(bytes):
    try:
        filesize_number_format = lambda value: formats.number_format(round(value, 1), 1)

        KB = 1 << 10
        MB = 1 << 20
        GB = 1 << 30
        TB = 1 << 40
        PB = 1 << 50

        if bytes < KB:
            value = "%s بایت" % filesize_number_format(bytes / KB)
        elif bytes < MB:
            value = "%s کیلوبایت" % filesize_number_format(bytes / KB)
        elif bytes < GB:
            value = "%s مگابایت" % filesize_number_format(bytes / MB)
        elif bytes < TB:
            value = "%s گیگابایت" % filesize_number_format(bytes / GB)
        elif bytes < PB:
            value = "%s ترابایت" % filesize_number_format(bytes / TB)
        else:
            value = "%s پنتابایت" % filesize_number_format(bytes / PB)

        return avoid_wrapping(value)
    except:
        return 0


@register.filter
def tostringrate(value):
    return str(int(value))


@register.filter
def get_range(value):
    return range(value)


@register.filter
def discount(val1, val2):
    return val1 - val2


@register.filter
def multiply(val1, val2):
    val1 = val1 or 0
    val2 = val2 or 0
    return val1 * val2


@register.simple_tag
def division(val1, val2, max_res=None):
    val1 = val1 or 0
    val2 = val2 or 1
    res = math.floor(val1 / val2)
    if max_res and res > max_res:
        return max_res
    else:
        return res


@register.filter
def to_int(val):
    try:
        return int(val)
    except:
        return val


@register.filter
def to_str(val):
    return str(val)


@register.filter
def get_years(val):
    try:
        val = int(val)
        year = int(gregorian_to_jalaliyear(datetime.date.today()))
        res = []
        for i in range(val):
            res.append(year - i)
        res = reversed(res)
        return res
    except:
        return []


@register.filter
def max_str(val, size):
    if not val:
        return val
    if len(str(val)) > size:
        return str(val)[:size] + "..."
    else:
        return str(val)


@register.filter
def file_name(file):
    if '/' in (file.name or ''):
        return file.name.split('/')[-1]
    return file.name


@register.filter
def phone_mobile(phone):
    if len(phone) == 11:
        return phone[:4] + '-' + phone[4:7] + '-' + phone[7:]
    return phone


@register.filter(is_safe=True)
@stringfilter
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')


@register.filter
def price(text):
    return text_to_price(text)


@register.filter
def toman_price(text):
    return text_to_price(division(text, 10))


@register.filter
def split(text: str):
    return text.split()

# @register.filter
# def get_badge(menu_item, user):
#     return MenuHandler.get_badge(menu_item, user)


# @register.filter
# def has_inbox_permission(user):
#     try:
#         return user.staff.role.menu_permissions.filter(url_name='inbox').exists()
#     except (ObjectDoesNotExist, AttributeError):
#         return False

# @register.simple_tag(takes_context=True)
# def get_unread_messages_count(context):
#     if 'request' in context:
#         request = context['request']
#         if not request.user.is_authenticated:
#             return 0
#         return MessageThread.unread_count(request.user)


# @register.simple_tag
# def get_static_pages():
#     return StaticPage.objects.filter(active=True, show=True).only('id', 'title', 'url')
