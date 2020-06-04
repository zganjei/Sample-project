# -*- coding: utf-8 -*-
import datetime
import math

from django import forms
from django.core.paginator import Paginator
from django.db.models.query_utils import Q

from utils.calverter import jalali_to_gregorian, jalali_time_to_gregorian
from utils.persian import arToPersianChar, persianToEnNumb




class Filter(object):
    def __init__(self, http_request, filter_form, filter_handlers, other_filter_func, data_per_page, all_field_names, minimum_filters):
        self.http_request = http_request
        self.start_index = self.http_request.GET.get('start') or 1
        try:
            self.page_num = math.ceil((int(self.start_index) + 1) / int(data_per_page))
        except:
            self.page_num = 1
        self.filter_form = filter_form
        self.filter_handlers = filter_handlers
        self.data_per_page = data_per_page
        self.all_field_names = all_field_names
        self.other_filter_func = other_filter_func
        self.minimum_filters = minimum_filters
        self.ordering_handle()

    def process_filter(self, all_data):
        kwargs = {}
        query_filter = Q()
        form = None
        if self.filter_form:
            form = self.filter_form(self.http_request.GET, http_request=self.http_request)
            form_data = form.data
            if self.filter_handlers:
                for handler in self.filter_handlers:
                    select_filter = Filter.__check_handler(handler, kwargs, form_data)
                    if select_filter:
                        query_filter &= select_filter
            elif issubclass(self.filter_form, forms.ModelForm):
                for field in form.fields:
                    if isinstance(form.fields[field], forms.CharField):
                        handler = (field, 'str')
                    elif isinstance(form.fields[field], forms.DateField):
                        handler = (field, 'pdate')
                    elif isinstance(form.fields[field], forms.DateTimeField):
                        handler = (field, 'pdatetime')
                    elif isinstance(form.fields[field], forms.ModelChoiceField):
                        handler = (field, 'm2o')
                    elif isinstance(form.fields[field], forms.ModelMultipleChoiceField):
                        handler = (field, 'm2m')
                    elif isinstance(form.fields[field], forms.NullBooleanField):
                        handler = (field, 'null_bool')
                    elif isinstance(form.fields[field], forms.BooleanField):
                        handler = (field, 'bool')
                    else:
                        handler = (field, '')
                    select_filter = Filter.__check_handler(handler, kwargs, form_data)
                    if select_filter:
                        query_filter &= select_filter

            if self.minimum_filters and not any([form_data.get(x) for x in self.minimum_filters]):
                all_data = all_data.none()

        if hasattr(all_data, 'model'):
            # if self.order_field.replace('-', '') in [f.name for f in all_data.model._meta.get_fields()]:
            if query_filter:
                all_data = all_data.filter(query_filter)
            if self.order_field:
                all_data = all_data.filter(**kwargs).order_by(*self.order_field).distinct()
            else:
                all_data = all_data.filter(**kwargs).distinct()
        elif isinstance(all_data, list) and self.order_field:
            try:
                reverse = True if self.order_type != 'asc' else False
                all_data = sorted(all_data, key=lambda x: getattr(x, self.order_field[0]), reverse=reverse)
            except Exception as e:
                print('Exception in sorting DM data: %s' % str(e))

        all_data = self.other_filter_func(all_data, form)

        self.all_data = all_data

        p = Paginator(all_data, self.data_per_page)
        self.total_pages = p.num_pages
        self.total_data = p.count
        if int(self.page_num) > self.total_pages:
            self.page_num = self.total_pages
        page = p.page(self.page_num)
        paginate_data = page.object_list

        return form, paginate_data

    def ordering_handle(self):
        self.order_field = []
        order_field = str(self.http_request.GET.get('order[0][column]') or '')
        self.order_type = self.http_request.GET.get('order[0][dir]')
        if order_field and order_field.isdigit() and int(order_field) < len(self.all_field_names):
            order_field = self.all_field_names[int(order_field)]
            if self.order_type == 'asc':
                if isinstance(order_field, str):
                    self.order_field = [order_field]
                else:
                    self.order_field = order_field
            else:
                if isinstance(order_field, str):
                    self.order_field = ['-' + order_field]
                else:
                    self.order_field = []
                    for field in order_field:
                        if '-' in field:
                            self.order_field.append(field.replace('-', ''))
                        else:
                            self.order_field.append('-' + field)

    @staticmethod
    def __check_handler(handler, kwargs, form_data):
        field_name = handler[0]
        field_type = handler[1]

        if len(handler) > 2:
            if handler[2] is None:
                return
            django_lookup = handler[2] or field_name
        else:
            django_lookup = field_name

        field_value = persianToEnNumb(arToPersianChar(form_data.get(field_name)))
        if field_value and field_value != 'None':
            if field_type == 'str':
                search_field = django_lookup + '__icontains'
                select = Q()
                term = field_value.replace('\t', ' ')
                term = term.replace('\n', ' ')
                for t in [t for t in term.split(' ') if not t == '']:
                    select &= Q(**{search_field: t})
                return select
            elif field_type == 'bool':
                if field_value == 'on':
                    kwargs[django_lookup] = True
            elif field_type == 'null_bool':
                if field_value in (2, "2"):
                    kwargs[django_lookup] = True
                elif field_value in (3, "3"):
                    kwargs[django_lookup] = False
            elif field_type == 'm2o':
                kwargs[django_lookup + '__id'] = field_value
            elif field_type == 'm2m':
                kwargs[django_lookup + '__in'] = field_value
            elif field_type == 'pdate':
                miladi_date = jalali_to_gregorian(field_value)
                if django_lookup.endswith('gte'):
                    kwargs[django_lookup] = datetime.datetime.combine(miladi_date, datetime.time.min)
                elif django_lookup.endswith('lte'):
                    kwargs[django_lookup] = datetime.datetime.combine(miladi_date, datetime.time.max)
                else:
                    kwargs[django_lookup] = miladi_date.isoformat()
            elif field_type == 'pdatetime':
                kwargs[django_lookup] = jalali_time_to_gregorian(field_value, to_tehran_time=True)
            else:
                kwargs[django_lookup] = field_value
