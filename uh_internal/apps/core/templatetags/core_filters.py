"""
.. module:: resnet_internal.apps.core.templatetags
   :synopsis: University Housing Internal Core Template Tags and Filters.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>
"""

from django import template

from ....settings.base import ACCESS_PERMISSIONS


register = template.Library()


@register.simple_tag(takes_context=True)
def user_has_permission(context, permission_class):
    if permission_class in ACCESS_PERMISSIONS:
        return 'request' in context and hasattr(context['request'], 'user') and context['request'].user.is_authenticated() and context['request'].user.has_access(permission_class)

    raise KeyError('Invalid Permission Class')


@register.filter
def keyvalue(dictionary, key):
    """ Returns a dictionary value given a key.

    :param dictionary: The dictionary to index.
    :type dictionary: dict
    :param key: The key of the value to retrieve.
    :type key: str
    :returns: The value mapped the provided key in the provided dictionary.

    """

    return dictionary[key]


@register.filter
def getrange(value):
    """ Returns an iterator given a range value.

    :param value: The length of the range to produce.
    :type value: int
    :returns: A range based of the value provided.

    """

    return range(value)


@register.filter
def add(value, arg):
    """ Adds two values together and returns the result.

    :param value: The value to modify.
    :type value: any
    :param arg: The value to add to the current value.
    :type arg: any
    :returns: The result of the addition.

    """

    return value + arg


@register.filter
def subtract(value, arg):
    """ Subtracts one value from another and returns the result.

    :param value: The value to modify.
    :type value: any
    :param arg: The value to subtract from the current value.
    :type arg: any
    :returns: The result of the subtraction.

    """

    return value - arg


@register.filter
def multiply(value, arg):
    """Multiplies two values together and returns the result.

    :param value: The value to modify.
    :type value: any
    :param arg: The value to multiply with the current value.
    :type arg: any
    :returns: The result of the multiplication.

    """

    return value * arg


@register.filter
def divide(value, arg):
    """Divides one value by another and returns the result.

    :param value: The value to modify.
    :type value: any
    :param arg: The value by which to divide the current value.
    :type arg: any
    :returns: The result of the division.

    """

    return value / arg


@register.filter
def clean_srs_escapes(value):
    """Cleans uneccessary escapes from SRS strings."""

    return value.replace('\\', '')
