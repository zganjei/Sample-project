from django.conf import settings
from django.core import validators
from django.utils.encoding import force_text
from django_select2.forms import ModelSelect2Widget, ModelSelect2TagWidget, ModelSelect2MultipleWidget
from utils.persian import arToPersianChar, persianToEnNumb




class TagTitledModelWidget(ModelSelect2Widget):
    search_fields = ['name__icontains']
    empty_values = list(validators.EMPTY_VALUES)
    default_error_messages = {
        'invalid_choice': "مقدار انتخاب شده معتبر نمی باشد",
    }

    def build_attrs(self, extra_attrs=None, **kwargs):
        """Add select2's tag attributes."""
        self.attrs.setdefault('createSearchChoice', '*START*createIfNotExist*END*')
        return super(TagTitledModelWidget, self).build_attrs(extra_attrs, **kwargs)

    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(TagTitledModelWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        value = super(TagTitledModelWidget, self).value_from_datadict(data, files, name)
        try:
            new_value = self.queryset.get(**{'pk': value})
        except (ValueError, self.queryset.model.DoesNotExist):
            arg = {"title": arToPersianChar(value)}
            if self.http_request.user.is_authenticated:
                arg['creator'] = self.http_request.user
            new_value = self.queryset.create(**arg)
        return new_value.pk


class TitledMultipleModelWidget(ModelSelect2TagWidget):
    search_fields = ['name__icontains', ]

    class Media:
        js = (settings.SELECT2_JS, 'django_select2/django_select2.js', 'select2/i18n/fa.js')
        css = {'screen': (settings.SELECT2_CSS,)}

    def build_attrs(self, extra_attrs=None, **kwargs):
        """Add select2's tag attributes."""
        self.attrs.setdefault('data-width', '700px')
        self.attrs.setdefault('data-dir', 'rtl')
        self.attrs.setdefault('data-token-separators', '[","]')
        self.attrs.setdefault('data-create-search-choice', '*START*django_select2_createSearchChoiceNew*END*')
        self.attrs.setdefault('data-format-result', '*START*django_select2_formatResult*END*')
        # self.attrs.setdefault('data-template-result', '*START*test*END*')

        self.attrs.setdefault('data-minimum-input-length', 2)
        return super(TitledMultipleModelWidget, self).build_attrs(extra_attrs, **kwargs)

    def __init__(self, *args, **kwargs):
        self.http_request = None
        self.inst = None
        self.label = None
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        if 'inst' in kwargs:
            self.inst = kwargs.pop('inst')
        if 'label' in kwargs:
            self.label = kwargs.pop('label')
        super(TitledMultipleModelWidget, self).__init__(*args, **kwargs)

    def get_model_field_values(self, value):
        creator = None
        if self.http_request:
            creator = self.http_request.user
        return {'name': arToPersianChar(value.strip()), 'creator': creator}

    def create_new_value(self, value):
        if self.get_queryset().filter(name=arToPersianChar(value.strip())).exists():
            obj = self.get_queryset().filter(name=arToPersianChar(value.strip()))[0]
        else:
            obj = self.get_queryset().create(**self.get_model_field_values(value))
        return getattr(obj, 'pk')

    def value_from_datadict(self, data, files, name):
        values = super(TitledMultipleModelWidget, self).value_from_datadict(data, files, name)
        qs = self.get_queryset().filter(**{'pk__in': [x for x in list(values) if x.isdigit()]})
        pks = set(force_text(getattr(o, 'pk')) for o in qs)
        cleaned_values = []
        for val in values:
            if force_text(val) not in pks:
                val = self.create_new_value(val.strip())
            cleaned_values.append(val)
        return cleaned_values

    def render_options(self, *args):
        """Render only selected options."""
        try:
            selected_choices, = args
        except ValueError:  # Signature contained `choices` prior to Django 1.10
            choices, selected_choices = args
        output = ['<option></option>' if not self.is_required and not self.allow_multiple_selected else '']
        selected_choices = {force_text(v) for v in selected_choices}
        choices = []
        for pk in selected_choices:
            if pk:
                choices.append((pk, self.label_from_instance(self.get_queryset().get(pk=pk))))
        for option_value, option_label in choices:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)


class MyModelSelect2Widget(ModelSelect2Widget):
    class Media:
        #     js = (settings.SELECT2_JS, 'django_select2/django_select2.js', 'lib/select2/fa.js')
        #     css = {'screen': (settings.SELECT2_CSS,)}
        js = (settings.SELECT2_JS, 'lib/select2/fa.js', 'django_select2/django_select2.js',)
        css = {'screen': (settings.SELECT2_CSS,)}

    def build_attrs(self, *args, **kwargs):
        """Set select2's AJAX attributes."""

        self.attrs.setdefault('data-width', '100%')
        self.attrs.setdefault('class', 'form-control')
        self.attrs.setdefault('data-dir', 'rtl')
        self.attrs.setdefault('data-minimum-input-length', 2)

        attrs = super(MyModelSelect2Widget, self).build_attrs(*args, **kwargs)
        return attrs

    def render_options(self, *args):
        """Render only selected options and set QuerySet from :class:`ModelChoicesIterator`."""
        try:
            selected_choices, = args
        except ValueError:
            choices, selected_choices = args
        selected_choices = {force_text(v) for v in selected_choices}
        output = ['<option></option>' if not self.is_required and not self.allow_multiple_selected else '']
        choices = []
        for pk in selected_choices:
            if pk:
                choices.append((pk, self.label_from_instance(self.get_queryset().get(pk=pk))))
        for option_value, option_label in choices:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

    def filter_queryset(self, term, queryset=None, **dependent_fields):
        term = arToPersianChar(persianToEnNumb(arToPersianChar(term)))
        return super(MyModelSelect2Widget, self).filter_queryset(term, queryset, **dependent_fields)


class MyModelSelect2MultipleWidget(ModelSelect2MultipleWidget):
    search_fields = ['name__icontains']

    class Media:
        js = (settings.SELECT2_JS, 'django_select2/django_select2.js', 'select2/i18n/fa.js')
        css = {'screen': (settings.SELECT2_CSS,)}

    def build_attrs(self, extra_attrs=None, **kwargs):
        """Add select2's tag attributes."""
        self.attrs.setdefault('data-width', '700px')
        self.attrs.setdefault('data-dir', 'rtl')
        self.attrs.setdefault('data-minimum-input-length', 2)
        return super(MyModelSelect2MultipleWidget, self).build_attrs(extra_attrs, **kwargs)

    def render_options(self, *args):
        """Render only selected options."""
        try:
            selected_choices, = args
        except ValueError:  # Signature contained `choices` prior to Django 1.10
            choices, selected_choices = args
        output = ['<option></option>' if not self.is_required and not self.allow_multiple_selected else '']
        selected_choices = {force_text(v) for v in selected_choices}
        choices = []
        for pk in selected_choices:
            if pk:
                choices.append((pk, self.label_from_instance(self.get_queryset().get(pk=pk))))
        for option_value, option_label in choices:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)
