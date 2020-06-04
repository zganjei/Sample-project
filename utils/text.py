# Users
import re
import textwrap

username_flags = re.ASCII | re.IGNORECASE
AT_SIGNS = r'[@\uff20]'
LIST_END_CHARS = r'([a-z0-9_]{1,20})(/[a-z][a-z0-9\x80-\xFF-]{0,79})?'
USERNAME_REGEX = re.compile(r'\B' + AT_SIGNS + LIST_END_CHARS, username_flags)
# Hashtags
HASHTAG_SIGNS = r'[#\uff03]'
# HASHTAG_REGEX = re.compile(r'\B' + HASHTAG_SIGNS + LIST_END_CHARS, username_flags)
HASHTAG_REGEX = re.compile(r"#(\w+)", re.IGNORECASE)


def text_to_price(val):
    if val is None:
        val = ''
    val = str(val)
    if val.isdigit():
        val = str(int(val))
    return '،'.join(textwrap.wrap(val[::-1], 3))[::-1]


def text_to_price_show(val):
    price = text_to_price(val)
    return '%s ریال' % price


def rate_text_float(val):
    if val:
        float_val = float("%.1f" % val)
        if float_val == int(float_val):
            return int(float_val)
        return "%.1f" % val
    return 0


def check_code_meli(code: str):
    code = str(code)
    code_len = len(code)
    if code_len < 8 or not code.isdigit(): return False;
    code = ('0000' + str(code))[code_len + 4 - 10:]
    if not code[3:9].isdigit(): return False

    c = int(code[9:10])
    s = 0
    for i in range(9):
        s += int(code[i:i + 1], 10) * (10 - i)
    s = s % 11
    return (s < 2 and c == s) or (s >= 2 and c == (11 - s))
