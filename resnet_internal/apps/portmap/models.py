"""
.. module:: resnet_internal.apps.network.models
   :synopsis: University Housing Internal Network Models.

   Major credit to Kyle Fast for saving a couple months' worth of work entering database info.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Thomas Willson <thomas.willson@me.com>


"""

from django.db.models.base import Model
from django.db.models.fields import CharField, GenericIPAddressField, BooleanField, PositiveSmallIntegerField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.utils.functional import cached_property

from ..computers.fields import MACAddressField
from ..core.models import Room


class Port(Model):

    room = ForeignKey(Room, verbose_name='Room', null=True)
    switch_ip = GenericIPAddressField(protocol='IPv4', verbose_name='Switch IP')
    switch_name = CharField(max_length=35, verbose_name='Switch Name')
    jack = CharField(max_length=5, verbose_name='Jack')
    blade = PositiveSmallIntegerField(verbose_name='Blade')
    port = PositiveSmallIntegerField(verbose_name='Port')
    active = BooleanField(default=True, verbose_name='Active')

    @cached_property
    def building(self):
        return self.room.building

    @cached_property
    def community(self):
        return self.room.building.community

    def __str__(self):
        return self.jack

    def save(self, *args, **kwargs):
        # Upper jack letters
        for field_name in ['jack']:
            value = getattr(self, field_name, None)
            if value:
                setattr(self, field_name, value.upper())

        super(Port, self).save(*args, **kwargs)


AP_TYPES = ['5 Ghz', '2.4 Ghz', 'Air Monitor']
AP_TYPE_CHOICES = [(AP_TYPES.index(ap_type), ap_type) for ap_type in AP_TYPES]


class AccessPoint(Model):

    name = CharField(max_length=30, verbose_name='DNS Name')
    property_id = CharField(max_length=7, unique=True, verbose_name='Property ID')
    serial_number = CharField(max_length=9, unique=True, verbose_name='Serial Number')
    mac_address = MACAddressField(unique=True, verbose_name='MAC Address')
    port = OneToOneField(Port, related_name='access_point')
    ip_address = GenericIPAddressField(protocol='IPv4', verbose_name='IP Address')
    ap_type = PositiveSmallIntegerField(choices=AP_TYPE_CHOICES, verbose_name='Type')

    @cached_property
    def room(self):
        return self.port.room

    @cached_property
    def building(self):
        return self.room.building

    @cached_property
    def community(self):
        return self.building.community


class NetworkDevice(Model):
    """Network Infrastructure Device."""

    display_name = CharField(max_length=100, verbose_name='Display Name')
    dns_name = CharField(max_length=75, verbose_name='DNS Name')
    ip_address = GenericIPAddressField(verbose_name='IP Address', protocol='IPv4')
