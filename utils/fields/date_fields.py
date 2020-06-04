# -*- coding:utf-8 -*-
import datetime

from django.utils.safestring import mark_safe
from utils.calverter import jalali_to_gregorian, gregorian_to_jalali, jalali_time_to_gregorian, gregorian_to_jalali_time


from django import forms


class ShamsiWidget(forms.DateInput):
    def render(self, name, value, attrs=None, renderer=None):
        value = gregorian_to_jalali(value)
        html = super(ShamsiWidget, self).render(name, value, attrs, renderer)
        js = """
        <script type='text/javascript'>
        $('#id_%s').MdPersianDateTimePicker({
            Placement: 'bottom',
            Trigger: 'click',
            TargetSelector: '#id_%s',
            EnableTimePicker: false,
            Disabled: false,
            Format: 'yyyy/MM/dd',
            ToDate: false,
            FromDate: false,
            IsGregorian: false,
            EnglishNumber: false,
        });
        </script>
        """ % (name, name)
        return mark_safe(u"%s %s" % (html, js))

    def value_from_datadict(self, data, files, name):
        shamsi_val = data.get(name, None)
        miladi_val = jalali_to_gregorian(shamsi_val)
        if miladi_val:
            return miladi_val.isoformat()
        else:
            return miladi_val


class ShamsiDateField(forms.DateField):
    widget = ShamsiWidget

    def to_python(self, value):
        return super(ShamsiDateField, self).to_python(value)


class ShamsiDateTimeWidget(forms.DateTimeInput):
    def render(self, name, value, attrs=None, renderer=None):
        value = gregorian_to_jalali_time(value, apply_timezone=True)
        html = super(ShamsiDateTimeWidget, self).render(name, value, attrs, renderer)
        js = """
        <script type='text/javascript'>
        $('#id_%s').MdPersianDateTimePicker({
            Placement: 'bottom',
            Trigger: 'click',
            TargetSelector: '#id_%s',
            EnableTimePicker: true,
            Disabled: false,
            Format: 'yyyy/MM/dd H:m:s',
            ToDate: false,
            FromDate: false,
            IsGregorian: false,
            EnglishNumber: false,
        });
        </script>
        """ % (name, name)
        return mark_safe(u"%s %s" % (html, js))

    def value_from_datadict(self, data, files, name):
        shamsi_val = data.get(name, None)
        miladi_val = jalali_time_to_gregorian(shamsi_val, to_utc_time=True)
        return miladi_val


class ShamsiDateTimeField(forms.DateTimeField):
    widget = ShamsiDateTimeWidget

    def to_python(self, value):
        return super(ShamsiDateTimeField, self).to_python(value)


class JqueryTimeWidget(forms.TimeInput):
    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = {}
        attrs.update({'autocomplete': 'nope', 'data-date-format': 'H:i', 'data-form-control': 'time', 'data-lang': 'fa', })
        html = super(JqueryTimeWidget, self).render(name, value, attrs, renderer)
        return mark_safe(html)
