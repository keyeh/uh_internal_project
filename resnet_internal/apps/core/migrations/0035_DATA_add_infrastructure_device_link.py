# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-09 11:20
from __future__ import unicode_literals

from django.db import migrations


def add_infrastructure_device_link(apps, schema_editor):
    NavbarLink = apps.get_model('core', 'NavbarLink')
    PermissionClass = apps.get_model('core', 'PermissionClass')

    if not NavbarLink.objects.filter(display_name='Network Infrastructure').exists():
        link = NavbarLink()
        link.display_name = 'Network Infrastructure'
        link.icon = 'images/icons/database.png'
        link.sequence_index = 5

        parent_qs = NavbarLink.objects.filter(display_name='Databases')
        if parent_qs.exists():
            link.parent_group = parent_qs.first()
        else:
            return

        link.url_name = 'network:network_infrastructure_devices'
        link.save()

        permission_class_qs = PermissionClass.objects.filter(name='network')
        if permission_class_qs.exists():
            link.permission_classes.add(permission_class_qs.first())

        link.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_DATA_update_url_names_for_app_urls'),
    ]

    operations = [
        migrations.RunPython(add_infrastructure_device_link),
    ]