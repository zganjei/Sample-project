# -*- coding:utf-8 -*-
from django import forms
from django.forms.models import modelform_factory

from utils.calverter import gregorian_to_jalali, gregorian_to_jalali_time
from utils.fields.date_fields import ShamsiDateField, JqueryTimeWidget, ShamsiDateTimeField
from utils.persian import arToPersianChar

# from utils.geo.geo import GeoFormField




def handle_form_fields(form):
    for field in form.fields:
        if isinstance(form.fields[field], forms.DateTimeField):
            old_field = form.fields[field]
            old_widget_attrs = form.fields[field].widget.attrs
            new_field = ShamsiDateTimeField(label=old_field.label, required=old_field.required,
                                            initial=gregorian_to_jalali_time(old_field.initial))
            form.fields[field] = new_field
            form.fields[field].widget.attrs = old_widget_attrs

        elif isinstance(form.fields[field], forms.DateField):
            old_field = form.fields[field]
            old_widget_attrs = form.fields[field].widget.attrs
            new_field = ShamsiDateField(label=old_field.label, required=old_field.required,
                                        initial=gregorian_to_jalali(old_field.initial))
            form.fields[field] = new_field
            form.fields[field].widget.attrs = old_widget_attrs

        elif isinstance(form.fields[field], forms.TimeField):
            old_widget_attrs = form.fields[field].widget.attrs
            form.fields[field].widget = JqueryTimeWidget(attrs=old_widget_attrs)

        elif isinstance(form.fields[field], forms.FileField):
            form.fields[field].widget.template_name = 'utils/clearable_file_input.html'

        # elif isinstance(form.fields[field], forms.PointField):
        #     old_field = form.fields[field]
        #     old_widget_attrs = form.fields[field].widget.attrs
        #     new_field = GeoFormField(label=old_field.label, required=old_field.required,
        #                              initial=old_field.initial)

        # form.fields[field] = new_field
        # form.fields[field].widget.attrs = old_widget_attrs

        # old_widget_attrs = form.fields[field].widget.attrs
        # form.fields[field].widget = ThumbFileWidget(attrs=old_widget_attrs)


class BaseForm(forms.Form):
    has_placeholder = True

    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(BaseForm, self).__init__(*args, **kwargs)
        handle_form_fields(self)
        # process_js_validations(self)
        self.check_fields()

    def clean(self):
        cd = super(BaseForm, self).clean()
        return cd

    def check_fields(self):
        handle_form_fields(self)
        for field in self.fields:
            if self.fields[field].required and '*' not in self.fields[field].label:
                self.fields[field].label = self.fields[field].label + ' *'

            if not isinstance(self.fields[field], (forms.BooleanField, forms.FileField)):
                if self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs.update({'class': 'form-control'})
                else:
                    self.fields[field].widget.attrs = {'class': 'form-control'}

            if self.has_placeholder and isinstance(self.fields[field], forms.CharField):
                if self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs.update({'placeholder': self.fields[field].label})
                else:
                    self.fields[field].widget.attrs = {'placeholder': self.fields[field].label}


class BaseModelForm(forms.ModelForm):
    has_placeholder = True
    has_creator = False
    has_modifier = False
    exclude_from_clean = []

    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(BaseModelForm, self).__init__(*args, **kwargs)
        if 'creator' in self.fields and not self.has_creator:
            del self.fields['creator']
        if 'modifier' in self.fields and not self.has_modifier:
            del self.fields['modifier']

        self.check_fields()

    def check_fields(self):
        handle_form_fields(self)
        for field in self.fields:
            if self.fields[field].required and '*' not in self.fields[field].label:
                self.fields[field].label = self.fields[field].label + ' *'

            if not isinstance(self.fields[field], (forms.BooleanField, forms.FileField)):
                if self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs.update({'class': 'form-control'})
                else:
                    self.fields[field].widget.attrs = {'class': 'form-control'}

            if self.has_placeholder and isinstance(self.fields[field], forms.CharField):
                if self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs.update({'placeholder': self.fields[field].label})
                else:
                    self.fields[field].widget.attrs = {'placeholder': self.fields[field].label}

                    # process_js_validations(self)

    def clean(self):
        cd = super(BaseModelForm, self).clean()
        for field in self.fields:
            if isinstance(self.fields[field], forms.CharField) and field not in self.exclude_from_clean:
                value = cd.get(field)
                if value and isinstance(value, str):
                    cd[field] = arToPersianChar(value)

        return cd

    def save(self, commit=True):
        obj = super(BaseModelForm, self).save(commit=False)

        if hasattr(self, 'http_request'):
            if obj.id:
                obj.modifier = self.http_request.user
            else:
                obj.creator = self.http_request.user

        if commit:
            obj.save()
            self.save_m2m()

        return obj


class BaseFilterModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(BaseFilterModelForm, self).__init__(*args, **kwargs)
        handle_form_fields(self)

        for field in self.fields:
            self.fields[field].required = False
            if isinstance(self.fields[field], (forms.ModelChoiceField, forms.ChoiceField)):
                if self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs.update({'class': 'form-control', 'data-dir': 'rtl'})
                else:
                    self.fields[field].widget.attrs = {'class': 'form-control', 'data-dir': 'rtl'}

                    # process_js_validations(self)


class BaseFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(BaseFilterForm, self).__init__(*args, **kwargs)
        handle_form_fields(self)

        for field in self.fields:
            if isinstance(self.fields[field], (forms.ModelChoiceField, forms.ChoiceField)):
                if self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs.update({'class': 'form-control', 'data-dir': 'rtl'})
                else:
                    self.fields[field].widget.attrs = {'class': 'form-control', 'data-dir': 'rtl'}


def create_titled_filter(klass):
    class FilterForm(BaseFilterModelForm):
        class Meta:
            model = klass
            fields = ('title',)

    return FilterForm


def create_model_form(klass, **kwargs):
    if not 'exclude' in kwargs:
        kwargs['exclude'] = []

    form = BaseModelForm
    if 'form' in kwargs:
        form = kwargs.pop('form')

    return modelform_factory(klass, form=form, **kwargs)


def confirm_obj(http_request, selected_instances):
    for p in selected_instances:
        p.confirm = True
        p.save()
