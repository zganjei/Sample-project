# -*- coding: utf-8 -*-
from collections import OrderedDict

from django import forms
from django.contrib import messages
from django.http import Http404
from django.http.request import QueryDict
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse




class ManagerAction(object):
    action_name = ""  # the name that use for creating js and ajax
    action_verbose_name = ""  # the name that show to user
    confirm_message = ""
    is_view = False  # if True should override action_view
    is_popup = True
    new_tab = False
    css_class = 'btn-primary'
    font_awesome_class = ''
    height = '200'
    width = '800'

    min_count = None
    max_count = None

    def do(self, http_request, selected_instances):
        pass

    def action_view(self, http_request, selected_instances):
        pass

    def set_all_data(self, all_data):
        self.all_data = all_data

    def get_all_data(self):
        if hasattr(self, 'all_data'):
            return self.all_data
        return []


class AddAction(ManagerAction):
    is_view = True
    css_class = 'btn-outline btn-success'
    font_awesome_class = 'fa fa-plus'

    def __init__(self, modelForm, action_name='add', action_verbose_name="افزودن", form_title="افزودن",
                 save_def=None):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title
        self.save_def = save_def

    def action_view(self, http_request, selected_instances):
        if http_request.method == 'POST':
            form = self.modelForm(http_request.POST, http_request.FILES, http_request=http_request)
            if form.is_valid():
                if self.save_def:
                    instance = form.save(commit=False)
                    self.save_def(http_request, instance)
                else:
                    form.save()
                form = None
                messages.success(http_request, "%s با موفقیت انجام شد." % self.form_title)
        else:
            form = self.modelForm(http_request=http_request)

        return render(http_request, 'manager/actions/add_edit.html', {'form': form, 'title': self.form_title})


class EditAction(ManagerAction):
    is_view = True
    css_class = 'btn-outline btn-info'
    font_awesome_class = 'fa fa-edit'
    max_count = 1
    min_count = 1

    def __init__(self, modelForm, action_name='edit', action_verbose_name="ویرایش", form_title="ویرایش"):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()
        if http_request.method == 'POST':
            form = self.modelForm(http_request.POST, http_request.FILES, instance=selected_instances[0],
                                  http_request=http_request)
            if form.is_valid():
                form.save()
                form = None
                messages.success(http_request, "%s با موفقیت انجام شد." % self.form_title)
        else:
            form = self.modelForm(instance=selected_instances[0], http_request=http_request)

        return render(http_request, 'manager/actions/add_edit.html', {'form': form, 'title': self.form_title})


class DoAction(ManagerAction):
    action_name = 'do'
    confirm_message = 'آیا از انجام این عملیات اطمینان دارید؟'

    def __init__(self, do_function=None, action_name='', action_verbose_name="", min_count='1',
                 confirm_message=None):
        if do_function:
            self.do = do_function
        if action_name:
            self.action_name = action_name
        if action_verbose_name:
            self.action_verbose_name = action_verbose_name
        self.min_count = min_count
        if confirm_message:
            self.confirm_message = confirm_message

    def do(self, http_request, selected_instances):
        pass


class LinkAction(ManagerAction):
    action_name = 'link'
    css_class = 'btn-outline btn-info'
    max_count = 1
    min_count = 1
    is_view = True
    is_popup = False
    url_name = ''

    def __init__(self, action_name='', action_verbose_name='', url_name=''):
        if action_name:
            self.action_name = action_name
        if action_verbose_name:
            self.action_verbose_name = action_verbose_name
        if url_name:
            self.url_name = url_name

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        return HttpResponseRedirect(reverse(self.url_name, args=[selected_instances[0].id]))


class DeleteAction(DoAction):
    action_name = 'delete'
    css_class = 'btn-outline btn-danger'
    font_awesome_class = 'fa fa-times'
    action_verbose_name = 'حذف'
    confirm_message = 'آیا از حذف موارد انتخاب شده اطمینان دارید؟'

    def do(self, http_request, selected_instances):
        for obj in selected_instances:
            obj.delete()


