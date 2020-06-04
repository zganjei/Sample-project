# -*- coding: utf-8 -*-
from django.conf import settings




def register_children():
    for app in settings.INSTALLED_APPS:
        try:
            __import__(app + '.managers')
        except ImportError as s:
            pass
            # if type(s) is not ModuleNotFoundError:
            #     print(type(s))
            #     print(s)
