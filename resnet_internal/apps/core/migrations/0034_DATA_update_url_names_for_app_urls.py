# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-08 18:34
from __future__ import unicode_literals

from django.db import migrations

LINK_TRANSLATION_TABLE = [
    ('restech_list_edit', 'technicians:home'),
    ('printers', 'printers:home'),
    ('csd_assign_domain', 'core:csd_assign_domain'),
    ('computers', 'computers:home'),
    ('ports', 'network:ports'),
    ('rooms', 'core:rooms'),
    ('printer_ordered_items', 'printerrequests:ordered_items'),
    ('access_points', 'network:access_points'),
    ('rosters', 'rosters:home'),
    ('resident_lookup', 'residents:home'),
    ('printer_inventory', 'printerrequests:inventory'),
]


def update_navbar_url_names(apps, schema_editor):
    NavbarLink = apps.get_model('core', 'NavbarLink')

    for original, replacement in LINK_TRANSLATION_TABLE:
        qs = NavbarLink.objects.filter(url_name=original)
        if qs.exists():
            for link in qs:
                link.url_name = replacement
                link.save()


def rollback_navbar_url_names(apps, schema_editor):
    NavbarLink = apps.get_model('core', 'NavbarLink')

    for original, replacement in LINK_TRANSLATION_TABLE:
        qs = NavbarLink.objects.filter(url_name=replacement)
        if qs.exists():
            for link in qs:
                link.url_name = original
                link.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_permissionclass_plural'),
    ]

    operations = [
        migrations.RunPython(update_navbar_url_names, reverse_code=rollback_navbar_url_names),
    ]