class ShowAction(ManagerAction):
    action_name = 'show'
    action_verbose_name = "مشاهده جزئیات"
    is_view = True

    def __init__(self, modelForm, action_name='show', action_verbose_name="مشاهده جزئیات", form_title="مشاهده",
                 width='800', height='200', min_count='1'):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title
        self.height = height
        self.width = width
        self.min_count = min_count

    def action_view(self, http_request, selected_instances):
        form = self.modelForm(instance=selected_instances[0], prefix='show', http_request=http_request)
        for field in form.fields:
            form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        return render(http_request, 'manager/actions/show.html', {'form': form, 'title': self.form_title})


class ConfirmAction(ManagerAction):
    is_view = True

    def __init__(self, field_name, action_name='confirm', action_verbose_name="بررسی", form_title="بررسی",
                 min_count='1', field_label="تایید شده", on_change_event=None):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.field_name = field_name
        self.form_title = form_title
        self.min_count = min_count
        self.field_label = field_label
        self.height = '200'
        self.on_change_event = on_change_event

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        field_label = self.field_label
        field_val = getattr(selected_instances[0], self.field_name)

        class ConfirmForm(forms.Form):
            confirm = forms.NullBooleanField(label=field_label, initial=field_val, required=False)
            confirm.widget.choices = (('1', "نامشخص"),
                                      ('2', "بله"),
                                      ('3', "خیر"))

        if http_request.method == 'POST':
            form = ConfirmForm(http_request.POST)
            if form.is_valid():
                confirm = form.cleaned_data.get('confirm')
                setattr(selected_instances[0], self.field_name, confirm)
                selected_instances[0].save()
                form = None
                if self.on_change_event:
                    self.on_change_event(selected_instances[0], confirm)
                messages.success(http_request, "%s با موفقیت انجام شد." % self.form_title)
        else:
            form = ConfirmForm()

        return render(http_request, 'manager/actions/add_edit.html', {'form': form, 'title': self.form_title})


class FormsetActionItem:
    def __init__(self, formset, prefix, title):
        self.Formset = formset
        self.prefix = prefix
        self.title = title
        self.formset_obj = None


class AddFormsetsAction(ManagerAction):
    is_view = True
    css_class = 'btn-outline btn-success'
    font_awesome_class = 'fa fa-plus'

    def __init__(self, modelForm, formset_mapper, action_name='add', action_verbose_name="افزودن", form_title="افزودن", link_to_edit=False,
                 template_name=None):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title
        self.formset_mapper = formset_mapper
        self.link_to_edit = link_to_edit
        self.template_name = template_name

    def action_view(self, http_request, selected_instances):
        for formset_action_item in self.formset_mapper:
            formset_action_item.formset_obj = formset_action_item.Formset(prefix=formset_action_item.prefix)

        # poll_formset = PollFormset(prefix='poll')
        # pre_attach_formset = PreAttachmentFormset(prefix='pre_attach')
        # pre_attach_formset = PostAttachmentFormset(prefix='post_attach')
        if http_request.method == 'POST':
            form = self.modelForm(http_request.POST, http_request.FILES, http_request=http_request)
            if form.is_valid():
                obj = form.save(commit=False)
                formset_isvalid = True
                for formset_action_item in self.formset_mapper:
                    formset_action_item.formset_obj = formset_action_item.Formset(
                        http_request.POST, http_request.FILES, prefix=formset_action_item.prefix, instance=obj)
                    if not formset_action_item.formset_obj.is_valid():
                        formset_isvalid = False

                if formset_isvalid:
                    obj.save()
                    form.save_m2m()
                    form = None
                    for formset_action_item in self.formset_mapper:
                        formset_action_item.formset_obj = formset_action_item.Formset(
                            http_request.POST, http_request.FILES, prefix=formset_action_item.prefix, instance=obj)
                        if formset_action_item.formset_obj.is_valid():
                            formset_action_item.formset_obj.save(commit=True)
                    messages.success(http_request, "%s با موفقیت انجام شد." % self.form_title)
                    if self.link_to_edit:
                        new_params = OrderedDict({'n': 'edit', 'i': obj.id})
                        edit_url = change_query_string(http_request, new_params)
                        return HttpResponseRedirect(edit_url)
        else:
            form = self.modelForm(http_request=http_request)

        return render(http_request, self.template_name or 'manager/actions/add_edit_with_formsets.html',
                      {'form': form, 'title': self.form_title,
                       'formset_mapper': self.formset_mapper,
                       })


