from django.core.exceptions import ValidationError
from django.db import models
from django.forms.fields import NullBooleanField, MultipleChoiceField
from django.forms.widgets import NullBooleanSelect


class HardNullBooleanSelect(NullBooleanSelect):
    def __init__(self, attrs=None):
        choices = (('1', '--همه--'),
                   ('2', 'بله'),
                   ('3', 'خیر')
                   )
        super(NullBooleanSelect, self).__init__(attrs, choices)


class HardNullBooleanField(NullBooleanField):
    widget = HardNullBooleanSelect


class IntegerMultipleChoiceField(MultipleChoiceField):
    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return [int(val) for val in value]


class CharNullField(models.CharField):
    """
    Subclass of the CharField that allows empty strings to be stored as NULL.
    """

    description = "CharField that stores NULL but returns ''."

    def from_db_value(self, value, expression, connection):
        """
        Gets value right out of the db and changes it if its ``None``.
        """
        if value is None:
            return ''
        else:
            return value

    def to_python(self, value):
        """
        Gets value right out of the db or an instance, and changes it if its ``None``.
        """
        if isinstance(value, models.CharField):
            # If an instance, just return the instance.
            return value
        if value is None:
            # If db has NULL, convert it to ''.
            return ''

        # Otherwise, just return the value.
        return value

    def get_prep_value(self, value):
        """
        Catches value right before sending to db.
        """
        if value == '':
            # If Django tries to save an empty string, send the db None (NULL).
            return None
        else:
            # Otherwise, just pass the value.
            return value
