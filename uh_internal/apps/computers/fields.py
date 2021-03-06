"""
.. module:: resnet_internal.apps.computers.models
   :synopsis: University Housing Internal Computer Index Models.

.. moduleauthor:: Thomas Willson <tewillso@calpoly.edu>
.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

import ast
import re

from django.db.models import Field, TextField
from django.forms.fields import RegexField


# MAC Address
MAC_RE = r'^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$'
mac_re = re.compile(MAC_RE, re.IGNORECASE)

# Comma separated integers (list of ports)
CSI_RE = r'^(\d+(,\d+)*)?$'
csi_re = re.compile(CSI_RE)

# Comma separated values (list of domain names)
CSV_RE = r'^(.+(,.+)*)?$'
csv_re = re.compile(CSV_RE, re.DOTALL)


class DomainNameListFormFiled(RegexField):
    default_error_messages = {
        'invalid': 'Domain names must be comma-separated e.g. "a.example.com, b.example.com, c.example.com".',
    }

    def __init__(self, *args, **kwargs):
        super(DomainNameListFormFiled, self).__init__(csv_re, *args, **kwargs)


class MACAddressFormField(RegexField):
    default_error_messages = {
        'invalid': 'Enter a valid MAC address.',
    }

    def __init__(self, *args, **kwargs):
        super(MACAddressFormField, self).__init__(mac_re, *args, **kwargs)


class MACAddressField(Field):
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 17
        super(MACAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {'form_class': MACAddressFormField}
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)


class PortListFormField(RegexField):
    default_error_messages = {
        'invalid': 'Ports must be comma-separated with no whitespace. e.g. "22,80,443,993".',
    }

    def __init__(self, *args, **kwargs):
        super(PortListFormField, self).__init__(csi_re, *args, **kwargs)


class ListField(TextField):
    description = "Stores a python list"

    def from_db_value(self, value, expression, connection, context):
        if not value:
            return []

        try:
            return ast.literal_eval(value)
        except:
            return []

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if not value:
            return []

        try:
            return ast.literal_eval(value)
        except:
            return []

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': PortListFormField}
        defaults.update(kwargs)
        return super(ListField, self).formfield(**defaults)