class EditFormsetsAction(ManagerAction):
    is_view = True
    css_class = 'btn-outline btn-info'
    font_awesome_class = 'fa fa-edit'
    max_count = 1
    min_count = 1

    def __init__(self, modelForm, formset_mapper, action_name='edit', action_verbose_name="ویرایش", form_title="ویرایش",
                 template_name=None):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title
        self.formset_mapper = formset_mapper
        self.template_name = template_name

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        obj = selected_instances[0]

        if http_request.method == 'POST':
            for formset_action_item in self.formset_mapper:
                formset_action_item.formset_obj = formset_action_item.Formset(http_request.POST, http_request.FILES,
                                                                              prefix=formset_action_item.prefix,
                                                                              instance=obj)
            form = self.modelForm(http_request.POST, http_request.FILES, instance=obj,
                                  http_request=http_request)
            if form.is_valid():
                obj = form.save(commit=False)
                formset_isvalid = True
                for formset_action_item in self.formset_mapper:
                    if not formset_action_item.formset_obj.is_valid():
                        formset_isvalid = False

                if formset_isvalid:
                    obj.save()
                    form.save_m2m()
                    form = None
                    for formset_action_item in self.formset_mapper:
                        items = formset_action_item.formset_obj.save(commit=True)
                    messages.success(http_request, "%s با موفقیت انجام شد." % self.form_title)
        else:
            form = self.modelForm(instance=obj, http_request=http_request)
            for formset_action_item in self.formset_mapper:
                formset_action_item.formset_obj = formset_action_item.Formset(prefix=formset_action_item.prefix,
                                                                              instance=obj)

        return render(http_request, self.template_name or 'manager/actions/add_edit_with_formsets.html',
                      {'form': form, 'title': self.form_title,
                       'formset_mapper': self.formset_mapper})


class FormsetsAction(ManagerAction):
    is_view = True
    css_class = 'btn-outline btn-info'
    font_awesome_class = 'fa fa-edit'
    max_count = 1
    min_count = 1

    def __init__(self, formset_mapper, action_name='formset-edit', action_verbose_name="ویرایش", form_title="ویرایش"):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.form_title = form_title
        self.formset_mapper = formset_mapper

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        obj = selected_instances[0]

        success = False
        if http_request.method == 'POST':
            for formset_action_item in self.formset_mapper:
                formset_action_item.formset_obj = formset_action_item.Formset(http_request.POST, http_request.FILES,
                                                                              prefix=formset_action_item.prefix,
                                                                              instance=obj)
            formset_isvalid = True
            for formset_action_item in self.formset_mapper:
                if not formset_action_item.formset_obj.is_valid():
                    formset_isvalid = False

            if formset_isvalid:
                for formset_action_item in self.formset_mapper:
                    items = formset_action_item.formset_obj.save(commit=True)
                messages.success(http_request, "%s با موفقیت انجام شد." % self.form_title)
                success = True
        else:
            for formset_action_item in self.formset_mapper:
                formset_action_item.formset_obj = formset_action_item.Formset(prefix=formset_action_item.prefix,
                                                                              instance=obj)

        return render(http_request, 'manager/actions/formsets_action.html',
                      {'title': self.form_title, 'formset_mapper': self.formset_mapper, 'success': success})


def change_query_string(http_request, new_params):
    query_dict = QueryDict(http_request.META.get('QUERY_STRING', '').encode('utf8')).copy()

    for item in new_params:
        query_dict[item] = new_params[item]

    action_url = '%s?%s' % (http_request.path_info, query_dict.urlencode())

    return action_url
