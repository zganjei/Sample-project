# -*- coding:utf-8 -*-



def process_js_validations(form):
    from django import forms

    required = True
    excludes_required = ''
    if hasattr(form, 'js_validation_configs'):
        if 'required' in form.js_validation_configs:
            required = form.js_validation_configs.get('required')
        if 'excludes_required' in form.js_validation_configs:
            excludes_required = form.js_validation_configs.get('excludes_required')
    for field in form.fields:
        validations = ''
        if form.fields[field].required and required and field not in excludes_required:
            validations += 'required,'

        if isinstance(form.fields[field], (forms.DateField, forms.DateTimeField)):
            validations += 'custom[date],'
        elif isinstance(form.fields[field], forms.EmailField):
            validations += 'custom[email],'
        elif isinstance(form.fields[field], forms.FloatField):
            validations += 'custom[number],'
        elif isinstance(form.fields[field], forms.IntegerField):
            validations += 'custom[integer],'
        if field.find('username') > -1 or field.find('email') > -1:
            validations += 'custom[only_english],'
        if hasattr(form, 'extra_js_validation') and form.extra_js_validation.get(field):
            validations += form.extra_js_validation.get(field) + ','

        if validations:
            form.fields[field].widget.attrs.update({'class': 'validate[%s] text-input' % validations})
