import json

import six
from django import forms
from django.forms.utils import ValidationError
from jsonfield.fields import JSONField, JSONFormField


class HardJsonFormField(JSONFormField):
    def to_python(self, value):
        if isinstance(value, six.string_types) and value:
            try:
                return json.loads(value, **self.load_kwargs)
            except ValueError:
                raise ValidationError("فرمت json صحیحی نیست")
        return value

    def clean(self, value):

        if not value and not self.required:
            return None

        # Trap cleaning errors & bubble them up as JSON errors
        try:
            return super(HardJsonFormField, self).clean(value)
        except TypeError:
            raise ValidationError("فرمت json صحیحی نیست")


class HardJsonField(JSONField):
    form_class = HardJsonFormField

    def dumps_for_display(self, value):
        kwargs = {"indent": 2}
        kwargs.update(self.dump_kwargs)
        if not value or isinstance(value, str):
            return value
        return json.dumps(value, **kwargs)

    def get_prep_value(self, value):
        """Convert JSON object to a string"""
        if self.null and value is None:
            return None
        if not value or isinstance(value, str):
            return value
        return json.dumps(value, **self.dump_kwargs)

    def to_python(self, value):
        """The SubfieldBase metaclass calls pre_init instead of to_python, however to_python
        is still necessary for Django's deserializer"""
        while value and isinstance(value, six.string_types):
            try:
                return json.loads(value, **self.load_kwargs)
            except ValueError:
                raise ValidationError("فرمت json صحیحی نیست")
        return value

    def pre_init(self, value, obj):
        """Convert a string value to JSON only if it needs to be deserialized.

        SubfieldBase metaclass has been modified to call this method instead of
        to_python so that we can check the obj state and determine if it needs to be
        deserialized"""

        try:
            if obj._state.adding:
                # Make sure the primary key actually exists on the object before
                # checking if it's empty. This is a special case for South datamigrations
                # see: https://github.com/bradjasper/django-jsonfield/issues/52
                if getattr(obj, "pk", None) is not None:
                    while value and isinstance(value, six.string_types):
                        try:
                            return json.loads(value, **self.load_kwargs)
                        except ValueError:
                            raise ValidationError("فرمت json صحیحی نیست")

        except AttributeError:
            # south fake meta class doesn't create proper attributes
            # see this:
            # https://github.com/bradjasper/django-jsonfield/issues/52
            pass

        return value
