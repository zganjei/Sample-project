# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.db import models
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import Template, Context
from django.urls.base import reverse
from django.utils.html import strip_tags
from django.utils.safestring import SafeString, mark_safe

from utils.calverter import gregorian_to_jalali
from utils.manager.filter import Filter
from utils.manager.table import Table, Header, Row
from utils.text import text_to_price



manager_children = []


class ManagerRegister(type):
    def __new__(mcs, name, bases, classdict):
        from django.urls import path
        from kpedia.urls import urlpatterns
        from utils.manager import views

        new_cls = type.__new__(mcs, name, bases, classdict)
        if not new_cls in manager_children and new_cls.manager_name:
            manager_children.append(new_cls)
            urlpatterns += [
                path('%s/%s/' % (settings.ADMIN_BASE_URL, new_cls.manager_name), views.process_main_page,
                     {'manager_name': new_cls.manager_name}, name=new_cls.manager_name),
                path('%s/%s/actions/' % (settings.ADMIN_BASE_URL, new_cls.manager_name), views.process_actions,
                     {'manager_name': new_cls.manager_name}, name=new_cls.manager_name + "_actions"),
            ]
        return new_cls


class ManagerColumn(object):
    def __init__(self, column_name, column_verbose_name, column_width, is_variable=False, allow_html=False,
                 aggregation=False, is_price=False, order_field=None, css_class=None, to_int=False):
        self.column_name = column_name
        self.column_verbose_name = column_verbose_name
        self.column_width = column_width
        self.is_variable = is_variable
        self.is_price = is_price
        self.allow_html = allow_html
        self.aggregation = aggregation
        self.order_field = order_field or column_name
        self.css_class = css_class
        self.visible = column_width != 0
        self.to_int = to_int


class ManagerGroupHeader(object):
    def __init__(self, start_column_name, number_column, title):
        self.start_column_name = start_column_name
        self.number_column = number_column
        self.title = title


class ObjectsManager(metaclass=ManagerRegister):
    # private fields
    __all_data_cashed = None

    manager_name = ""
    permission_name = ""
    manager_verbose_name = ""
    filter_form = None
    filter_handlers = (
        ()
        # ('name_of_field', 'type_of_field', 'django_lookup')
        # type_of_field = str|bool|m2o|m2m|pdate
    )
    minimum_filters = []
    data_per_page = 10
    aggregation = False

    actions = []
    multi_select = False
    excel_export = False
    # action name that must call after search process
    action_after_search = None

    # extra url get params for json action
    extra_params = ''

    # view quality attributes
    height = 350
    auto_width = True

    # extend from base html or nobase html
    has_base_template = True

    def __init__(self, http_request, height=None):
        self.http_request = http_request
        if height:
            self.height = height
        if self.can_view():
            self.columns = self.get_columns()
            rows = http_request.GET.get('length') or self.data_per_page
            all_field_names = [x.order_field for x in self.get_columns()]
            self.filter_obj = Filter(self.http_request, self.filter_form, self.filter_handlers, self.other_filter_func,
                                     rows,
                                     all_field_names, self.minimum_filters)
            all_data = self.get_all_data_cashed()
            self.filter_form, self.page_data = self.filter_obj.process_filter(all_data)

    def get_all_data(self):
        """
            این تابع باید داده ها را برای لیست کردن برگرداند
        """
        return []

    def get_all_data_cashed(self):
        if self.__all_data_cashed is None:
            self.__all_data_cashed = self.get_all_data()
        return self.__all_data_cashed

    def get_columns(self):
        columns = [
            # list of ManagerColumn
        ]
        return columns

    def can_view(self):
        """
            این تابع چک میکند که کاربر میتواند این صفحه را ببیند یا خیر
        """
        if self.http_request.user.is_superuser:
            return True
        # try:
        #     return self.http_request.user.staff.role.menu_permissions.filter(
        #         url_name=self.permission_name or self.manager_name).exists()
        # except ObjectDoesNotExist:
        return False
        #     return True

    def render_main_list(self):
        if not self.can_view():
            raise Http404()
        c = {
            'manager': self
        }
        if self.has_base_template:
            template = 'manager/main.html'
        else:
            template = 'manager/main_no_base.html'
        return render(self.http_request, template, c)

    def action_url(self):
        return reverse('%s_actions' % self.manager_name)

    def process_action_request(self):
        action_type = self.http_request.GET.get('t')
        if action_type == 'json':
            return self.process_json()
        elif action_type == 'action':
            return self.process_manages_actions()
        elif action_type == 'excel':
            return self.process_excel()
        raise Http404()

    def process_json(self):
        table = self._create_data_table(self.page_data)
        json = table.get_dgrid_json(self.filter_obj.total_pages, self.filter_obj.page_num, self.filter_obj.total_data,
                                    self.aggregation)
        return HttpResponse(json, content_type='application/json')

    def process_manages_actions(self):
        action_name = self.http_request.GET.get('n')
        instances_id = self.http_request.GET.get('i')
        selected_instances = self._get_instances_by_ids(instances_id)
        for action in self.actions:
            if action.action_name == action_name:
                if action.is_view:
                    action.set_all_data(self.get_all_data_cashed())
                    return action.action_view(self.http_request, selected_instances)
                else:
                    action.do(self.http_request, selected_instances)
                    res = []
                    for message_item in messages.get_messages(self.http_request):
                        res.append({'message': message_item.message, 'tags': message_item.tags})
                    return HttpResponse(json.dumps(res), content_type="application/json")
        raise Http404()

    def _create_data_table(self, page_data, columns=None):
        id_columns = ManagerColumn('id', 'id', '0')
        if not columns:
            columns = [id_columns] + self.get_columns()
        table = Table()
        header = Header()
        for column in columns:
            header.create_cell(column.column_name, column.column_verbose_name, column.column_width, column.aggregation)

        table.set_header(header)
        for row_item in page_data:
            row = Row()
            for column in columns:
                data = row_item
                column_name = column.column_name
                if not column.is_variable and '__' in column_name:
                    fk = column_name[:column_name.index('__')]
                    column_name = column_name[column_name.index('__') + 2:]
                    data = getattr(data, fk)

                # if isinstance(data, models.Model) and isinstance(data, Visitor) and column_name == 'id':
                #     column_name = 'session_key'
                if column.is_variable:
                    function = getattr(self, 'get_' + column_name)
                    value = function(data)
                else:
                    value = getattr(data, column_name)
                if isinstance(value, bool):
                    if value is True:
                        value = '<i class="fa fa-check text-navy"></i>'
                    else:
                        value = '<i class="fa fa-times text-danger"></i>'
                elif isinstance(value, date):
                    value = gregorian_to_jalali(value)
                elif isinstance(data, models.Model) and not column.is_variable:

                    try:
                        if data.__class__._meta.get_field(column_name).choices:
                            value = getattr(data, 'get_' + column_name + '_display')()
                    except FieldDoesNotExist:
                        pass

                if hasattr(value, 'all'):
                    value = ' ، '.join([str(x) for x in value.all()])
                if callable(value):
                    value = value()

                if column.to_int and value:
                    value = str(int(value))
                elif not isinstance(value, (SafeString,)):
                    value = str(value)

                if value is None or value == 'None':
                    value = "---"
                elif column.is_price:
                    value = text_to_price(value)

                if column.allow_html:
                    value = mark_safe(value)

                row.create_cell(column.column_name, value, column.column_width, column.aggregation)
            table.add_row(row)
        return table

    def get_filter_form_content(self):
        return None

    def get_compiled_filter_form_content(self):
        content = self.get_filter_form_content()
        return Template(content).render(Context({'form': self.filter_form}))

    def _get_instances_by_ids(self, instances_id):
        if instances_id:
            try:
                instances_id = [int(x) for x in instances_id.split(',')]
            except ValueError:
                return []
            instances = []
            all_data = self.get_all_data_cashed()
            for data in all_data:
                if data.pk in instances_id:
                    instances.append(data)
            return instances
        return []

    def process_excel(self):
        import xlsxwriter
        import string

        columns = self.get_excel_columns()
        table = self._create_data_table(self.filter_obj.all_data, columns)

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        worksheet.right_to_left()

        bold = workbook.add_format({'bold': True})
        letters = list(string.ascii_uppercase)
        for case in string.ascii_uppercase:
            for case2 in string.ascii_uppercase:
                letters.append(case + case2)

        group_headers = self.get_group_headers()
        if group_headers:
            i = 2
            for group_header in group_headers:
                column_head_s = letters[i]
                column_head_f = letters[i - 1 + group_header.number_column]
                worksheet.merge_range(column_head_s + '1:' + column_head_f + '1', strip_tags(group_header.title), bold)
                i += group_header.number_column
            i = 1
            for cell in table.header:
                column_head = letters[i - 1]
                worksheet.set_column(column_head + ':' + column_head, int(cell.width) * 2)
                worksheet.write_string(1, i - 1, strip_tags(cell.value), bold)
                i += 1
        else:
            i = 1
            for cell in table.header:
                column_head = letters[i - 1]
                worksheet.set_column(column_head + ':' + column_head, int(cell.width) * 2)
                worksheet.write_string(0, i - 1, strip_tags(cell.value), bold)
                i += 1

        row_i = 1
        if group_headers:
            row_i = 2
        align_format = workbook.add_format({'align': 'right'})
        for row in table:
            cell_i = 0
            for cell in row:
                worksheet.write_string(row_i, cell_i, strip_tags(cell.value), align_format)
                cell_i += 1
            row_i += 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        file_name = datetime.now().strftime('%Y%m%d%H%M%S')
        response['Content-Disposition'] = "attachment; filename=%s.xlsx" % file_name
        return response

    def other_filter_func(self, all_data, form):
        return all_data

    def get_excel_columns(self):
        return []

    def get_group_headers(self):
        return []

    @staticmethod
    def get_manager_by_name(manager_name):
        for manager in manager_children:
            if manager.manager_name == manager_name:
                return manager
        return None
